"""This module defines the database structure for the application"""
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from db.database import BaseModel, GUID


class Container(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "containers"
    user_id = Column(GUID(), ForeignKey('users.id'))
    name = Column(String, nullable=False)
    base_image = Column(String)
    user_image = Column(String)
    git_repo = Column(String, nullable=False)
    image = Column(String)

    def __init__(self, user_id=None, name=None, git_repo=None):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.user_id = user_id
        self.name = name
        self.git_repo = git_repo

    def __repr__(self):
        """Return the username"""
        return '<Name %r>' % self.name