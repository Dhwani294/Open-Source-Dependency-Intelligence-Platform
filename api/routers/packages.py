from __future__ import annotations

import time
from fastapi import APIRouter

from api.schemas import BaseResponse
from api.routers._store import load_all

router = APIRouter(
    prefix="/api/v1/packages",
    tags=["packages"],
)


def compute_risk(vulns):
    if not vulns:
        return "LOW"

    max_score = max(
        v.get("severity_score") or 0
        for v in vulns
    )

    if max_score >= 9:
        return "CRITICAL"
    if max_score >= 7:
        return "HIGH"
    if max_score >= 4:
        return "MEDIUM"
    return "LOW"


@router.get("/{package_name}", response_model=BaseResponse)
def get_package_risk(package_name: str):
    start = time.time()

    data = load_all()

    vulns = [
        r for r in data["osv"]
        if r["package_name"] == package_name
    ]

    result = {
        "package_name": package_name,
        "risk_score": compute_risk(vulns),
        "vulnerability_count": len(vulns),
    }

    return BaseResponse(
        response_time_ms=round(
            (time.time() - start) * 1000,
            2,
        ),
        data_freshness_timestamp="latest",
        data=result,
    )