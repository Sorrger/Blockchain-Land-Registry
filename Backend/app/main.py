from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, properties, ownerships

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(properties.router)
app.include_router(ownerships.router)


@app.get("/health")
def health():
    return {"status": "ok"}
