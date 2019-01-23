#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Topic, Section

engine = create_engine('sqlite:///deepLearningNotes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Deep Learning Topics
session.add_all([Topic(name="Historical Trends"),
                 Topic(name="Linear Algebra"),
                 Topic(name="Probability"),
                 Topic(name="Numerical Computation"),
                 Topic(name="Learning Algorithms")])
session.commit()

# Sections of Topics (Subtopics)
session.add_all([Section(name="Changing Names", topic_id=1),
                 Section(name="Increasing Data Set", topic_id=1),
                 Section(name="Increasing Model Size", topic_id=1),
                 Section(name="Increasing Accuracy", topic_id=1),
                 Section(name="Variables", topic_id=2),
                 Section(name="Operations", topic_id=2),
                 Section(name="Linear Dependence", topic_id=2),
                 Section(name="Random Variables", topic_id=3),
                 Section(name="Distributions", topic_id=3),
                 Section(name="Probability Types", topic_id=3),
                 Section(name="Numerical Error", topic_id=4),
                 Section(name="Conditioning", topic_id=4),
                 Section(name="The Task", topic_id=5),
                 Section(name="Performance Measure", topic_id=5),
                 Section(name="Experience", topic_id=5)])
session.commit()

topics = session.query(Topic).all()
for topic in topics:
    print("{} {}".format(topic.id, topic.name))
    sections = session.query(Section).filter_by(topic_id=topic.id)
    for section in sections:
        print("\t{} {}".format(section.id, section.name))

session.close()
