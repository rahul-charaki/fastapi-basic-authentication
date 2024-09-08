from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import user, authentication
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html = True), name="static")

origins = [
    "http://localhost",
    "http://127.0.0.1",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)