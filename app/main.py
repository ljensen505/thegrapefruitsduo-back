from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import version
from app.routers import musician_router, user_router

app = FastAPI()
app.include_router(musician_router)
app.include_router(user_router)

origins = [
    "http://localhost:3000",
    "https://thegrapefruitsduo.com",
    "https://www.thegrapefruitsduo.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    message = "api for thegrapefruitsduo.com"
    return {"message": message, "version": version}
