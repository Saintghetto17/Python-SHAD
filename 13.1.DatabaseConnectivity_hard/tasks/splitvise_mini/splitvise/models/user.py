from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from .base import Base
from .trip import UserTrip


class User(Base):  # type: ignore
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)

    # Relations
    trips = relationship('Trip', secondary=UserTrip, back_populates='users')

    def __repr__(self) -> str:
        return f'<User user_id={self.user_id}, username={self.username}>'
