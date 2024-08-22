from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from bot.models.base import Base


class User(Base):
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
