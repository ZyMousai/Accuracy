# from typing import Optional

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Accuracy", version="1.0")

# 跨域
# allow_origins 允许的url列表
# allow_methods 允许的请求方式
# allow_headers 允许的请求头
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
