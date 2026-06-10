from __future__ import annotations

import time
from fastapi import APIRouter

from api.schemas import BaseResponse
from api.routers._store import load_all

router = APIRouter(
    prefix="/api/v1/ecosystems",
    tags=["ecosystems"],
)


@router.get("/{ecosystem}", response_model=BaseResponse)
def get_patch_velocity(ecosystem: str):
    start = time.time()

    data = load_all()

    records = [
        r for r in data["osv"]
        if r["ecosystem"] == ecosystem
    ]

    avg_severity = (
        sum(r["severity_score"] or 0 for r in records)
        / len(records)
        if records else 0
    )

    result = {
        "ecosystem": ecosystem,
        "avg_severity_score": avg_severity,
        "vulnerability_count": len(records),
    }

    return BaseResponse(
        response_time_ms=round(
            (time.time() - start) * 1000,
            2,
        ),
        data_freshness_timestamp="latest",
        data=result,
    )