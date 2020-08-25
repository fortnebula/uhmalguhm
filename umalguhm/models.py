"""This module defines the database structure for the application"""
from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    """This class sets up a table for user accounts"""
    __tablename__= "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __init__(self, username=None, password=None, role='member'):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        """Return the username"""
        return '<User %r>' % self.username
