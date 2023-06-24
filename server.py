import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    response = {
        "status_code": 200,
        "status": "success",
        "details": "Welcome to the OhMyBank API",
    }
    return response

'''
# Create Account API
POST /api/v2/accounts

Request
{
  "username": "vaishno",
  "user_email":"vaishno@example.com"
  "password":"qwerty"
  "account_type": "savings",
  "balance": 1000.00,
  "currency": "usd",
  "account_role": "user",
  "phone": "+1234567890",
  "address": "123 Main St, City, Country",
}

Response
{
  status: "success",
  data: {
        "account_id": "987654321",
        "username": "vaishno",
        "account_type": "savings",
        "balance": 1000.00,
        "currency": "USD",
        "created_at": "2023-06-24T10:30:00Z"
    }
}
'''
@app.post("/api/v2/accounts")
async def create_account(account: schemas.UserAccountCreate, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_username_and_password(db, account.username, account.password)
    if db_account:
        return HTTPException(status_code=400, detail="Username already registered")
    
    try:
        crud.create_account(db=db, account=account)
        response = {
            "status_code": 200,
            "status": "success",
            "details": "Account created successfully",
        }
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)