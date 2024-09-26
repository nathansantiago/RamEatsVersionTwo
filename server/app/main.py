from fastapi import FastAPI
from routes import users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def health_check():
    return 'Health check complete'