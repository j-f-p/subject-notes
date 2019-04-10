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

### III. Public Views and Navigation

#### User Story
As a visitor, I want to navigate to any section so that I can view it.

<ol>
  <li> Acceptance Criteria to Fulfill User Story
    <ul>
      <li>
        The subject contents view, has an area which lists the last several added or updated sections.
      </li>
      <li>
        In the subject contents view, there is a navigation area for topics.
      </li>
      <li>
        Selecting a topic opens the topic contents view with a second level navigation area for sections.
      </li>
      <li>
        The initial topic contents view has an area which shows the first section of the topic. This can be something like an abstract, intro, objective or preview.
      </li>
    </ul>
  </li><br>
  <li> User Flows Designed to Fulfill User Story
    <ul>
      <li> A visitor navigates to a topic, and there, immediately observes the first section of the topic. User flow steps:
        <ol>
          <li>
            A visitor opens the website app. On the landing page, the subject contents has a list of topics and appears in an area on the side of the page. That acts as natural navigator.
          </li>
          <li>
            The visitor hovers over the topics and observes that they appear selectable.
          </li>
          <li>
            The visitor clicks on a topic and the topic contents view is opened. The topic contents has a similar list of sections, acting as a navigation area. The topic contents page also has an area that shows the first section of the topic, including that section's notes.
          </li>
        </ol>
      </li><br>
      <li> A visitor navigates to a section through a topic. User flow steps:
        <ol>
          <li>
            A visitor opens the website app. On the landing page, the subject contents has a list of topics and appears in an area on the side of the page. That acts as natural navigator.
          </li>
          <li>
            The visitor hovers over the topics and observes that they appear selectable.
          </li>
          <li>
            The visitor clicks on a topic and the topic contents view is opened. The topic contents has a similar list of sections, acting as a navigation area.
          </li>
          <li>
            The visitor clicks on a section and the section view is opened. The section view contains the notes for the section.
          </li>
        </ol>
      </li><br>
      <li> A visitor navigates to a section through the list of latest several added or updated sections. User flow steps:
        <ol>
          <li>
            A visitor opens the website app. On the landing page, there is an area with a list of the latest added or updated sections.
          </li>
          <li>
            The visitor hovers over the list of latest sections and observes that they appear selectable.
          </li>
          <li>
            The visitor clicks on one of the latest sections and the associated section view is opened. The section view contains the notes for the section.
          </li>
        </ol>
      </li>
    </ul>
  </li>
</ol>

### IV. Authentication
Each public view will have a sign-in button on the upper right corner of the page.  Clicking the sign-in button will open the sign-in desk. The sign-in desk will have options for signing in. For this project submission there is only the option of signing in through Google.

For signing in through Google, the app employs [Google's AOuth 2.0 APIs](https://developers.google.com/identity/protocols/OpenIDConnect) for authentication. This authentication is implemented according to Google's [web server app authentication sequence][1]. The implementation employs Google's Python authentication library [web server implementation][2]. It employs [the Google AOuth2 API](https://developers.google.com/api-client-library/python/apis/oauth2/v2) for accessing a user's Google profile and email.

### V. Contributor Views and Navigation
Contributor views and their associated navigation will be the same as the public views with the addition of extra buttons for adding, updating and deleting sections, and for viewing JSON endpoints.

### VI. Contributor Actions
As a visitor, any attempt to reach a new, edit or delete form via URL entry will be thwarted and an adequate flash notice is displayed.

#### A. User Story for Creating a Section
As a contributor, I want to add a topic section.<br>
<ol>
  Acceptance Criteria to Fulfill User Story
    <ul>
      <li>
        If the number of sections is less than the maximum allowed for a topic, the topic contents view will have an add-section button. Otherwise, there is no add-section button and an attempt to reach the add-section form via URL entry will be thwarted and an adequate flash notice is displayed.
      </li>
      <li>
        The add-section button is clearly labelled and in the view pane containing the list of sections of the topic.
      </li>
      <li>
        Clicking the add-section button opens a view with a form for adding a section to the topic.
      </li>
      <li>
        The add-section form has fields for defining the section's title and notes.
      </li>
      <li>
        The add-section form has buttons for submitting the new section or cancelling the submission.
      </li>
    </ul>
</ol>

#### B. User Story for Updating a Section
As a contributor, I want to edit a topic section.<br>
<ol>
  Acceptance Criteria to Fulfill User Story
    <ul>
      <li>
        The section view, has a clearly labelled button for editing the section.
      </li>
      <li>
        The edit-section button is in the view pane containing the section content.
      </li>
      <li>
        Clicking the edit-section button opens a view with a form for editing a section.
      </li>
      <li>
        The edit-section form has fields for editing the section's title and notes. Each field will have its associated current content as a placeholder.
      </li>
      <li>
        The edit-section form has buttons for submitting the edit or cancelling it.
      </li>
    </ul>
</ol>

#### C. User Story for Deleting a Section
As a contributor, I want to remove a topic section.<br>
<ol>
  Acceptance Criteria to Fulfill User Story
    <ul>
      <li>
        The section view, has a clearly labelled button for deleting the section.
      </li>
      <li>
        The delete-section button is in the view pane containing the section content and well separated from any other buttons.
      </li>
      <li>
        Clicking the delete-section button opens a view with buttons for confirming or cancelling the deletion of a section.
      </li>
      <li>
        The buttons for confirming or cancelling a deletion are well separated.
      </li>
    </ul>
</ol>

#### D. User Story for Editing a Topic's First Section Notes
As a contributor, I can edit a topic's first section notes.<br>
<ol>
  Acceptance Criteria to Fulfill User Story
    <ul>
      <li>
        The topic contents view has a clearly labelled button for editing the topic's first section notes.
      </li>
      <li>
        Clicking the edit-notes button opens a view with a form for editing the notes.
      </li>
      <li>
        The edit-notes form has fields for editing the section's notes. The field has its associated current content as a placeholder.
      </li>
      <li>
        The edit-notes form has buttons for submitting the edit or cancelling it.
      </li>
    </ul>
</ol>

Any attempt to reach a delete form for the first section of a topic through URL entry will be thwarted and an adequate flash notice is displayed. This section limitation was motivated by a potential future version of the app involving a third level user.

### VII. JSON API Endpoints
Routes exist for viewing a section in JSON and a topic in JSON. These routes are available for authenticated users. Any attempt to reach a JSON endpoint as a visitor is thwarted and an adequate flash notice is displayed. For exhibition purposes, their is a "topic json" button in each topic contents view and a "section json" button in each section view; in addition, the JSON is formatted for human readability.
