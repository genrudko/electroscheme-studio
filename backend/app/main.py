from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "app": "ElectroScheme Studio API",
    }


@app.get("/api/demo-project")
def demo_project() -> dict:
    return {
        "version": "0.1",
        "project": {
            "name": "Minimal Demo",
            "code": "minimal-demo",
        },
        "sheets": [
            {
                "id": "sheet_1",
                "name": "Demo Sheet",
                "format": "A3",
                "orientation": "landscape",
                "width_mm": 420,
                "height_mm": 297,
            }
        ],
        "symbols": [
            {
                "id": "busbar_1",
                "type": "busbar",
                "label": "1C",
                "x": 60,
                "y": 60,
                "width": 260,
                "height": 0,
                "terminals": [
                    {"id": "t1", "x": 120, "y": 60},
                    {"id": "t2", "x": 220, "y": 60},
                ],
            },
            {
                "id": "q1",
                "type": "circuit_breaker",
                "label": "Q1",
                "x": 120,
                "y": 110,
                "rotation": 90,
                "terminals": [
                    {"id": "a", "x": 120, "y": 80},
                    {"id": "b", "x": 120, "y": 145},
                ],
                "properties": {
                    "name": "Demo circuit breaker",
                    "voltage_kv": 10,
                    "state": "closed",
                },
            },
        ],
        "connections": [
            {
                "id": "conn_1",
                "from": "busbar_1.t1",
                "to": "q1.a",
            }
        ],
    }
