from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from biomed_api.api.routes import router


app = FastAPI(
    title="Biomedical Analytics API",
    version="0.1.0",
    description="FastAPI + Plotly biomedical analytics service.",
)
app.mount("/output", StaticFiles(directory="output"), name="output")
app.include_router(router)
