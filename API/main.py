import uvicorn
from fastapi import FastAPI

from initialize import init_app

app = FastAPI(title="Accuracy", version="1.0")


# 初始化app
init_app(app)


@app.get("/")
async def read_root():
    return {"Hello": "Accuracy"}


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
