#!/usr/bin/env python3
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topic'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    # Each topic must have one section.

    @property
    def serialize(self):
        return {
            'k1 topic': self.name,
            'k2 id': self.id
        }


# Max number of sections a topic can have
# For development and testing purposes the max number of sections per topic is
# set to a relatively small number. 10 is employed as a convenient number. With
# this limit, each topic's first section's id can be conveniently set to an
# integer ending with 0, or more generally, num where nMaxSecs % num == 0.
def maxSectionsPerTopic():
    return 10


class Section(Base):
    __tablename__ = 'section'
    name = Column(String(50), nullable=False)
    notes = Column(String(800))
    id = Column(Integer, primary_key=True)
    utc = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship(Topic)

    @property
    def serialize(self):
        return {
            'k1 section': self.name,
            'k2 notes': self.notes,
            'k3 id': self.id,
            'k4 topic id': self.topic_id
        }


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
# EOF
