#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Topic, Section

engine = create_engine('sqlite:///test.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Deep Learning Topics
session.add_all([Topic(name="Historical Trends"),
                 Topic(name="Linear Algebra"),
                 Topic(name="Probability"),
                 Topic(name="Numerical Computation"),
                 Topic(name="Learning Algorithms")])
session.commit()

# Sections of Topics (Subtopics)

# Note that the app assumes each topic has something like an intro section.

# For development and testing purposes the max number of sections is set to a
# relatively small number. 10 is employed as  convenient number. With this
# limit, each topic's first section's id can be conveniently set to an integer
# ending with 0.
session.add_all([Section(name="Intro", topic_id=1, id=10),  # section id = 10
                 Section(name="Changing Names", topic_id=1),
                 Section(name="Increasing Data Set", topic_id=1),
                 Section(name="Increasing Model Size", topic_id=1),
                 Section(name="Increasing Accuracy", topic_id=1),
                 Section(name="Intro", topic_id=2, id=20),  # section id = 20
                 Section(name="Variables", topic_id=2),
                 Section(name="Operations", topic_id=2),
                 Section(name="Linear Dependence", topic_id=2),
                 Section(name="Intro", topic_id=3, id=30),
                 Section(name="Random Variables", topic_id=3),
                 Section(name="Distributions", topic_id=3),
                 Section(name="Probability Types", topic_id=3),
                 Section(name="Intro", topic_id=4, id=40),
                 Section(name="Numerical Error", topic_id=4),
                 Section(name="Conditioning", topic_id=4),
                 Section(name="Intro", topic_id=5, id=50),
                 Section(name="The Task", topic_id=5),
                 Section(name="Performance Measure", topic_id=5),
                 Section(name="Experience", topic_id=5)])  # section id = 53
session.commit()

# Section notes
#   Each string value for notes is built by triple quotes for convenience of
# human readability of the code. The resulting newlines and indent spaces are
# removed by employing the split() and join() methods.
section = session.query(Section).filter_by(id=10).one()
section.notes = ' '.join('''
    There are four salient trends in the history of the study of deep learning.
    Deep learning has been variously labelled in its relatively short history.
    The size of data sets analyzed by deep learning has increased with the
    march of this history. Simultaneously, deep learning mathematical model
    sizes have continued to increase. Logically, the accuracy of this analyses
    have continued to improve.'''.split())
session.add(section)
session.commit()

section = session.query(Section).filter_by(id=11).one()
section.notes = ' '.join('''
    What we now know as deep learning was introduced as cybernetics circa 1940.
    It began being called connectionism or neural networks circa 1980. The rise
    of the current name began circa 2006.'''.split())
session.add(section)
session.commit()

section = session.query(Section).filter_by(id=12).one()
section.notes = ' '.join('''
    Increases in computer memory have resulted in commensurate increases in
    digital data. Larger data sets have enabled deep learning algorithms to be
    applied to increasingly complex applications.'''.split())
session.add(section)
session.commit()

section = session.query(Section).filter_by(id=13).one()
section.notes = ' '.join('''
    Increases in computer performance have enabled commensurate increases in
    deep learning model sizes. Specifically, the number of neurons of an
    artificial neural network has doubled about every 2.5 years since their
    inception.  Additionally, the number of connections per model neuron has
    risen.'''.split())
session.add(section)
session.commit()

section = session.query(Section).filter_by(id=14).one()
section.notes = ' '.join('''
    Image recognition error rate steadily dropped annually from 28% in 2010 to
    4% in 2015.'''.split())
session.add(section)
session.commit()

topics = session.query(Topic).all()
for topic in topics:
    print("{} {}".format(topic.id, topic.name))
    sections = session.query(Section).filter_by(topic_id=topic.id)
    for section in sections:
        print("\t{} {}".format(section.id, section.name))

session.close()
