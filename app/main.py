from fastapi import FastAPI
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app import models
from app.config import settings
from app.routers import auth, jobs, applications, subscriptions

# Função para inicializar o banco com dados iniciais
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Só adiciona dados se não houver vagas
        if db.query(models.Job).count() == 0:
            mock_jobs = [
                models.Job(
                    job_order_number="H-2024-12345",
                    title="Farm Worker - Harvesting",
                    employer="Green Valley Farms",
                    location="Fresno, CA",
                    state="CA",
                    visa_type="H-2A",
                    description="Seasonal harvesting of fruits and vegetables. Experience preferred.",
                    contact_email="jobs@greenvalley.com",
                    posted_at=date(2024, 5, 1),
                    expires_at=date(2024, 8, 30)
                ),
                models.Job(
                    title="Landscaping Assistant",
                    employer="Urban Gardens LLC",
                    location="Austin, TX",
                    state="TX",
                    visa_type="H-2B",
                    description="Residential and commercial landscaping work.",
                    contact_email="hiring@urbangardens.com",
                    posted_at=date(2024, 5, 3),
                    expires_at=date(2024, 7, 15)
                ),
                models.Job(
                    title="Dairy Farm Hand",
                    employer="Meadowbrook Dairy",
                    location="Boise, ID",
                    state="ID",
                    visa_type="H-2A",
                    description="Daily care of dairy cattle and milking operations.",
                    contact_email="careers@meadowbrookdairy.com",
                    posted_at=date(2024, 5, 5),
                    expires_at=date(2024, 9, 1)
                )
            ]
            for job in mock_jobs:
                db.add(job)
            db.commit()
    finally:
        db.close()

# Inicializa o banco
init_db()

# Cria a aplicação FastAPI
app = FastAPI(
    title="H2Apply API",
    description="Backend para o SaaS H2Apply - candidaturas H-2A/H-2B",
    version="1.0.0"
)

# Configuração de CORS
origins = [
    "http://localhost:3000",
    "https://h2apply-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui todas as rotas
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(subscriptions.router)
