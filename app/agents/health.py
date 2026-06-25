from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class HealthCheckResult:
    status: str
    status_code: int | None
    response_time_ms: float | None
    error: str | None
    checked_at: datetime


def check_endpoint(endpoint: str, timeout_seconds: float = 5.0) -> HealthCheckResult:
    checked_at = datetime.now(UTC)
    parsed = urlparse(endpoint)

    if parsed.scheme not in {"http", "https"}:
        return HealthCheckResult(
            status="invalid_endpoint",
            status_code=None,
            response_time_ms=None,
            error="Endpoint must use http or https.",
            checked_at=checked_at,
        )

    request = Request(
        endpoint,
        method="GET",
        headers={"User-Agent": "AgentRank-HealthCheck/0.1"},
    )
    started_at = perf_counter()

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            status_code = response.status
            response.read(1024)
    except HTTPError as exc:
        response_time_ms = round((perf_counter() - started_at) * 1000, 2)
        return HealthCheckResult(
            status=_status_from_code(exc.code),
            status_code=exc.code,
            response_time_ms=response_time_ms,
            error=str(exc.reason),
            checked_at=checked_at,
        )
    except (TimeoutError, URLError, OSError) as exc:
        response_time_ms = round((perf_counter() - started_at) * 1000, 2)
        return HealthCheckResult(
            status="unreachable",
            status_code=None,
            response_time_ms=response_time_ms,
            error=str(exc),
            checked_at=checked_at,
        )

    response_time_ms = round((perf_counter() - started_at) * 1000, 2)
    return HealthCheckResult(
        status=_status_from_code(status_code),
        status_code=status_code,
        response_time_ms=response_time_ms,
        error=None,
        checked_at=checked_at,
    )


def _status_from_code(status_code: int) -> str:
    if 200 <= status_code < 400:
        return "healthy"
    if 400 <= status_code < 500:
        return "degraded"
    return "unreachable"
