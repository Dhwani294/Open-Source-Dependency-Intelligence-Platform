from __future__ import annotations

import time
from datetime import datetime, timezone

from fastapi import FastAPI

from api.routers import (
    vulnerabilities,
    packages,
    ecosystems,
    maintainers,
    health,
)

app = FastAPI(
    title="VulnGraph API",
    version="1.0.0",
)


def response_meta(start_time: float) -> dict:
    return {
        "response_time_ms": round(
            (time.time() - start_time) * 1000,
            2,
        ),
        "data_freshness_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }


app.include_router(vulnerabilities.router)
app.include_router(packages.router)
app.include_router(ecosystems.router)
app.include_router(maintainers.router)
app.include_router(health.router)