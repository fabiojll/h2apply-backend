from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import models
from app.database import get_db

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

# Rota para verificar status da assinatura
@router.get("/status")
def get_subscription_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # assumindo que você tem get_current_user
):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id
    ).first()
    status = subscription.status if subscription else "inactive"
    return {"status": status}

# Rota para ativação manual por código (enviado por e-mail)
@router.post("/activate")
def activate_subscription(
    code: str = Query(..., description="Código de ativação enviado por e-mail"),
    db: Session = Depends(get_db)
):
    # 🔑 Substitua esta lista pelos códigos válidos que você gerar
    VALID_CODES = ["ABC123", "XYZ789", "H2APPLY2025"]  # ← personalize aqui

    if code not in VALID_CODES:
        raise HTTPException(status_code=400, detail="Código de ativação inválido")

    # Aqui você pode associar o código a um e-mail específico se quiser
    # Por simplicidade, vamos ativar a assinatura do último usuário cadastrado
    # (ou você pode pedir o e-mail no corpo da requisição)

    # Alternativa mais segura: peça o e-mail junto com o código
    # Mas para manter simples, vamos ativar via token no frontend depois

    # ⚠️ Esta versão ativa a assinatura do usuário logado
    # Então o frontend deve enviar o token + código
    raise HTTPException(status_code=501, detail="Rota de ativação requer autenticação. Use /activate-me com token.")
