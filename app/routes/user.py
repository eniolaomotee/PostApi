from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas, utils
from sqlalchemy.orm import Session
from .. database import  get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#Get all users 
@router.get('/', response_model=List[schemas.UserOut])
def get_all_user(db:Session=Depends(get_db)):
    all_user = db.query(models.User).all()

    return all_user

    


# Create new User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password
    hashed_password = utils.hash(user.password)

    user.password= hashed_password


    new_user = models.User(**user.dict())

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# Get User by id
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exit")
    return user
