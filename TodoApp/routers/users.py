from typing import Annotated
from ..Todo import UserVerfication, UserPhoneNumber

from fastapi import Depends, HTTPException, APIRouter
from starlette import status

from ..models import Users
from ..database import SesssionLocal
from sqlalchemy.orm import Session

from .auth import get_current_user

from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SesssionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')

    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerfication):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change!")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()

@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, user_phone_number: UserPhoneNumber):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = user_phone_number.phone_number

    db.add(user_model)
    db.commit()