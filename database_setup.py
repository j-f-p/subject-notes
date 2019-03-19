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
    # Each topic must have an intro section.
    # TODO: Add property serialize.


# Max number of sections a topic can have
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
            'name': self.name,
            'description': self.description,
            'id': self.id
        }


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
# EOF
