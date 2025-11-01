from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user  # vamos criar isso depois
from typing import List

router = APIRouter(prefix="/applications", tags=["applications"])

# Dependência para obter usuário autenticado
def get_current_user_from_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Vamos implementar isso na próxima etapa
    pass

@router.post("/", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # protegido
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
    current_user: models.User = Depends(get_current_user)  # protegido
):
    applications = db.query(models.Application).filter(
        models.Application.user_id == current_user.id
    ).all()
    return applications
