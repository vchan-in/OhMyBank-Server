from pydantic import BaseModel

# Model for User Account
class UserAccount(BaseModel):
    account_id: int
    username: str
    user_email: str
    hashed_password: str
    account_type: str
    balance: float
    currency: str
    phone: str
    address: str
    is_active: bool
    is_admin: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Model for User Account Creation
class UserAccountCreate(BaseModel):
    account_id: int
    username: str
    user_email: str
    password: str
    account_type: str
    currency: str
    phone: str
    address: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

# Model for Transaction
class Transaction(BaseModel):
    transaction_id: int
    user_account_id: int
    transaction_type: str
    amount: float
    currency: str
    transaction_status: str
    transaction_timestamp: str
    transaction_description: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Model for Transaction Creation
class TransactionCreate(BaseModel):
    transaction_id: int
    user_account_id: int
    transaction_type: str
    amount: float
    currency: str
    transaction_status: str
    transaction_timestamp: str
    transaction_description: str

    class Config:
        orm_mode = True

# Model for Account Balance
class AccountBalance(BaseModel):
    account_id: int
    balance: float
    currency: str

    class Config:
        orm_mode = True

# Model to deposit funds into an account
class DepositFunds(BaseModel):
    account_id: int
    amount: float
    currency: str

    class Config:
        orm_mode = True

# Model to withdraw funds from an account
class WithdrawFunds(BaseModel):
    account_id: int
    amount: float
    currency: str

    class Config:
        orm_mode = True

# Model to transfer funds from one account to another
class TransferFunds(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
    currency: str

    class Config:
        orm_mode = True

# Model to get all transactions for an account
class AllTransactions(BaseModel):
    account_id: int

    class Config:
        orm_mode = True