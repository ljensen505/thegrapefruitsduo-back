from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import version
from app.admin import VerifyToken
from app.routers import group_router, musician_router, user_router

app = FastAPI()
app.include_router(musician_router)
app.include_router(user_router)
app.include_router(group_router)

auth = VerifyToken()

origins = [
    "http://localhost:3000",
    "https://thegrapefruitsduo.com",
    "https://www.thegrapefruitsduo.com",
    "https://tgd.lucasjensen.me",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    message = "api for thegrapefruitsduo.com"
    return {"message": message, "version": version}
