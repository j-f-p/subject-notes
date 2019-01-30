#!/usr/bin/env python
from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Topic, Section

app = Flask(__name__)

engine = create_engine('sqlite:///deepLearningNotes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)  # define a configured session class


# Subject string constant
#   Defined as a string literal return value to ensure that it is constant.
#   Value not in database, until feature is added to enable user to specify it.
def subject():
    return "Deep Learning"


@app.route('/topics/')
def contents():
    session = DBSession()  # open session
    topics = session.query(Topic).all()
    session.close()
    return render_template('contents.html', subject=subject(), topics=topics)


# Route for returning a topic's contents (GET Request)
@app.route('/topics/<int:topic_id>/')
def topicContents(topic_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    sections = session.query(Section).filter_by(topic_id=topic.id)
    session.close()
    return render_template('topicContents.html', subject=subject(),
                           topic=topic, sections=sections)


# Route for adding a new topic section
@app.route('/topics/<int:topic_id>/new/', methods=['GET', 'POST'])
def newSection(topic_id):
    if request.method == 'POST':
        session = DBSession()
        newSection = Section(
            name=request.form['name'], notes=request.form['notes'],
            topic_id=topic_id)
        session.add(newSection)
        session.commit()
        session.close()
        flash('Added section: "{}"'.format(newSection.name))
        return redirect(url_for('topicContents', topic_id=topic_id))
    else:
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        session.close()
        return render_template('newSection.html', topic=topic)


# Route for viewing a topic section (GET Request)
@app.route('/topics/<int:topic_id>/<int:section_id>/')
def viewSection(topic_id, section_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    section = session.query(Section).filter_by(id=section_id).one()
    session.close()
    return render_template('viewSection.html', subject=subject(), topic=topic,
                           section=section)


# Route for updating a topic section
@app.route('/topics/<int:topic_id>/<int:section_id>/edit/',
           methods=['GET', 'POST'])
def editSection(topic_id, section_id):
    if request.method == 'POST':
        session = DBSession()
        section = session.query(Section).filter_by(id=section_id).one()
        section.name = request.form['name']
        section.notes = request.form['notes']
        session.add(section)
        session.commit()
        session.close()
        flash('{} was updated.'.format(section.name))
        return redirect(url_for('topicContents', topic_id=topic_id))
    else:
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.close()
        return render_template(
            'editSection.html', topic=topic, section=section)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
