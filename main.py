from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, get_db
from auth import create_access_token, verify_password, get_current_user
from schemas import UserLogin
from routers import users, chat
from fastapi.security import OAuth2PasswordRequestForm
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "ChatterBox API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login")
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    import models as m
    user = db.query(m.User).filter(m.User.email == credentials.username).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(credentials.password, user.password):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
@app.get("/chat", response_class=HTMLResponse)
def chat_page():
    with open("test_chat.html") as f:
        return f.read()