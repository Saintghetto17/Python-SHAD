from sqlalchemy import Integer, Column, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .base import Base


class Summary(Base):  # type: ignore
    __tablename__ = 'summaries'

    # TODO: fix me
