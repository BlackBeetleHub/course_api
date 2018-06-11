from flask_login._compat import unicode

from database import Base
from sqlalchemy import String, Integer, Column, Float


class User(Base):
    __tablename__ = 'user'

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "{}".format(self.id_name)


class Point(Base):
    __tablename__ = 'point'

    def __init__(self, id_path,  lat, lng):
        self.id_path = id_path
        self.lat = lat
        self.lng = lng

    id = Column(Integer, primary_key=True)
    id_path = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)

    def __repr__(self):
        return "{}".format(self.id)


class Path(Base):
    __tablename__ = 'path'

    def __init__(self, id_user, name):
        self.name = name
        self.id_user = id_user

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    id_user = Column(Integer)

    def __repr__(self):
        return "{}".format(self.name)
