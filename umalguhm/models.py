from sqlalchemy import Column, Integer, String
from .db import Base
from passlib.hash import sha256_crypt

class PassGen():
    def cryptpass(password):
        secure_password = sha256_crypt.hash(password)
        return secure_password

    def decryptpass(password, hash):
        verify_password = sha256_crypt.verify(password, hash)
        return verify_password

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __init__(self, username=None, password=None, role='member'):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username
#db.session.add(User(name="Flask", email="example@example.com"))
#db.session.commit()

#users = User.query.all()