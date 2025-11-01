import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.config import settings
from app.dependencies import get_current_user
from app.schemas import CheckoutResponse

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verifica se já tem assinatura ativa
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id,
        models.Subscription.status == "active"
    ).first()
    if subscription:
        raise HTTPException(status_code=400, detail="Você já tem uma assinatura ativa")

    # Dados para a API da Lemon Squeezy
    checkout_data = {
        "product_options": {
            "redirect_url": f"{settings.frontend_url}/dashboard",
            "receipt_button_text": "Ir para o H2Apply",
            "receipt_link_url": f"{settings.frontend_url}/dashboard"
        },
        "checkout_data": {
            "email": current_user.email,
            "name": current_user.name,
            "custom": {
                "user_id": str(current_user.id)
            }
        },
        "variant_id": settings.lemon_squeezy_variant_id
    }

    headers = {
        "Authorization": f"Bearer {settings.lemon_squeezy_api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://api.lemonsqueezy.com/v1/checkouts",
                json=checkout_data,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            checkout_url = data["data"]["attributes"]["url"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail="Erro ao criar checkout")

    return {"checkout_url": checkout_url}

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
