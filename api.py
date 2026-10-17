import logging
import os
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("thaif.production")

STARTED_AT = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Production API starting")
    yield
    logger.info("Production API shutting down")


app = FastAPI(
    title="Thaif AI Production System",
    description="A production-style API with validation, request IDs, logs, and health monitoring.",
    version="1.0.0",
    lifespan=lifespan,
)


class TextInput(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


def process_text(text: str) -> dict:
    cleaned = " ".join(text.split())
    if not cleaned:
        raise HTTPException(
            status_code=422,
            detail="Text cannot be blank.",
        )

    words = cleaned.split()
    return {
        "original_text": cleaned,
        "word_count": len(words),
        "character_count": len(cleaned),
        "uppercase_text": cleaned.upper(),
        "status": "processed",
    }


@app.middleware("http")
async def request_logging(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "Unhandled request error request_id=%s path=%s",
            request_id,
            request.url.path,
        )
        raise

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/")
def root():
    return {
        "name": "Thaif AI Production System",
        "version": app.version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "uptime_seconds": round(time.time() - STARTED_AT, 2)}


@app.post("/process")
def process(payload: TextInput):
    result = process_text(payload.text)
    logger.info(
        "text_processed word_count=%s character_count=%s",
        result["word_count"],
        result["character_count"],
    )
    return result