from os import environ
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Topic, Editor, Section


if environ.get('DATABASE_URL') is None:
    engine = create_engine('postgresql:///deeplearning')
else:
    engine = create_engine(environ.get('DATABASE_URL'))

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# The Initial Editors
session.add_all([Editor(email="alter_ego@example.com"),  # default editor
                 Editor(email="emailreel@gmail.com")])

# Deep Learning Topics
session.add_all([Topic(title="Historical Trends"),
                 Topic(title="Linear Algebra"),
                 Topic(title="Probability"),
                 Topic(title="Numerical Computation"),
                 Topic(title="Learning Algorithms")])
session.commit()

# Sections of Topics (Subtopics)
#   Each topic has: something like an intro section and an upper limit to the
#     number of its sections.
#   Every section is stored in one database table.
#   The id of the initial section of a topic is constrained.
#   The default primary key sequencing in postgresql requires every section's
#     primary key to be manually defined upon section initialization.
#   Thus, a section's id is manually defined and the number of sections
#     initialized for each topic is limited.
session.add_all([
    Section(id=10, title="Intro", topic_id=1, editor_id=2),
    Section(id=11,   title="Changing Names", topic_id=1, editor_id=2),
    Section(id=12,   title="Increasing Data Set", topic_id=1, editor_id=2),
    Section(id=13,   title="Increasing Model Size", topic_id=1, editor_id=2),
    Section(id=14,   title="Increasing Accuracy", topic_id=1, editor_id=2),
    Section(id=20, title="Intro", topic_id=2),
    Section(id=21,   title="Variables", topic_id=2, editor_id=2),
    Section(id=22,   title="Operations", topic_id=2, editor_id=2),
    Section(id=23,   title="Linear Dependence", topic_id=2, editor_id=2),
    Section(id=30, title="Intro", topic_id=3),
    Section(id=31,   title="Random Variables", topic_id=3, editor_id=2),
    Section(id=32,   title="Distributions", topic_id=3, editor_id=2),
    Section(id=33,   title="Probability Types", topic_id=3, editor_id=2),
    Section(id=40, title="Intro", topic_id=4),
    Section(id=41,   title="Numerical Error", topic_id=4, editor_id=2),
    Section(id=42,   title="Conditioning", topic_id=4, editor_id=2),
    Section(id=50, title="Intro", topic_id=5),
    Section(id=51,   title="The Task", topic_id=5),
    Section(id=52,   title="Performance Measure", topic_id=5),
    Section(id=53,   title="Experience", topic_id=5)])
# Above, the last section id is 53. The actual number of sections is less.
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
    sizes have continued to increase. Logically, the accuracy of analyses with
    deep learning have continued to improve.'''.split())
section.utce = datetime.utcnow()
session.commit()

section = session.query(Section).filter_by(id=11).one()
section.notes = ' '.join('''
    What we now know as deep learning was introduced as cybernetics circa 1940.
    It began being called connectionism or neural networks circa 1980. The rise
    of the current name began circa 2006.'''.split())
section.utce = datetime.utcnow()
session.commit()

section = session.query(Section).filter_by(id=12).one()
section.notes = ' '.join('''
    Increases in computer memory have resulted in commensurate increases in
    digital data. Larger data sets have enabled deep learning algorithms to be
    applied to increasingly complex applications.'''.split())
section.utce = datetime.utcnow()
session.commit()

section = session.query(Section).filter_by(id=13).one()
section.notes = ' '.join('''
    Increases in computer performance have enabled commensurate increases in
    deep learning model sizes. Specifically, the number of neurons of an
    artificial neural network has doubled about every 2.5 years since their
    inception.  Additionally, the number of connections per model neuron has
    risen.'''.split())
section.utce = datetime.utcnow()
session.commit()

section = session.query(Section).filter_by(id=14).one()
section.notes = ' '.join('''
    Image recognition error rate steadily dropped annually from 28% in 2010 to
    4% in 2015.'''.split())
section.utce = datetime.utcnow()
session.commit()

topics = session.query(Topic).all()
for topic in topics:
    print("{} {}".format(topic.id, topic.title))
    sections = session.query(Section).filter_by(topic_id=topic.id)
    for section in sections:
        print("\t{} {:24} {} UTC".format(section.id, section.title,
              section.utci.strftime('%Y-%m-%d %-I:%M:%S.%f %p')))
# section.utci is not aware of timezone. Thus, '%Z' format would return empty.
# However, it is known to have been generated in UTC. Thus, 'UTC' can be added
# manually.
session.close()
