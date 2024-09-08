from fastapi import APIRouter, Depends, status, HTTPException , Response
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, database, models, token, oauth2
from sqlalchemy.orm import Session
from app.repository import user

router = APIRouter(tags=['Authentication'])


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    userLogin = db.query(models.User).filter(
        models.User.username == request.username).filter(models.User.is_active==1).first()
    if not userLogin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    # if not Hash.verify(user.password, request.password):
    if userLogin.password != request.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")

    access_token = token.create_access_token(data={"sub": userLogin.username})
    

    return {"access_token": access_token, "token_type": "bearer", "user": { "username": userLogin.username}}


@router.get("/logout")
async def logout(response: Response, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Also tried following two comment lines
    # response.set_cookie(key="access_token", value="", max_age=1)
    # response.delete_cookie("access_token", domain="localhost")
    response.delete_cookie("access_token")

    user.log_activity(current_user, "User has logged out", db)
    return {"message": "Logged out successfully"}
