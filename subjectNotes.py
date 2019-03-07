#!/usr/bin/env python3
import hashlib
import os
import google_auth_oauthlib.flow
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify
from flask import session as signed_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Topic, Section
from app_consts import gapiGSIscopes, gpdFileName, subject

app = Flask(__name__)

engine = create_engine('sqlite:///test.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)  # define a configured session class


# This app employs the following terms to label its contents in hierarchical
# order: subect, topic, section and note. A note is some string literal or
# component thereof, defined by the user. A section comprises one or more
# notes. A topic comprises one or more sections. And the subject comprises one
# or more topics.


# Place relevant Google API project credentials in Python dictionary.
def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


# Route for sign in desk
@app.route('/signindesk/')
def signInDesk():
    return render_template('signInDesk.html', subject=subject())


# Route for starting authentication by OAuth 2 framework protocol flow.
@app.route('/authenticate/')
def authenticate():
    # Initialize flow instance for managing the protocol flow.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        gpdFileName(), scopes=gapiGSIscopes())

    # Set redirect URI to that set in the Google API Console.
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so that the callback can verify the auth server response.
    # This inhibits request forgery.
    signed_session['state'] = state

    # Redirect to Google's Oauth 2 server and activate Google Sign-In.
    return redirect(authorization_url)


# Handle authorization code or error from Google Sign-In response. If response
# is an authorization code, exchange it for refresh and access tokens and
# access Google API project credentials. Otherwise, abort sign in.
@app.route('/oauth2callback')
def oauth2callback():
    if request.args.get('code'):
        # Re-initialize flow instance with verification of session state.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            gpdFileName(), scopes=gapiGSIscopes(),
            state=signed_session['state'])

        flow.redirect_uri = url_for('oauth2callback', _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0
        # tokens. This response is flask.request.url.
        flow.fetch_token(authorization_response=request.url)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        signed_session['credentials'] = credentials_to_dict(flow.credentials)

        flash("Sign in approved.")
    else:
        flash("Sign in aborted.")
    return redirect(url_for('contents'))

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
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = hashlib.sha256(os.urandom(1024)).hexdigest()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
