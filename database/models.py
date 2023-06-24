from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# User Account Model
class UserAccount(Base):
    __tablename__ = "user_accounts"

    account_id = Column(Integer, primary_key=True, index=True) # Account ID
    username = Column(String, unique=True, index=True)
    user_email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    account_type = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    phone = Column(String)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(String)
    updated_at = Column(String)

    # Relationship
    transactions = relationship("Transaction", back_populates="user_account")

# Transaction Model
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True) # Transaction ID
    user_account_id = Column(Integer, ForeignKey("user_accounts.account_id")) # Account ID
    transaction_type = Column(String)
    amount = Column(Integer)
    currency = Column(String)
    transaction_status = Column(String)
    transaction_timestamp = Column(String)
    transaction_description = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

    # Relationship
    user_account = relationship("UserAccount", back_populates="transactions")