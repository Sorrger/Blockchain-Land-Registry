from fastapi import FastAPI
from app.routers import users, properties, ownerships

app = FastAPI()

app.include_router(users.router)
app.include_router(properties.router)
app.include_router(ownerships.router)


@app.get("/health")
def health():
    return {"status": "ok"}
