from sqlalchemy.engine import Engine

from app.evaluations.models import BenchmarkResult


def sync_benchmark_schema(engine: Engine) -> None:
    BenchmarkResult.__table__.create(bind=engine, checkfirst=True)
