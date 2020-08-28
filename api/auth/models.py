"""This module defines the database structure for the application"""
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from db.database import BaseModel, GUID


class User(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "users"
    username = Column(String, unique=False, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __init__(self, username=None, password=None, role='member'):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.username = username
        self.password_hash = sha256_crypt.hash(password)
        self.role = role

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)

    def __repr__(self):
        """Return the username"""
        return '<User %r>' % self.username