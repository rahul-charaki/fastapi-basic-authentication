from fastapi import APIRouter,status, Depends
from app import database, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.repository import user
from typing import List

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


get_db = database.get_db

@router.post('/create')
def create_user(request: schemas.NewUser, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get('/all', response_model=List[schemas.ShowUser])
def allUsers(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_all(db)

@router.get('/active', response_model=List[schemas.ShowUser])
def activeUsers(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get(db)

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.update( id, request, db, current_user)


@router.delete('/remove/{id}', status_code=status.HTTP_202_ACCEPTED)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.updateToDelete(id, db, current_user)

# write sample api to list 1 to 10 numbers
@router.get('/list', tags=['Users'])
def list_numbers():
    return list(range(1, 11))