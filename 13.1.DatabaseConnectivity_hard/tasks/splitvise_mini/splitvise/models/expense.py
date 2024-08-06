from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .base import Base


class Expense(Base):  # type: ignore
    __tablename__ = 'expenses'

    # TODO: fix me