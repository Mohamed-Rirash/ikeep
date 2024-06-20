from app.config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import User

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    web_name = Column(String(150))
    url = Column(String(150))
    email = Column(String(255))
    password = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))  # Corrected here

    user = relationship("User", back_populates="account")
