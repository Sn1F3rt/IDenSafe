from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.mysql import LONGBLOB

from .database import Base


class User(Base):
    __tablename__ = "users"

    address = Column(String(42), primary_key=True, nullable=False)
    username = Column(String(10), unique=True, nullable=True)
    nonce = Column(String(11), nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime, default=datetime.now(UTC), nullable=True)
    kyc_status = Column(Integer, default=0, nullable=False)
    name = Column(String(100), nullable=True)
    name_allowed = Column(Boolean, default=False, nullable=False)
    age = Column(Integer, nullable=True)
    age_allowed = Column(Boolean, default=False, nullable=False)
    location = Column(String(100), nullable=True)
    location_allowed = Column(Boolean, default=False, nullable=False)
    id_number = Column(String(20), nullable=True)
    id_number_allowed = Column(Boolean, default=False, nullable=False)
    id_front = Column(LONGBLOB, nullable=True)
    id_back = Column(LONGBLOB, nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_verified(self):
        return self.verified

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.address

    def __repr__(self):
        return f"<User {self.address}>"
