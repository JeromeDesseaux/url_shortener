from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

# Simple test d'accessibilité du serveur sur sa racine
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to our URL shortener app"}

# Création d'une URL raccourcie, réception de sa version courte et vérification 
# du stockage REDIS sur un double appel
def test_shorten_url():
    website_to_shorten = "https://youtube.com"
    post_data = {"url": website_to_shorten}
    response = client.post("/shortify", json=post_data)
    json = response.json()
    assert response.status_code == 200
    assert json is not None
    assert "short" in json
    # Test duplicated entry
    response = client.post("/shortify", json=post_data)
    json = response.json()
    assert response.status_code == 200
    assert json is not None
    assert "short" in json

# Test de redirection lors de l'appel avec une URL raccourcie
def test_redirect():
    website_to_shorten = "https://youtube.com"
    post_data = {"url": website_to_shorten}
    response = client.post("/shortify", json=post_data)
    json = response.json()
    assert response.status_code == 200
    assert json is not None
    assert "short" in json
    shorten_url = json['short']
    # Test duplicated entry
    response = client.get(f"/{shorten_url}")
    assert response.status_code == 200