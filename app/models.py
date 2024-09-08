from sqlalchemy import Boolean, Column,  Integer, String, ForeignKey, DateTime
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String(32), unique=True)
    password = Column(String(32))
    created_by = Column(Integer, ForeignKey('users.id'))
    created_date = Column(DateTime)
    updated_by = Column(Integer, ForeignKey('users.id'))
    updated_date = Column(DateTime)
    is_active = Column(Boolean)


