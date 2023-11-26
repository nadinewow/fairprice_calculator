import uvicorn
from fastapi import FastAPI
from app.api.endpoints import router


def create_app() -> FastAPI:
    application = FastAPI()

    application.include_router(router)

    return application


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)


