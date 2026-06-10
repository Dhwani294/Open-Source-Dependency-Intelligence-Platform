from fastapi import APIRouter

from api.schemas import BaseResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["health"],
)


@router.get("/health", response_model=BaseResponse)
def health():
    return BaseResponse(
        response_time_ms=0.1,
        data_freshness_timestamp="system",
        data={"status": "ok"},
    )