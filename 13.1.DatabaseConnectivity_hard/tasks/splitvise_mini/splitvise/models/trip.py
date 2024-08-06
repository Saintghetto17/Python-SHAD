import datetime

from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


UserTrip = Table(
    'users_trips', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('trip_id', ForeignKey('trips.trip_id'), primary_key=True)
)


class Trip(Base):  # type: ignore
    __tablename__ = 'trips'

    trip_id = Column(Integer, primary_key=True)
    # TODO: fix me

    # Relations
    users = relationship('User', secondary=UserTrip, back_populates='trips')
