# Subject Notes
Objective: Udacity Student Project Submission of Item Catalog Project<br>
Developer: JF Padilla<br>
Contact: emailreel@gmail.com

## Description
This project is a web application for collaboratively compiling notes about various topics of a subject. The app is developed with [Flask](http://flask.pocoo.org/) and [Python 3.X syntax](https://en.wikipedia.org/wiki/History_of_Python#Version_3). It has a database managed by [SQLAlchemy](https://www.sqlalchemy.org/) and [PostgreSQL](https://www.postgresql.org/). The app is deployed on the [Heroku](https://www.heroku.com/) platform. The demonstration database involves notes taken from a book about [Deep Learning](http://www.deeplearningbook.org/). This app can authenticate any user with a Google account. Authentication occurs through [Google's AOuth 2.0 APIs](https://developers.google.com/identity/protocols/OpenIDConnect). Authenticated users are able to post, edit and delete notes. Components of this project were inspired by [Udacity](https://www.udacity.com/) courses about web-server app development with Flask. This was the second of three primary projects completed toward achieving the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Design

### I. Data Labels and Organization
This app employs the following terms to label its contents in hierarchical order: subject, topic, section and note. The term "note" is employed to label a written statement. Programmatically, any notes of a section are contained by a single string. A section comprises zero or more notes. A topic comprises one or more sections. The app assumes that every topic in the database has a first section. The term "subject" is employed to label the overall subject of the notes; the entire database is the subject data.

There are two types of sections. The first section of a topic and any other section. The stand alone term "section" refers to any section other than the first section of a topic.

There is a maximum number of sections a topic can have. This number is set to a small value for development purposes. The number of topics and topic properties is fixed from the initial state of the database.

The app subject title is stored as method return value, a string literal, in the source.

### II. Users
For this project submission, there are two kinds of users of the deployed web-server app: visitors and contributors.

* A visitor is any non-authenticated user. They see only the public views of the app.
* A contributor is an authenticated user. They see the authenticated or contributor views of the app. A contributor has authority for the following actions:
  * Add, edit or remove a section, which includes the section's title and notes.
  * Edit the notes of a topic's first section.
  * View topic and section data in JSON.
  * View email of the initiator and last editor of a section or a topic's first section.

### III. Authentication
Each public view has a sign-in button on the upper right corner of the page.  Clicking the sign-in button will open the sign-in desk. The sign-in desk is intended to have multiple options for signing in. For this project submission, there is only the option of signing in through Google.

For signing in through Google, the app employs [Google's AOuth 2.0 APIs](https://developers.google.com/identity/protocols/OpenIDConnect) for authentication. This authentication is implemented according to Google's [web server app authentication sequence][1]. The implementation employs Google's Python authentication library [web server implementation][2]. It employs [the Google AOuth2 API](https://developers.google.com/api-client-library/python/apis/oauth2/v2) for accessing a user's Google profile and email.

## Environment
The environment for developing this project was a modified version of the Linux virtual machine defined by the [Udacity FSND Virtual Machine][3]. It was provisioned by Vagrant 2.2.4 and VirtualBox 6.0. The operating system of the virtual machine was Bento Ubuntu 18.10. The web app was tested on Chrome 73, Firefox 66 and Edge 42. The environment for deploying the project is the [Heroku](https://www.heroku.com/) platform with the Python 3.7.3 runtime and the [Green Unicorn](https://gunicorn.org/) server.

## Execution
Subject Notes is deployed at https://subject-notes.herokuapp.com.

[1]: https://developers.google.com/identity/protocols/OAuth2#webserver
[2]: https://developers.google.com/api-client-library/python/auth/web-app
[3]: https://github.com/udacity/fullstack-nanodegree-vm
