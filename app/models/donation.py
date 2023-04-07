from sqlalchemy import Column, Text, Integer, ForeignKey
from app.core.db import Base
from app.models.base import AbstractMixin


class Donation(AbstractMixin, Base):
    user_id = Column(
        Integer, ForeignKey("user.id", name="fk_donation_user_id_user")
    )
    comment = Column(Text)
