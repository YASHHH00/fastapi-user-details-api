from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ✅ Root route to fix 404
@app.get("/")
def read_root():
    return {"message": "FastAPI deployment successful on Render!"}

# ✅ Example POST route (change as per your app logic)
class User(BaseModel):
    name: str
    email: str

@app.post("/user")
def create_user(user: User):
    return {"name": user.name, "email": user.email}
