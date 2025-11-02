from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.get("/status")
def get_subscription_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id
    ).first()
    status = subscription.status if subscription else "inactive"
    return {"status": status}

@router.post("/activate")
def activate_subscription(
    code: str = Query(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    VALID_CODES = ["ABC123", "XYZ789", "H2APPLY2025"]  # ← personalize

    if code not in VALID_CODES:
        raise HTTPException(status_code=400, detail="Código inválido")

    # Ativa ou cria assinatura
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        subscription = models.Subscription(user_id=current_user.id)

    subscription.status = "active"
    db.add(subscription)
    db.commit()

    return {"message": "Assinatura ativada com sucesso!"}
