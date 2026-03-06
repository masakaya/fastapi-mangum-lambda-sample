from fastapi import FastAPI
from mangum import Mangum

from src.controllers import users

app = FastAPI(
    title="Hello Lambda API",
    description="FastAPI + Mangum sample for AWS Lambda",
    version="0.1.0",
)

# コントローラー登録
app.include_router(users.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello Lambda"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


# AWS Lambda handler
handler = Mangum(app, lifespan="off")
