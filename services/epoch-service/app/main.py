from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator


class EpochRequest(BaseModel):
    date: datetime = Field(..., description="ISO-8601 timestamp with timezone")

    @field_validator("date")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("date must include a timezone")
        return value


class EpochResponse(BaseModel):
    epoch: int


app = FastAPI(title="epoch-service", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/epoch", response_model=EpochResponse)
def epoch(request: EpochRequest) -> EpochResponse:
    return EpochResponse(epoch=int(request.date.timestamp()))
