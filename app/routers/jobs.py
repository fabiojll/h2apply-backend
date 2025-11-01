from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas
from app.database import get_db
from typing import List, Optional

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=List[schemas.JobResponse])
def read_jobs(
    visa_type: Optional[str] = Query("all"),
    state: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    employer: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Job)

    # Filtro por tipo de visto
    if visa_type != "all":
        query = query.filter(models.Job.visa_type == visa_type)

    # Filtro por estado
    if state:
        query = query.filter(models.Job.state.ilike(f"%{state}%"))

    # Filtro por título
    if title:
        query = query.filter(models.Job.title.ilike(f"%{title}%"))

    # Filtro por empresa
    if employer:
        query = query.filter(models.Job.employer.ilike(f"%{employer}%"))

    jobs = query.all()
    return jobs
