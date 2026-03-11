from fastapi import FastAPI, Header, HTTPException
from datetime import datetime
import sqlite3


app = FastAPI()

TOKENS = {"tokem_servicio_A"}

conn = sqlite3.connect("logs.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    service TEXT,
    severity TEXT,
    message TEXT,
    received_at TEXT
)
""")

conn.commit()

@app.post("/logs")
def recibit_logs(logs: list, authorization: str = Header(None)):
    if not authorization or authorization.replace("Token ", "") not in TOKENS:
        raise HTTPException(status_code=401, detail={"error": "Quién sos, bro?"})
    
    for log in logs:
        c.execute("INSERT INTO logs VALUES (NULL, ?, ?, ?, ?, ?)",
                  (log["timestamp"], log["service"], log["severity"], log["message"], datetime.utcnow().isoformat()))
    conn.commit()


@app.get("/logs")
def ver_logs():
    c.execute("SELECT * FROM logs")
    for i in c.fetchall():
        print(i)
    return [{"id": r[0], "timestamp": r[1], "service": r[2], "severity": r[3], "message": r[4], "received_at": r[5]} for r in c.fetchall()]