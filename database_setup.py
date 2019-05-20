from datetime import datetime
from os import environ
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

Base = declarative_base()


# The Subject Notes app employs the following terms to label its contents in
# hierarchical order: subject, topic, section and note. A note is some string
# literal or component thereof, defined by the user. A section comprises one or
# more notes. A topic comprises one or more sections. And the subject comprises
# one or more topics.


# Subject of notes
#   Return the subject of the notes as a string. This string is not defined in
# the database since, by design, the app supports only one subject. Also, this
# literal is not needed in the SQL processing of the database.
def subject():
    return "Deep Learning"


# Topic of the subject
# * There must be at least one topic.
# * The number of Sections a Topic has ranges from 1 to maxSectionsPerTopic().
class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'k1 id': self.id,
            'k2 topic': self.title
        }


# Editor
# * An editor is any authenticated user.
# * There must be at least one editor.
class Editor(Base):
    __tablename__ = 'editor'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)


# Max number of Sections a Topic can have
#   For development and testing purposes the max number of sections per topic
# is set to a relatively small number. 10 is employed as a convenient number.
# With this limit, each topic's first section's id can be conveniently set to
# an integer ending with 0. Generally, the first section's id is num where
# num % nMaxSecs == 0.
def maxSectionsPerTopic():
    return 10


# Default value for edit Coordinated Universal Time (UTC)
#   When initalized, a section's edit UTC equals its initial UTC. SQLAlchemy
# requires this kind of method to set the default value of one column to that
# of another.
def utceDefault(context):
    return context.get_current_parameters()['utci']


# Section of a Topic
# * By app design, each topic must have at least one section assigned to it.
# * The id of the first Section of a Topic is constrained by:
#     first_topic_section.id % maxSectionsPerTopic() == 0
# * The id of the last Section of a Topic is constrained by:
#     last_topic_section.id < first_topic_section.id + maxSectionsPerTopic()
# * The initiator_id is the id of the editor who started the section.
# * utci is the UTC time when the initiator started the Section.
# * The editor_id is the id of the editor who last edited the section.
# * utce is the UTC time when the editor last edited the Section.
# * The datetime objects assigned to utci and utce do not contain timezone
#     information. Since the function employed to generate them, utcnow,
#     outputs its time in UTC, utci and utce are in the UTC timezone.
class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    notes = Column(String(800))
    utci = Column(DateTime, default=datetime.utcnow, nullable=False)
    utce = Column(DateTime, default=utceDefault)
    topic_id = Column(Integer, ForeignKey('topic.id'), nullable=False)
    editor_id = Column(Integer, ForeignKey('editor.id'), default=1,
                       nullable=False)
    topic = relationship(Topic)
    editor = relationship(Editor)

    @property
    def serialize(self):
        return {
            'k1 id': self.id,
            'k2 section': self.title,
            'k3 notes': self.notes,
            'k4 topic id': self.topic_id,
            'k5 editor id': self.editor_id
        }


if environ.get('DATABASE_URL') is None:
    engine = create_engine('postgresql:///deeplearning')
else:
    engine = create_engine(environ.get('DATABASE_URL'))

Base.metadata.create_all(engine)
# EOF
