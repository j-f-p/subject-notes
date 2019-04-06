from hashlib import sha256
from os import environ, urandom
from requests import post
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify
from flask import session as signed_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from database_setup import Base, Topic, Section, maxSectionsPerTopic
from app_consts import gaj, gajFileName, gapiOauth, gapiScopes, subject

app = Flask(__name__)

app.config['SECRET_KEY'] = sha256(urandom(1024)).hexdigest()
# For development and exhibition, have JSON endpoints present JSON for human
# readability. For a production, app present JSON minified, thus, remove the
# below line.
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

if environ.get('DATABASE_URL') is None:
    engine = create_engine('postgresql:///deeplearning')
else:
    engine = create_engine(environ.get('DATABASE_URL'))

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


# Method that returns a Boolean that indicates whether user is signed or not.
def signedIn():
    # Since 'userinfo' depends on 'credentials', only a check for 'credentials'
    # is made.
    return 'credentials' in signed_session


# Method that returns Google account email if user is signed in.
def gaem():
    if 'credentials' in signed_session:
        return signed_session['userinfo']['email']
    else:
        return None


# Method that returns Google account 'given_name' if user is signed in.
def gagn():
    if 'credentials' in signed_session:
        return signed_session['userinfo']['given_name']
    else:
        return None


# Route for sign in desk
@app.route('/signindesk/')
def signInDesk():
    if 'credentials' not in signed_session:
        if request.referrer is not None:
            signed_session['signInReferrer'] = request.referrer
        else:
            signed_session['signInReferrer'] = url_for('contents')

        return render_template('signInDesk.html', subject=subject())

    # Otherwise, user is already signed-in and method return quietly, without
    # displaying a "flash" message.
    if request.referrer is not None:
        return redirect(request.referrer)
    else:
        return redirect(url_for('contents'))

