from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import psycopg2
import os

app = FastAPI()

# שליפת משתני סביבה מ-Render
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# התחברות לבסיס הנתונים
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# מבנה לקוח
class Client(BaseModel):
    company: str
    first_name: str
    last_name: str
    business_id: Optional[str] = None
    phone: Optional[str] = None
    contact_phone: Optional[str] = None
    email: Optional[str] = None
    sector: Optional[str] = None
    source: Optional[str] = None
    created_by: Optional[str] = None
    notes: Optional[str] = None

@app.get("/")
def root():
    return {"message": "PromiXed CRM API is running 🎉"}

@app.get("/clients")
def get_clients():
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    cur.close()
    return rows

@app.post("/clients")
def create_client(client: Client):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients 
        (company, first_name, last_name, business_id, phone, contact_phone, email, sector, source, created_by, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        client.company, client.first_name, client.last_name,
        client.business_id, client.phone, client.contact_phone,
        client.email, client.sector, client.source,
        client.created_by, client.notes
    ))
    client_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return {"id": client_id}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # אפשר לשים במקום * דומיין מסוים אם רוצים הגבלה
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

