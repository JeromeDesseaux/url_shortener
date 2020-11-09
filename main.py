from fastapi import FastAPI
from routers.shortener import router as shortener_router

# Création du serveur principal
app = FastAPI()

# Ajout des routes du raccourcisseur d'URL
app.include_router(shortener_router)