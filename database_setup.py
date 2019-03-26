#!/usr/bin/env python3
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


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
#   The id of the first Section of a Topic is constrained by:
#     first_topic_section.id % maxSectionsPerTopic() == 0
#   The id of the last Section of a Topic is constrained by:
#     last_topic_section.id < first_topic_section.id + maxSectionsPerTopic()
#   utc contains the time of initialization or last edit. Though the
#     object itself does not contain timezone information, its time is in UTC.
#   The initiator property is a string that holds the email address of the
#     person who started the section.
#   The editor property is a string that holds the email address of the person
#     who last edited the section.
class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    notes = Column(String(800))
    utc = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    initiator = Column(String(50), nullable=False, default="admin@example.com")
    editor = Column(String(50))
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


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
# EOF
