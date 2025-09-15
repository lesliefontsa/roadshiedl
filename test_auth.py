import urllib.request
import urllib.parse
import json

# Test d'authentification
data = {
    'username': 'admin',
    'password': 'admin123'
}

# Encoder les données
json_data = json.dumps(data).encode('utf-8')

# Créer la requête
req = urllib.request.Request(
    'http://127.0.0.1:8009/api/auth/login/',
    data=json_data,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Success!")
        print("Status:", response.status)
        print("Response:", json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Response:", e.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))