import requests
from datetime import datetime
import random

URL = "http://127.0.0.1:8000/logs"
TOKEN = "token_servicio_A"


logs = []
for _ in range(5):
    logs.append({
        "timestamp": datetime.utcnow().isoformat(),
        "service": "servicio_A",
        "severity": random.choice(["INFO", "DEBUG", "ERROR"]),
        "message": "Mensaje de prueba"
    })
resp = requests.post(URL, json=logs, headers={
    "Autorization": f"token {TOKEN}"
    })
print(resp.json())