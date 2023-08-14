from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base, engine


# Candidates SQL Table, currently anyone can add a new candidate but only candidate can delete their row
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    
    # Number of votes each candidate has
    votes = Column(Integer, default=0, nullable=False)
    owner = relationship("User")


# Users SQL Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


# Votes SQL Table
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    candidate_id = Column(Integer, ForeignKey(
        "candidates.id", ondelete="CASCADE"), primary_key=True)
    
Base.metadata.create_all(bind=engine)
