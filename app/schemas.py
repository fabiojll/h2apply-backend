from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# ===============
# Autenticação
# ===============

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# ===============
# Usuário
# ===============

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    subscription_status: Optional[str] = "inactive"

    class Config:
        from_attributes = True

# ===============
# Vagas (Jobs)
# ===============

class JobBase(BaseModel):
    job_order_number: Optional[str] = None
    title: str
    employer: str
    location: str
    state: str
    visa_type: str
    description: str
    contact_email: str
    posted_at: date
    expires_at: date

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True

# ===============
# Candidaturas (Applications)
# ===============

class ApplicationCreate(BaseModel):
    job_id: int

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    sent_at: date
    status: str

    class Config:
        from_attributes = True

# ===============
# Assinatura (Subscription)
# ===============

class CheckoutResponse(BaseModel):
    checkout_url: str

class SubscriptionStatusResponse(BaseModel):
    status: str
