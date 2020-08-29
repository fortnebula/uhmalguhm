"""This module defines the database structure for the application"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from db.database import BaseModel, GUID


class User(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "users"
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    containers = relationship('Container', backref='user', lazy=True)

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


class Container(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "containers"
    user_id = Column(GUID(), ForeignKey('users.uuid'))
    docker_image = Column(String, nullable=False)
    docker_tag = Column(String, nullable=False)
    status = Column(String, nullable=False)

    def __init__(self, user_id=None, docker_image=None,
                 docker_tag=None, status=None):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.user_id = user_id
        self.docker_image = docker_image
        self.docker_tag = docker_tag
        self.status = status

    def __repr__(self):
        """Return the username"""
        return '<Container_ID %r>' % self.uuid
