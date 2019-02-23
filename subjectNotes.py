#!/usr/bin/env python3
import random
import string
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Topic, Section

app = Flask(__name__)

engine = create_engine('sqlite:///deepLearningNotes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)  # define a configured session class


# This app employs the following terms to label its contents in hierarchical
# order: subect, topic, section and note. A note is some string literal or
# component thereof, defined by the user. A section comprises one or more
# notes. A topic comprises one or more sections. And the subject comprises one
# or more topics.


# Subject string constant
#   Defined as a string literal return value to ensure that it is constant.
#   Value not in database, until feature is added to enable user to specify it.
def subject():
    return "Deep Learning"


# Route for authentication form
#   login_session['state'] is a token that adds a layer of security against a
#   request forgery.
@app.route('/login/')
def viewLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return "The current session state token is \"%s\"." %\
        login_session['state']


# Route for viewing the subject's contents in terms of topics
@app.route('/topics/')
def contents():
    session = DBSession()  # open session
    topics = session.query(Topic).all()
    # latest_sections is an array of doubles: [(section, tname), ..., (...)].
    # Each double is a section and its associated topic name.
    latest_sections = session.query(Section, Topic.name).\
        filter(Section.topic_id == Topic.id).\
        order_by(Section.id.desc())[0:5]
    session.close()
    return render_template('contents.html', subject=subject(), topics=topics,
                           latest_sections=latest_sections)


# Route for viewing a topic's contents in terms of sections (GET Request)
@app.route('/topics/<int:topic_id>/')
def topicContents(topic_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    sections = session.query(Section).filter_by(topic_id=topic.id).all()
    session.close()
    return render_template('topicContents.html', subject=subject(),
                           topic=topic, sections=sections)


# Route for adding a new topic section
@app.route('/topics/<int:topic_id>/new/', methods=['GET', 'POST'])
def newSection(topic_id):
    if request.method == 'POST':
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        new_section = Section(
            name=request.form['name'], notes=request.form['notes'],
            topic_id=topic_id)
        session.add(new_section)
        session.commit()
        flashMessage = 'Section "{}" was added to topic "{}".'\
            .format(new_section.name, topic.name)
        session.close()
        flash(flashMessage)
        return redirect(url_for('topicContents', topic_id=topic_id))
    else:
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        session.close()
        return render_template('newSection.html', subject=subject(),
                               topic=topic)


# Route for viewing a topic section (GET Request)
@app.route('/topics/<int:topic_id>/<int:section_id>/')
def viewSection(topic_id, section_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    sections = session.query(Section).filter_by(topic_id=topic.id)
    section = session.query(Section).filter_by(id=section_id).one()
    session.close()
    return render_template('viewSection.html', subject=subject(), topic=topic,
                           sections=sections, section=section)


# Route for updating a topic section
@app.route('/topics/<int:topic_id>/<int:section_id>/edit/',
           methods=['GET', 'POST'])
def editSection(topic_id, section_id):
    if request.method == 'POST':
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        if request.form['name'] != "" or request.form['notes'] != "":
            if request.form['name'] != "":
                section.name = request.form['name']
            if request.form['notes'] != "":
                section.notes = request.form['notes']
            session.add(section)
            session.commit()
            flashMessage = 'Section "{}" of topic "{}" was updated.'\
                .format(section.name, topic.name)
            flash(flashMessage)
        session.close()
        return redirect(url_for('viewSection', topic_id=topic_id,
                                section_id=section_id))
    else:
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.close()
        return render_template('editSection.html',
                               subject=subject(), topic=topic, section=section)


# Route for deleting a topic section
@app.route('/topics/<int:topic_id>/<int:section_id>/delete/',
           methods=['GET', 'POST'])
def deleteSection(topic_id, section_id):
    if request.method == 'POST':
        session = DBSession()  # open session
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.delete(section)
        session.commit()
        # At this point, section is not tied to a session and can be employed
        # outside the session, however, topic is tied to the session.
        flashMessage = ('Section "{}" was deleted from topic "{}".'
                        .format(section.name, topic.name))
        session.close()
        flash(flashMessage)
        return redirect(url_for('topicContents', topic_id=topic_id))
    else:
        session = DBSession()  # open session
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.close()
        return render_template('deleteSection.html',
                               subject=subject(), topic=topic, section=section)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
