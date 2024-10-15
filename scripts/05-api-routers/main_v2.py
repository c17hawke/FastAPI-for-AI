from fastapi import FastAPI
from routers import train, predict

app = FastAPI()
app.include_router(train.router)
app.include_router(predict.router)
