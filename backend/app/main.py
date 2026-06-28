from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.project import router as project_router
from app.api.symbol_library import router as symbol_router

app = FastAPI(
    title="ElectroScheme Studio API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)
app.include_router(symbol_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "app": "ElectroScheme Studio API",
    }


@app.get("/api/demo-project")
def demo_project() -> dict:
    """Legacy endpoint; prefer GET /api/project."""
    from app.core.project_service import get_demo_project

    return get_demo_project().model_dump(by_alias=True)
