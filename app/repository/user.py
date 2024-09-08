from datetime import datetime
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status



def get_all(db: Session):
    users = db.query(models.User).order_by(models.User.created_date.desc()).all()
    return users

def get(db: Session):
    active_users = db.query(models.User).filter(models.User.is_active == True).order_by(models.User.created_date.desc()).all()
    return active_users

def create(request: schemas.NewUser, db: Session):
    print(request)
    exists_user = db.query(models.User).filter(models.User.username == request.username).first()
    # duplicate check code to be implemented
    if exists_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Username {request.username} already exists")
    else:        
        new_user = models.User(
            username=request.username, 
            password=request.password, 
            created_by=1,
            created_date=datetime.now(),
            is_active=1,
        )
        db.add(new_user)
        db.commit()

    return ({"new_user": new_user, "detail": "user_added"})
    

def update(id: int, request: schemas.User, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id)
    exists_user = db.query(models.User).filter(models.User.id != id).filter(models.User.username == request.username).first()
     # duplicate check code to be implemented
    if exists_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"{request.username} already exists")
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    
    user = user.update({'id': id, 'username': request.username,  'is_active': request.is_active}, synchronize_session=False)
    db.commit()
    return ({"updated_user": user, "detail": "user_update"})

def destroy(id: int, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return ({"deleted_user": user, "detail": "user_delete"})