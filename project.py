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


@app.route('/topics/')
def contents():
    session = DBSession()  # open session
    topics = session.query(Topic).all()
    session.close()
    return render_template('contents.html', topics=topics)


# Route (GET Request) for returning a topic's contents
@app.route('/topics/<int:topic_id>/')
def topicContents(topic_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    sections = session.query(Section).filter_by(topic_id=topic.id)
    session.close()
    return render_template('topicContents.html',
                           topic=topic, sections=sections)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