# Route for starting authentication by OAuth 2 framework protocol flow
@app.route('/authenticate/')
def authenticate():
    # Initialize flow instance for managing the protocol flow.
    flow = Flow.from_client_secrets_file(gajFileName(), scopes=gapiScopes())

    # Set redirect URI to that set in the Google API Console.
    flow.redirect_uri = gaj()['web']['redirect_uris'][2]

    authorization_url, state = flow.authorization_url(
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so that the callback can verify the auth server response.
    # This inhibits request forgery.
    signed_session['state'] = state

    # Redirect to Google's Oauth 2 server and activate Google Sign-In.
    return redirect(authorization_url)


# Route for handling Google Sign-In response
# Handle authorization code or error from Google Sign-In response. If response
# is an authorization code, exchange it for refresh and access tokens and
# access Google API project credentials. Otherwise, abort sign in.
@app.route('/oauth2callback')
def oauth2callback():
    if request.args.get('code'):
        # Re-initialize flow instance with verification of session state.
        flow = Flow.from_client_secrets_file(
            gajFileName(), scopes=gapiScopes(), state=signed_session['state'])

        # This is part of the re-initialization, by API design.
        flow.redirect_uri = gaj()['web']['redirect_uris'][2]

        # Use the authorization server's response to fetch the OAuth 2.0
        # tokens. This response is flask.request.url.
        flow.fetch_token(authorization_response=request.url)

        # Store credentials in session.
        # TODO: For production, store credentials encrypted in a persistent
        #       database.
        signed_session['credentials'] = credentials_to_dict(flow.credentials)

        oauth2 = build(gapiOauth()['name'], gapiOauth()['version'],
                       credentials=flow.credentials)

        # Store userinfo in session.
        # TODO: For production, store userinfo encrypted in a persistent
        #       database.
        signed_session['userinfo'] = oauth2.userinfo().get().execute()

        flash('Sign in approved. Welcome {}.'.
              format(signed_session['userinfo']['given_name']))
    else:
        flash('Sign in aborted.')
    return redirect(signed_session['signInReferrer'])


# Route for sigining out
@app.route('/signout/')
def signOut():
    if 'credentials' in signed_session:
        credentials = Credentials(**signed_session['credentials'])

        # Revoke credentials
        revoke = post(
            'https://accounts.google.com/o/oauth2/revoke',
            params={'token': credentials.token},
            headers={'content-type': 'application/x-www-form-urlencoded'})

        revoke_status_code = getattr(revoke, 'status_code')

        # Clear credentials and user info from session
        del signed_session['credentials']
        del signed_session['userinfo']
        session_cleared = True

        if 'credentials' in signed_session or 'userinfo' in signed_session:
            session_cleared = False

        if revoke_status_code == 200 and session_cleared:
            flash('You\'ve successfully signed out.')
        else:
            flash('A sign-out error occurred.')
    # else user is not signed-in and method returns quietly

    if request.referrer is not None:
        return redirect(request.referrer)
    else:
        return redirect(url_for('contents'))


# Route for root
@app.route('/')
def root():
    return redirect(url_for('contents'))


# Route for viewing the subject's contents in terms of topics
@app.route('/topics/')
def contents():
    session = DBSession()  # open session
    topics = session.query(Topic).all()
    # latest_sections is an array of doubles: [(section, t.title), ..., (...)].
    # Each double is a section and its associated topic title.
    latest_sections = session.query(Section, Topic.title).\
        filter(Section.topic_id == Topic.id).\
        order_by(Section.utce.desc())[0:5]
    session.close()
    return render_template(
        'contents.html', subject=subject(), signedIn=signedIn(), uname=gagn(),
        topics=topics, latest_sections=latest_sections)


# Route for viewing a topic's contents in terms of sections
@app.route('/topics/<int:topic_id>/')
def topicContents(topic_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    sections = session.query(Section).filter_by(topic_id=topic.id).\
        order_by(Section.id).all()
    session.close()
    return render_template(
        'topicContents.html', subject=subject(), signedIn=signedIn(),
        uname=gagn(), maxNumSecs=maxSectionsPerTopic(),
        topic=topic, sections=sections)


# Route for adding a new topic section
@app.route('/topics/<int:topic_id>/new/', methods=['GET', 'POST'])
def newSection(topic_id):
    if 'credentials' not in signed_session:
        flash('Please sign in.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))

    if request.method == 'POST':
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        lastTopicSec_id = session.query(Section).\
            filter_by(topic_id=topic_id).order_by(Section.id.desc()).first().id
        new_section = Section(
            title=request.form['title'], notes=request.form['notes'],
            initiator=gaem(), topic_id=topic_id, id=lastTopicSec_id+1)
        session.add(new_section)
        session.commit()
        flash('Section "{}" was added to topic "{}" by {}.'
              .format(new_section.title, topic.title, gagn()))
        session.close()
        return redirect(url_for(
            'viewSection', topic_id=topic_id, section_id=new_section.id))
    else:
        session = DBSession()
        nTopSecs = session.query(Section).filter_by(topic_id=topic_id).count()
        if nTopSecs == maxSectionsPerTopic():
            session.close()
            flash('Number of sections of topic is at maximum.')
            return redirect(url_for('topicContents', topic_id=topic_id))
        else:
            topic = session.query(Topic).filter_by(id=topic_id).one()
            session.close()
            return render_template('newSection.html', subject=subject(),
                                   uname=gagn(), topic=topic)


# Route for viewing a topic section
@app.route('/topics/<int:topic_id>/<int:section_id>/')
def viewSection(topic_id, section_id):
    session = DBSession()  # open session
    topic = session.query(Topic).filter_by(id=topic_id).one()
    sections = session.query(Section).filter_by(topic_id=topic.id).\
        order_by(Section.id).all()
    section = session.query(Section).filter_by(id=section_id).one()
    session.close()
    if section.id == sections[0].id:
        # It's possible that an intro section is selected from the contents
        # view via url. Then, render the associated topic contents view.
        return redirect(url_for('topicContents', topic_id=topic_id))
    else:
        return render_template(
            'viewSection.html', subject=subject(), signedIn=signedIn(),
            uname=gagn(), maxNumSecs=maxSectionsPerTopic(),
            topic=topic, sections=sections, section=section)


# Route for updating a topic's first section notes
@app.route('/topics/<int:topic_id>/<int:section_id>/editTS0/',
           methods=['GET', 'POST'])
def editTopicSection0(topic_id, section_id):
    if 'credentials' not in signed_session:
        flash('Please sign in.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))

    if request.method == 'POST':
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        if request.form['notes'] != "":
            section.notes = request.form['notes']
            section.editor = gaem()
            session.commit()
            flash('{} section of topic "{}" was updated by {}.'
                  .format(section.title, topic.title, gagn()))
        else:
            flash('There were no changes.')
        session.close()
        return redirect(url_for('viewSection', topic_id=topic_id,
                                section_id=section_id))
    else:
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.close()
        return render_template('editTopicSection0.html', subject=subject(),
                               uname=gagn(), topic=topic, section=section)


# Route for updating a topic section
@app.route('/topics/<int:topic_id>/<int:section_id>/edit/',
           methods=['GET', 'POST'])
def editSection(topic_id, section_id):
    if 'credentials' not in signed_session:
        flash('Please sign in.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))

    if request.method == 'POST':
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        if request.form['title'] != "" or request.form['notes'] != "":
            if request.form['title'] != "":
                section.title = request.form['title']
            if request.form['notes'] != "":
                section.notes = request.form['notes']
            section.editor = gaem()
            session.commit()
            flash('Section "{}" of topic "{}" was updated by {}.'
                  .format(section.title, topic.title, gagn()))
        else:
            flash('There were no changes.')
        session.close()
        return redirect(url_for('viewSection', topic_id=topic_id,
                                section_id=section_id))
    else:
        session = DBSession()
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.close()
        return render_template('editSection.html', subject=subject(),
                               uname=gagn(), topic=topic, section=section)


# Route for deleting a topic section
@app.route('/topics/<int:topic_id>/<int:section_id>/delete/',
           methods=['GET', 'POST'])
def deleteSection(topic_id, section_id):
    if 'credentials' not in signed_session:
        flash('Please sign in.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))
    if section_id % maxSectionsPerTopic() == 0:
        flash('Procedure to delete first section of topic not defined.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))

    if request.method == 'POST':
        session = DBSession()  # open session
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.delete(section)
        session.commit()
        # At this point, section is not tied to a session and can be employed
        # outside the session, however, topic is tied to the session. Thus,
        # flash message is generated prior to session.close(). Note that
        # session.close() is not needed after session.commit(), though, kept
        # here for clarity.
        flash('Section "{}" was deleted from topic "{}" by {}.'
              .format(section.title, topic.title, gagn()))

        # Close any gaps in the set of section ids of this topic so that this
        # set comprises an arithmetic sequence of integers with common
        # difference of 1. Begin by checking whether there are more than 1
        # sections of the topic since there is always a first section.
        if session.query(Section).filter_by(topic_id=topic_id).count() > 1:
            lastTopicSec_id = session.query(Section).\
                filter_by(topic_id=topic_id).\
                order_by(Section.id.desc()).first().id
            if section_id < lastTopicSec_id:
                first = section_id + 1
                upper = lastTopicSec_id + 1
                for index in range(first, upper):
                    section = session.query(Section).filter_by(id=index).one()
                    section.id = index - 1
                    session.commit()

        session.close()
        return redirect(url_for('topicContents', topic_id=topic_id))
    else:
        session = DBSession()  # open session
        topic = session.query(Topic).filter_by(id=topic_id).one()
        section = session.query(Section).filter_by(id=section_id).one()
        session.close()
        return render_template('deleteSection.html', subject=subject(),
                               uname=gagn(), topic=topic, section=section)


# Route for viewing a topic section in JSON -- Section JSON API endpoint
@app.route('/topics/<int:topic_id>/<int:section_id>/JSON')
def sectionJSON(topic_id, section_id):
    if 'credentials' not in signed_session:
        flash('Please sign in.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))
    session = DBSession()
    section = session.query(Section).filter_by(id=section_id).one()
    session.close()
    return jsonify(section.serialize)


# Route for viewing a topic's sections in JSON -- Topic JSON API endpoint
@app.route('/topics/<int:topic_id>/JSON')
def topicJSON(topic_id):
    if 'credentials' not in signed_session:
        flash('Please sign in.')
        if request.referrer is not None:
            return redirect(request.referrer)
        else:
            return redirect(url_for('contents'))
    session = DBSession()
    sections = session.query(Section).filter_by(topic_id=topic_id).\
        order_by(Section.id).all()
    sectionsArrOfDicts = []
    for section in sections:
        sectionsArrOfDicts.append(section.serialize)
    topic = session.query(Topic).filter_by(id=topic_id).one()
    topicDict = topic.serialize
    topicDict.update({'k3 sections': sectionsArrOfDicts})
    session.close()
    return jsonify(topicDict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
