from fastapi import FastAPI
from database import engine, Base
from routes import auth_routes, blog_routes,comment_routes, tags_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

# include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(blog_routes.router, prefix="/posts", tags=["Post"])
app.include_router(comment_routes.router, prefix="/comments", tags=["Comments"])
app.include_router(tags_routes.router, prefix="/tags", tags=["Tags"])


