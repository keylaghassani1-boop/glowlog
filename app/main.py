import os
from contextlib import asynccontextmanager
from datetime import date
from typing import Literal, Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel, Field


def get_conn():
    # host = nama service di docker-compose ("db"), bukan localhost
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "glowlog"),
        user=os.getenv("DB_USER", "glowlog"),
        password=os.getenv("DB_PASSWORD", ""),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # buat tabel saat aplikasi pertama jalan
    conn = get_conn()
    with conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                brand TEXT NOT NULL,
                category TEXT NOT NULL,
                opened_at DATE,
                expires_at DATE,
                verdict TEXT NOT NULL DEFAULT 'masih dicoba',
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
    conn.close()
    yield


app = FastAPI(title="GlowLog", lifespan=lifespan)


class ProductIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    brand: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    opened_at: Optional[date] = None
    expires_at: Optional[date] = None
    verdict: Literal["cocok", "tidak cocok", "masih dicoba"] = "masih dicoba"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products")
def list_products():
    conn = get_conn()
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM products ORDER BY id DESC")
        rows = cur.fetchall()
    conn.close()
    return rows


@app.get("/products/expiring")
def expiring_products():
    # produk yang kedaluwarsa dalam 30 hari ke depan
    conn = get_conn()
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT * FROM products
            WHERE expires_at IS NOT NULL
              AND expires_at BETWEEN CURRENT_DATE AND CURRENT_DATE + 30
            ORDER BY expires_at
        """)
        rows = cur.fetchall()
    conn.close()
    return rows


@app.post("/products", status_code=201)
def create_product(p: ProductIn):
    conn = get_conn()
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """INSERT INTO products (name, brand, category, opened_at, expires_at, verdict)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
            (p.name, p.brand, p.category, p.opened_at, p.expires_at, p.verdict),
        )
        row = cur.fetchone()
    conn.close()
    return row