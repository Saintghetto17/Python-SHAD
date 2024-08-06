from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .base import Base


class Debt(Base):  # type: ignore
    __tablename__ = 'debts'

    debt_id = Column(Integer, primary_key=True)
    # TODO: fix me
