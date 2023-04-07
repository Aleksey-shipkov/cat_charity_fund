from datetime import datetime
from sqlalchemy import Column, Integer, CheckConstraint, Boolean, DateTime


class AbstractMixin:
    full_amount = Column(
        Integer, CheckConstraint("full_amount > 0"), nullable=False
    )
    invested_amount = Column(
        Integer,
        CheckConstraint("invested_amount >= 0"),
        default=0,
        nullable=False,
    )
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    close_date = Column(DateTime)
