from fastapi import APIRouter, Depends, HTTPException
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
