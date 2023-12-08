from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # So this would create a prop. for our post so when we create a post it shows a owner prop.
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    id = Column(Integer, primary_key=True, nullable=False)
    phone_number = Column(String)



###Model for our Vote table

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)

    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)

