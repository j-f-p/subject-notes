#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Topic, Section

""" This module contains methods for testing the database. """

engine = create_engine('sqlite:///test.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def addSection(topic_id, newName, newNotes):
    session = DBSession()
    lastTopicSec_id = session.query(Section).\
        filter_by(topic_id=topic_id).order_by(Section.id.desc()).first().id
    new_section = Section(
        name=newName, notes=newNotes, topic_id=topic_id, id=lastTopicSec_id+1)
    session.add(new_section)
    session.commit()
    session.close()
    return


def listSections():
    session = DBSession()
    topics = session.query(Topic).all()
    for topic in topics:
        print("{} {}".format(topic.id, topic.name))
        sections = session.query(Section).filter_by(topic_id=topic.id)
        for section in sections:
            print("\t{} {}".format(section.id, section.name))
    session.close()
    return


def updateSection(topic_id, newName, newNotes):
    session = DBSession()
    topic = session.query(Topic).filter_by(id=topic_id).one()
    section = session.query(Section).filter_by(id=section_id).one()
    section.name = newName
    section.notes = newNotes
    session.add(section)
    session.commit()
    session.close()
    return


def deleteSection(topic_id, section_id):
    session = DBSession()
    topic = session.query(Topic).filter_by(id=topic_id).one()
    section = session.query(Section).filter_by(id=section_id).one()
    session.delete(section)
    session.commit()
    return


def as1wi(name, notes, id):
    session = DBSession()
    new_section = Section(
        name=name, notes=notes, topic_id=1, id=id)
    session.add(new_section)
    session.commit()
    session.close()
    return


def lst1():
    session = DBSession()
    topic = session.query(Topic).first()
    print("{} {}".format(topic.id, topic.name))
    sections = session.query(Section).filter_by(topic_id=topic.id)
    for section in sections:
        print("\t{} {}".format(section.id, section.name))
    session.close()
    return


def dst1(section_id):
    session = DBSession()
    lastTopicSec_id = session.query(Section).\
        filter_by(topic_id=1).order_by(Section.id.desc()).first().id
    section = session.query(Section).filter_by(id=section_id).one()
    session.delete(section)
    session.commit()
    if section_id < lastTopicSec_id:
        lower = section_id + 1
        upper = lastTopicSec_id + 1
        for index in range(lower, upper):
            section = session.query(Section).filter_by(id=index).one()
            section.id = index - 1
            session.add(section)
            session.commit()
    session.close()
    return


def resetTestData():
    # Pre-condition: Sections have ids within an arithmetic sequence of
    # integers with common difference of 1, with an initial term of 15 and
    # length in {1,2,3,4,5}.
    print('\nSections Prior to Reset')
    lst1()
    session = DBSession()
    lastTopicSec_id = session.query(Section).\
        filter_by(topic_id=1).order_by(Section.id.desc()).first().id
    if lastTopicSec_id > 14:
        numIdsInResetRange = session.query(Section).\
            filter(Section.topic_id == 1, Section.id > 14).count()
        index0 = 15
        upper = index0 + numIdsInResetRange
        for index in range(index0, upper):
            oldSection = session.query(Section).filter_by(id=index).one()
            session.delete(oldSection)
            session.commit()
        print('\n\nSections After Deletion Phase')
        lst1()
        session.add_all([
            Section(name="1950s", notes="Rise of the Cold War....",
                    topic_id=1, id=15),
            Section(name="1960s", notes="The space race....",
                    topic_id=1, id=16),
            Section(name="1970s", notes="The golden age of hippies....",
                    topic_id=1, id=17),
            Section(name="1980s", notes="The golden age of video arcades....",
                    topic_id=1, id=18),
            Section(name="1990s", notes="Rise of the internet....",
                    topic_id=1, id=19),
        ])
        session.commit()
    session.close()
    print('\nSections After Reset')
    lst1()
    return

# idsInResetRangeSingles = session.query(Section).\
#     filter(Section.topic_id==1, Section.id>14).\
#     with_entities(Section.id).all()
# idsInResetRange = []
# for single in idsInResetRangeSingles:
#     idsInResetRange.append(single[0])
#
# resetRangeSections = [
#     Section(name="1950s", notes="Rise of the Cold War....",
#                     topic_id=1, id=15),
#     Section(name="1960s", notes="The space race....",
#                     topic_id=1, id=16),
#     Section(name="1970s", notes="The golden age of hippies....",
#                     topic_id=1, id=17),
#     Section(name="1980s", notes="The golden age of video arcades....",
#                     topic_id=1, id=18),
#     Section(name="1990s", notes="Rise of the internet....",
#                     topic_id=1, id=19),
# ]
# for index in range(numIdsInResetRange):
#     session.add(resetRangeSections[index])
#     session.commit()
#
#     Section(name="2000s", notes="A war against terrorism....",
#                     topic_id=1, id=16),
