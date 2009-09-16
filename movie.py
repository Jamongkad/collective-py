import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker, backref, relation, join

Base = declarative_base()

class Raters(Base):

    __tablename__ = 'raters'
    __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column('id', Integer(10), primary_key=True)
    name = Column('name', String(125))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Rater('%s')>" % self.name

class Movie(Base):
 
    __tablename__ = 'movie' 
    __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column('id', Integer(10), primary_key=True)
    movie_name = Column('movie_name', String(125))

    def __init__(self, movie_name):
        self.movie_name = movie_name

    def __repr__(self):
        return "<Movie('%s')>" % self.movie_name

class RatersPreference(Base):

    __tablename__ = 'raters_preference'
    __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column('id', Integer(10), primary_key=True)
    rater_id = Column('rater_id', Integer(10), ForeignKey('raters.id'))
    movie_id = Column('movie_id', Integer(10), ForeignKey('movie.id'))

    def __init__(self, rater_id, movie_id):
        self.rater_id = rater_id
        self.movie_id = movie_id

class Rating(Base):

    __tablename__ = 'rating'
    __table_args__ = {'mysql_engine':'InnoDB'}
 
    id = Column('id', Integer(10), primary_key=True)
    rater_id = Column('rater_id', Integer(10), ForeignKey('raters.id'))
    movie_id = Column('movie_id', Integer(10), ForeignKey('movie.id'))
    rating = Column('rating', Numeric(precision=8, scale=2))

    def __init__(self, rater_id, movie_id, rating):
        self.rater_id = rater_id
        self.movie_id = movie_id
        self.rating = rating

    def __repr__(self):
        return "<Rating('%d', '%d', '%s')>" % (self.rater_id, self.movie_id, self.rating)

class UserRole(Base):

    __tablename__ = 'user_role'
    __table_args__ = {'mysql_engine':'InnoDB'}
 
    id = Column('id', Integer(10), primary_key=True)
    rater_id = Column('rater_id', Integer(10), ForeignKey('raters.id'))
    role_id = Column('role_id', Integer(10), ForeignKey('role.id'))

    def __init__(self, rater_id, role_id):
        self.rater_id = rater_id
        self.role_id = role_id


class Role(Base):

    __tablename__ = 'role'
    __table_args__ = {'mysql_engine':'InnoDB'}

    id = Column('id', Integer(10), primary_key=True)
    role_name = Column('role_name', String(125)) 
    role_desc = Column('role_desc', Text())

    def __init__(self, role_name, role_desc):
        self.role_name = role_name
        self.role_desc = role_desc

engine = create_engine('mysql://root:p455w0rd@localhost/movie_db')

Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)()
