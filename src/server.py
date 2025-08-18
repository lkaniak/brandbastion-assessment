from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.api import playground_router, chat_router

app = FastAPI(title="BrandBastion Assessment API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playground_router)

app.include_router(chat_router)


if __name__ == "__main__":
    uvicorn.run("src.server:app", host="0.0.0.0", port=7777, reload=True)
