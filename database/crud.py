from sqlalchemy.orm import Session

from . import models, schemas
import hashlib, datetime, random

# ----------------- READ OPERATIONS -------------------

# Get all transactions for an account
def get_all_transactions(db: Session, account_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_account_id == account_id).all()

# Get account balance
def get_account_balance(db: Session, account_id: int):
    return db.query(models.UserAccount).filter(models.UserAccount.id == account_id).first()

# Get all accounts
def get_all_accounts(db: Session):
    return db.query(models.UserAccount).all()

# Get account by account ID
def get_account_by_id(db: Session, account_id: int):
    return db.query(models.UserAccount).filter(models.UserAccount.id == account_id).first()

# Get account by username
def get_account_by_username(db: Session, username: str):
    return db.query(models.UserAccount).filter(models.UserAccount.username == username).first()

# Get account by username and password
def get_account_by_username_and_password(db: Session, username: str, password: str):
    return db.query(models.UserAccount).filter(
        models.UserAccount.username == username,
        models.UserAccount.hashed_password == hashlib.md5(password.encode()).hexdigest()).first()


# ----------------- WRITE OPERATIONS -------------------

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"  # ISO 8601 format for datetime

# Create a new account
def create_account(db: Session, account: schemas.UserAccountCreate):
    db_account = models.UserAccount(
        account_id=random.randint(100000000, 999999999), # Generate random 9-digit account ID   # Vuln: Predictable random number generator
        username=account.username,
        user_email=account.user_email,
        hashed_password=hashlib.md5(account.password.encode()).hexdigest(), # Vuln: Weak hashing algorithm
        account_type=account.account_type,
        balance=0.0, # New accounts start with 0 balance
        currency=account.currency,
        phone=account.phone,
        address=account.address,
        is_active=account.is_active,
        is_admin=account.is_admin,
        created_at=datetime.datetime.now().strftime(DATETIME_FORMAT),
        updated_at=datetime.datetime.now().strftime(DATETIME_FORMAT))
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# Create a new transaction
def create_transaction(db: Session, transaction: schemas.TransactionCreate, account_id: int):
    db_transaction = models.Transaction(
        user_account_id=account_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        currency=transaction.currency,
        transaction_status=transaction.transaction_status,
        transaction_timestamp=transaction.transaction_timestamp,
        transaction_description=transaction.transaction_description,
        created_at=datetime.datetime.now().strftime(DATETIME_FORMAT),
        updated_at=datetime.datetime.now().strftime(DATETIME_FORMAT))
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Update account balance
def update_account_balance(db: Session, account_id: int, new_balance: float):
    db_account = db.query(models.UserAccount).filter(models.UserAccount.id == account_id).first()
    db_account.balance = new_balance
    db.commit()
    db.refresh(db_account)
    return db_account

# Update transaction status
def update_transaction_status(db: Session, transaction_id: int, new_status: str):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    db_transaction.transaction_status = new_status
    db.commit()
    db.refresh(db_transaction)
    return db_transaction