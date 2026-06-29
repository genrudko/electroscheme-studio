from __future__ import annotations

from fastapi import APIRouter

from app.core.parametric_busbar import generate_busbar_preview
from app.schemas.parametric_symbols import BusbarPreviewRequest, ParametricSymbolPreview


router = APIRouter(prefix="/api/parametric-symbols", tags=["parametric-symbols"])


@router.get("/busbar/default", response_model=ParametricSymbolPreview)
def default_busbar_preview() -> ParametricSymbolPreview:
    return generate_busbar_preview(BusbarPreviewRequest())


@router.post("/busbar/preview", response_model=ParametricSymbolPreview)
def busbar_preview(request: BusbarPreviewRequest) -> ParametricSymbolPreview:
    return generate_busbar_preview(request)