from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.evaluations.models import BenchmarkResult
from app.validations import service
from app.validations.schemas import ValidationReportCreate, ValidationReportRead


router = APIRouter()


@router.post(
    "/benchmarks/{benchmark_id}/validate",
    response_model=ValidationReportRead,
    status_code=status.HTTP_201_CREATED,
)
def create_benchmark_validation(
    benchmark_id: int,
    payload: ValidationReportCreate,
    db: Session = Depends(get_db),
):
    benchmark = db.execute(
        select(BenchmarkResult).where(BenchmarkResult.id == benchmark_id)
    ).scalar_one_or_none()
    
    if benchmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benchmark result not found.",
        )
        
    return service.create_validation_report(db, benchmark, payload)


@router.get(
    "/benchmarks/{benchmark_id}/validate",
    response_model=ValidationReportRead,
)
def get_benchmark_validation(
    benchmark_id: int,
    db: Session = Depends(get_db),
):
    report = service.get_validation_report(db, benchmark_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validation report not found.",
        )
    return report
