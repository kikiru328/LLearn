from fastapi import FastAPI  # clean architectgure Framework layer
from fastapi.middleware.cors import CORSMiddleware
from app.api.errors import register_exception_handlers
from app.api.health import router as health_router

print(f"Health router: {health_router}")
print(f"Health router routes: {health_router.routes}")


def create_app() -> FastAPI:
    app = FastAPI(
        title="LLearn API",
        description="AI 기반 개인화 학습 시스템 - 단기 기억을 장기 기억으로 전환",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: 운영 환경에서는 구체적인 도메인으로 제한
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 예외 핸들러
    register_exception_handlers(app)

    # router
    app.include_router(health_router)

    return app


app: FastAPI = create_app()


@app.get("/")
async def root():
    return {"message": "LLearn API Server"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
