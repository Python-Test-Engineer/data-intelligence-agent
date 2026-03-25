from __future__ import annotations

import shutil
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from csv_analyser.api.routes import router


OUTPUT_DIR = Path("output")
STARTUP_CLEAN_DIRS = ("images", "insights")
STARTUP_CLEAN_FILES = ("report.md", "RESPONSE_TO_OBJECTIVES.md")


def _reset_output_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for dir_name in STARTUP_CLEAN_DIRS:
        folder = OUTPUT_DIR / dir_name
        folder.mkdir(parents=True, exist_ok=True)
        for child in folder.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    for file_name in STARTUP_CLEAN_FILES:
        file_path = OUTPUT_DIR / file_name
        if file_path.exists() and file_path.is_file():
            file_path.unlink()


@asynccontextmanager
async def lifespan(_: FastAPI):
    _reset_output_dirs()
    yield


app = FastAPI(
    title="CSV Analyser",
    version="0.1.0",
    description="FastAPI + Plotly general-purpose CSV analytics service.",
    lifespan=lifespan,
)
app.mount("/output", StaticFiles(directory="output"), name="output")
app.include_router(router)
