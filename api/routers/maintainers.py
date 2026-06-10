from __future__ import annotations

import time
from fastapi import APIRouter

from api.schemas import BaseResponse
from api.routers._store import load_all

router = APIRouter(
    prefix="/api/v1/maintainers",
    tags=["maintainers"],
)


@router.get("/{handle}", response_model=BaseResponse)
def get_exposure(handle: str):
    start = time.time()

    data = load_all()

    packages = [
        r for r in data["pypi"]
        if r["maintainer_handle"] == handle
    ]

    result = {
        "maintainer": handle,
        "package_count": len(packages),
    }

    return BaseResponse(
        response_time_ms=round(
            (time.time() - start) * 1000,
            2,
        ),
        data_freshness_timestamp="latest",
        data=result,
    )