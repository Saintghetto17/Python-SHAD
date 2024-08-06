import datetime

from sqlalchemy import Integer, Column, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship

from .base import Base


class Event(Base):  # type: ignore
    __tablename__ = 'events'

    # TODO: fix me
