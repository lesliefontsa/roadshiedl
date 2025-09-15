import requests
import json

def test_api():
    try:
        url = 'http://127.0.0.1:8009/api/auth/login/'
        data = {'username': 'admin', 'password': 'admin123'}
        
        print(f"Envoi de la requête vers: {url}")
        print(f"Données: {data}")
        
        response = requests.post(url, json=data, timeout=10)
        
        print(f"\n=== RÉPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"Response Length: {len(response.text)}")
        print(f"Response (premiers 500 caractères):")
        print("-" * 50)
        print(response.text[:500])
        print("-" * 50)
        
        # Essayer de parser comme JSON
        try:
            json_data = response.json()
            print(f"\nJSON parsé avec succès:")
            print(json.dumps(json_data, indent=2))
        except json.JSONDecodeError as e:
            print(f"\nErreur JSON parse: {e}")
            print("Ce n'est pas du JSON valide.")
            
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête: {e}")
    except Exception as e:
        print(f"Erreur générale: {e}")

if __name__ == "__main__":
    test_api()