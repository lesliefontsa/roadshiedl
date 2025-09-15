import requests
import json

# Test de l'API de connexion
url = "http://localhost:8009/api/auth/login/"
data = {
    "username": "client1",
    "password": "client123"
}

print("=== Test de connexion API ===")
print(f"URL: {url}")
print(f"Données: {data}")

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"\nCode de réponse: {response.status_code}")
    print(f"Contenu de la réponse:")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(response.text[:500])
        
except requests.exceptions.ConnectionError:
    print("❌ Erreur de connexion au serveur - serveur non accessible")
except requests.exceptions.Timeout:
    print("❌ Timeout - le serveur ne répond pas")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n=== Test terminé ===")