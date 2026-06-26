from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.evaluations.models import BenchmarkResult
from app.validations.models import ValidationReport
from app.validations.schemas import ValidationReportCreate


def calculate_overall_score(payload: ValidationReportCreate) -> float:
    good_scores = [
        payload.factual_accuracy_score,
        payload.citation_reliability_score,
        payload.prompt_adherence_score,
        payload.consistency_score,
        payload.reasoning_quality_score,
        payload.economic_efficiency_score,
    ]
    avg_good = sum(good_scores) / len(good_scores)
    
    # Penalize based on hallucination rate
    overall_score = avg_good - (payload.hallucination_rate * 0.5)
    
    return round(max(0.0, min(100.0, overall_score)), 2)


def create_validation_report(
    db: Session,
    benchmark: BenchmarkResult,
    payload: ValidationReportCreate,
) -> ValidationReport:
    existing = db.execute(
        select(ValidationReport).where(ValidationReport.benchmark_id == benchmark.id)
    ).scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Validation report already exists for this benchmark result.",
        )
        
    overall_score = calculate_overall_score(payload)
    
    report = ValidationReport(
        benchmark_id=benchmark.id,
        agent_id=benchmark.agent_id,
        factual_accuracy_score=payload.factual_accuracy_score,
        hallucination_rate=payload.hallucination_rate,
        citation_reliability_score=payload.citation_reliability_score,
        prompt_adherence_score=payload.prompt_adherence_score,
        consistency_score=payload.consistency_score,
        reasoning_quality_score=payload.reasoning_quality_score,
        economic_efficiency_score=payload.economic_efficiency_score,
        overall_validation_score=overall_score,
        details=payload.details,
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_validation_report(
    db: Session,
    benchmark_id: int,
) -> ValidationReport | None:
    return db.execute(
        select(ValidationReport).where(ValidationReport.benchmark_id == benchmark_id)
    ).scalar_one_or_none()
