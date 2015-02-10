import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, Sequence, Integer, String, Boolean, ForeignKey

from settings import DB_URL, DEBUG
from util import trunc

engine = create_engine(DB_URL, echo=DEBUG)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Authentication
class User(Base):
    __tablename__ = 'auth'

    id = Column(Integer, Sequence('auth_id_seq'), primary_key=True)
    username = Column(String(128), nullable=False, index=True, unique=True)
    password = Column(String(128), nullable=False)
    is_superuser = Column(Boolean, nullable=False)

    def __repr__(self):
        return 'User<{}/sudo={}>'.format(self.username, self.is_superuser)


def get_user(id_or_name):
    if id_or_name.isdigit():
        try:
            i = int(id_or_name)
        except:
            return None
        return __get_user_by_id(i)
    else:
        return __get_user_by_name(id_or_name)

def __get_user_by_name(uname):
    session = Session()
    uname = uname.lower()
    user = session.query(User).filter_by(username=uname).scalar()
    session.close()
    return user

def __get_user_by_id(i):
    session = Session()
    user = session.query(User).filter_by(id=i).scalar()
    session.close()
    return user

def has_superuser():
    session = Session()
    u = session.query(User).filter_by(is_superuser=True).count()
    return u > 0


# Core
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(128), nullable=False, index=True, unique=True)

    def __repr__(self):
        return 'Category<{}>'.format(self.name)

def __setup_category():
    session = Session()
    try:
        ct = session.query(Category).filter_by(id=1).one()
    except NoResultFound:
        session.add(Category(id=1, name='Uncategorised'))
        session.commit()
    session.close()


class Vote(Base):
    __tablename__ = 'vote'

    id = Column(Integer, Sequence('vote_id_seq'), primary_key=True)
    question = Column(String(128), nullable=False)
    extended_desc = Column(String(1024), nullable=True)
    submitter_id = Column(Integer, ForeignKey('auth.id'), nullable=False)
    cat_id = Column(Integer, ForeignKey('category.id'), nullable=False, default=1)
    is_open = Column(Boolean, nullable=False)

    submitter = relationship("User", backref=backref('votes', order_by=id))
    category = relationship("Category", backref=backref('votes', order_by=id))

    def __repr__(self):
        return 'Vote<{}/{}>'.format(self.submitter, trunc(self.question, 20))

def get_active_votes():
    session = Session()
    vts = session.query(Vote).filter_by(is_open=True).all()
    return vts


class Choice(Base):
    __tablename__ = 'choice'

    id = Column(Integer, Sequence('choice_id_seq'), primary_key=True)
    text = Column(String(128), nullable=False)
    vote_id = Column(Integer, ForeignKey('vote.id'), nullable=False)
    colour = Column(String(7), nullable=False, default="#848484") # Yes, colour. I am British. Default is grey.

    vote = relationship("Vote", backref=backref('choices', order_by=id))

    def __repr__(self):
        return 'Choice<{}/{}>'.format(self.text, self.vote)


class CastVote(Base):
    __tablename__ = 'cast_vote'

    id = Column(Integer, Sequence('cast_vote_id_seq'), primary_key=True)
    submitter_id = Column(Integer, ForeignKey('auth.id'), nullable=False)
    choice_id = Column(Integer, ForeignKey('choice.id'), nullable=False)

    submitter = relationship("User", backref=backref('choices', order_by=id))
    choice = relationship("Choice", backref=backref('cast_votes', order_by=id))

    def __repr__(self):
        return 'CastVote<{}/{}>'.format(self.choice, self.submitter)


# Helpers
def write_to_db(obj):
    session = Session()
    session.add(obj)
    session.commit()
    session.close()

def delete_from_db(obj):
    session = Session()
    session.delete(obj)
    session.commit()
    session.close()

def get_all(model):
    session = Session()
    stuff = session.query(model).all()
    return stuff

# DB creation (must be LAST in file!)
Base.metadata.create_all(engine)
__setup_category()
