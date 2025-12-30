# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/public")
def public_route():
    print("secret api key!")  # ❌ violates logging
    return {"msg": "no auth!"}  # ❌ violates auth

@app.get("/secure")
def secure_route(auth):
    return {"msg": "ok"}  # ✅ fine

import sqlite3  # ❌ violates allowed database
