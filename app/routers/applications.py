from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verifica se a vaga existe
    job = db.query(models.Job).filter(models.Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")

    # Verifica se já se candidatou
    existing = db.query(models.Application).filter(
        models.Application.user_id == current_user.id,
        models.Application.job_id == application.job_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Já se candidatou a esta vaga")

    # Cria candidatura
    db_application = models.Application(
        user_id=current_user.id,
        job_id=application.job_id,
        status="sent"
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.get("/", response_model=List[schemas.ApplicationResponse])
def read_applications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    applications = db.query(models.Application).filter(
        models.Application.user_id == current_user.id
    ).all()
    return applications
