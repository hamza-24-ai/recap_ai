from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from app.models.user import User
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime,timedelta
import os

# Import from env file 
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
EXCESS_TOKEN_EXPIRE = int(os.getenv("EXCESS_TOKEN_EXPIRE"))
# ////////////////////////////////////////////////////////////////////////

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Create Logic about signUp and signIn
def password_hashed(password : str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def create_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXCESS_TOKEN_EXPIRE)
    to_encode.update({
        "exp" : expire
    })
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user (
        token : str = Depends(oauth_schema),
        db : Session = Depends(get_db)
):
    exception_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Inavlid Token",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id :int = payload.get("sub")
        if user_id is None:
            raise exception_error
        
    except JWTError:
        raise exception_error
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise exception_error
    return user