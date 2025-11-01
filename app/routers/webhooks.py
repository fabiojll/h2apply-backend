import hashlib
import hmac
import json
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.config import settings

router = APIRouter(tags=["webhooks"])

@router.post("/webhooks/lemon-squeezy")
async def lemon_squeezy_webhook(request: Request, db: Session = Depends(get_db)):
    # 1. Valida o webhook com assinatura
    body = await request.body()
    signature = request.headers.get("x-signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Assinatura ausente")

    expected_signature = hmac.new(
        settings.lemon_squeezy_webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=400, detail="Assinatura inválida")

    # 2. Processa o evento
    payload = json.loads(body)
    event_name = payload["meta"]["event_name"]
    data = payload["data"]

    # Só processa eventos de assinatura
    if event_name not in ["subscription_created", "subscription_updated"]:
        return {"status": "ignored"}

    attributes = data["attributes"]
    user_id = attributes["custom_data"].get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id ausente no webhook")

    # 3. Atualiza ou cria assinatura
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == int(user_id)
    ).first()

    if not subscription:
        subscription = models.Subscription(user_id=int(user_id))

    subscription.status = attributes["status"]
    subscription.lemon_squeezy_subscription_id = data["id"]
    db.add(subscription)
    db.commit()

    return {"status": "success"}
