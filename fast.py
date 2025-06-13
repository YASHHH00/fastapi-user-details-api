from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"
engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
class Details(Base):
    __tablename__ = "details"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)
    email = Column(String, unique=True ,index=True)
    is_True = Column(Boolean, default=False)
Base.metadata.create_all(bind = engine)
class detail(BaseModel):
    name: str
    location: str
    email: str
class DetailsResponse(BaseModel):
    id: int
    name: str
    location: str
    email: str
    class Config:
        orm_mode = True
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/details/", response_model=DetailsResponse)
def create_deatail(detail: detail):
    db = next(get_db())
    db_detail = Details(**detail.dict())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail
@app.get("/details/", response_model=list[DetailsResponse])
def read_details(skip: int = 0, limit: int = 10):
    db = next(get_db())
    details = db.query(Details).offset(skip).limit(limit).all()
    return details
@app.delete("/details/{detail_id}", response_model=DetailsResponse)
def delete_detail(detail_id: int):
    db = next(get_db())
    detail = db.query(Details).filter(Details.id == detail_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="Detail not found")
    db.delete(detail)
    db.commit()
    return detail
@app.put("/details/{detail_id}", response_model=DetailsResponse)
def update_detail(detail_id: int, detail: detail):
    db = next(get_db())
    db_detail = db.query(Details).filter(Details.id == detail_id).first()
    if not db_detail:
        raise HTTPException(status_code=404, detail="Detail not found")
    for key, value in detail.dict().items():
        setattr(db_detail, key, value)
    db.commit()
    db.refresh(db_detail)
    return db_detail