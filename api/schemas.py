from pydantic import BaseModel
from typing import Any


class BaseResponse(BaseModel):
    response_time_ms: float
    data_freshness_timestamp: str
    data: Any