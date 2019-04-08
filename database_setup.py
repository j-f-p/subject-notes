from datetime import datetime
from os import environ
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

Base = declarative_base()


# Main subject of notes
#   Return the subject of the notes as a string. This string is not defined in
#   the database since, by design, the app supports only one subject. Also,
#   this literal is not needed in the SQL processing of the database.
def subject():
    return "Deep Learning"


# Topic of the Subject
#   The number of Sections a Topic has ranges from 1 to maxSectionsPerTopic().
#   There must be one Section assigned to a Topic.
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


# Max number of Sections a Topic can have
#   For development and testing purposes the max number of sections per topic
# is set to a relatively small number. 10 is employed as a convenient number.
# With this limit, each topic's first section's id can be conveniently set to
# an integer ending with 0. Generally, the first section's id is num where
# num % nMaxSecs == 0.
def maxSectionsPerTopic():
    return 10


# Section of a Topic
# * The id of the first Section of a Topic is constrained by:
#     first_topic_section.id % maxSectionsPerTopic() == 0
# * The id of the last Section of a Topic is constrained by:
#     last_topic_section.id < first_topic_section.id + maxSectionsPerTopic()
# * The initiator property is a string that holds the email address of the
#     person who started the section.
# * utci is the UTC time when the initiator started the Section.
# * The editor property is a string that holds the email address of the person
#     who last edited the section.
# * utce is the UTC time when the editor last edited the Section.
# * The datetime objects assigned to utci and utce do not contain timezone
#   information. Since the function employed to generate them, utcnow,
#   outputs its time in UTC, utci and utce are in the UTC timezone.
class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    notes = Column(String(800))
    initiator = Column(
        String(50), nullable=False, default="emailreel@gmail.com")
    utci = Column(DateTime, default=datetime.utcnow, nullable=False)
    editor = Column(String(50))
    utce = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship(Topic)

    @property
    def serialize(self):
        return {
            'k1 id': self.id,
            'k2 section': self.title,
            'k3 notes': self.notes,
            'k4 topic id': self.topic_id
        }


if environ.get('DATABASE_URL') is None:
    engine = create_engine('postgresql:///deeplearning')
else:
    engine = create_engine(environ.get('DATABASE_URL'))

Base.metadata.create_all(engine)
# EOF
