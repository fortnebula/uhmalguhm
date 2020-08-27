"""This module defines the database structure for the application"""
from sqlalchemy import Column, Integer, String
from db.database import Base, GUID
import uuid

class Docker(Base):
    """This class sets up a table for user accounts"""
    __tablename__ = "dockers"
    id = Column(GUID, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True, nullable=False)
    base_image = Column(String, nullable=False)

    def __init__(self, username=None, password=None, role='member'):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.username = username
        self.password = sha256_crypt.hash(password)
        self.role = role

    def __repr__(self):
        """Return the username"""
        return '<User %r>' % self.username
