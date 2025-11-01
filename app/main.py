from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.database import engine, Base
from app.config import settings

# Cria as tabelas no banco (só na primeira execução)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="H2Apply API",
    description="Backend para o SaaS H2Apply - candidaturas H-2A/H-2B",
    version="1.0.0"
)

# Configuração de CORS
# Substitua pelo URL do seu frontend no Render
origins = [
    "http://localhost:3000",  # para testes locais
    "https://h2apply.onrender.com",  # 👈 ALTERE PARA SEU DOMÍNIO REAL NO RENDER
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router)
