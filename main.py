from fastapi import FastAPI
from database import engine, Base
from routes.auth_routes import router as auth_router



app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])