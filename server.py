import uvicorn, datetime
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import get_db, SessionLocal, engine

from auth.schemas import Token as TokenSchema
from auth.auth import authenticate_account, create_access_token, get_expire_time_access_token, get_current_account

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Configure CORS
origins = ["*"]  # Adjust this to allow requests from specific domains

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    response = {
        "status_code": 200,
        "details": "Welcome to the OhMyBank API",
    }
    return response

@app.post("/api/v2/accounts", status_code=201, tags=["accounts"])
async def create_account(account: schemas.UserAccountCreate, db: Session = Depends(get_db)):
    """
    ## Create Account API
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
        "is_active": true
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
    """
    db_account = crud.get_account_by_username_and_password(db, account.username, account.password)
    if db_account:
        return JSONResponse(status_code=400, content={"status_code": 400, "details": "Account already exists"})
    
    try:
        crud.create_account(db=db, account=account)
        response = {
            "status_code": 201,
            "details": "Account created successfully",
            "data": {
                "username": account.username,
                "balance": account.balance,
                "currency": account.currency,
            }
        }
        return response
    except Exception as e:
        return JSONResponse(status_code=400, content={"status_code": 400, "details": str(e)})


@app.post("/api/v2/accounts/login", tags=["accounts"], status_code=200)
async def login_account(account: schemas.UserAccountLogin, db: Session = Depends(get_db), response: Response = None):
    """
    ## Login Account API
    POST /api/v2/accounts/login

    Request
    {
        "username": "vaishno",
        "password":"qwerty"
    }

    Response
    {
        status: "success",
        data: {
                "access_token": access_token,
                "token_type": "bearer"
            }
    }
    """
    db_account = crud.get_account_by_username_and_password(db, account.username, account.password)
    if db_account:
        access_token = create_access_token(data={"sub": db_account.username})
        response = {
            "status_code": 200,
            "details": "Login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
        return response
    else:
        return JSONResponse(status_code=400, content={"status_code": 400, "details": "Invalid credentials"})
    

# Check Life Time of JWT Token
@app.post("/api/v2/accounts/check_token", tags=["accounts"])
async def check_token(token: TokenSchema, db: Session = Depends(get_db)):
    """
    ## Check Token API
    POST /api/v2/accounts/check_token

    Request
    {
        "access_token": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2YWlzaG5vIiwiZXhwIjoxNjg3Njc5MjczfQ.MyrahPWqn5NlofMOT2ldMehU52RRNZQXyym27abulx8,
        "token_type": "bearer",
    }

    Response
    {
        status: "success",
        data: {
                "expire_time": 2023-06-25T13:17:53
            }
    }
    """
    try:
        expire_time = get_expire_time_access_token(token.access_token)
        response = {
            "status_code": 200,
            "details": "Token checked successfully",
            "data": {
                "expire_time": expire_time
            }
        }
        return response
    except Exception as e:
        response.status_code = 400
        return HTTPException(status_code=400, detail=str(e))
    

# Use JWT token for authentication and get current account
@app.get("/api/v2/accounts/me", tags=["accounts"])
async def read_account_me(current_account: schemas.UserAccount = Depends(get_current_account)):
    """
    ## Read Account API
    GET /api/v2/accounts/me

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
    """
    return current_account
    



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)