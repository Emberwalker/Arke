import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, Sequence, Integer, String, Boolean, ForeignKey

from settings import DB_URL
from arke import DEBUG
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


def get_user(uname):
    session = Session()
    try:
        user = session.query(User).filter_by(username=uname).one()
        return user
    except MultipleResultsFound as mrf:
        logging.error("Found multiple users for name {} ({})".format(uname, mrf))
    except NoResultFound:
        pass  # Ignore.
    return None


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


class Choice(Base):
    __tablename__ = 'choice'

    id = Column(Integer, Sequence('choice_id_seq'), primary_key=True)
    text = Column(String(128), nullable=False)
    vote_id = Column(Integer, ForeignKey('vote.id'), nullable=False)

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


# DB creation (must be LAST in file!)
Base.metadata.create_all(engine)
__setup_category()
