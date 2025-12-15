from fastapi import FastAPI

from app.database.session import engine, Base
from app.models import user, property, ownership

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}
