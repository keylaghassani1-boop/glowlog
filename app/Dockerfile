# ---------- Stage 1: builder ----------
FROM python:3.12.7-slim AS builder

WORKDIR /build

# salin dependency dulu supaya layer cache terpakai
COPY requirements.txt .

# pasang dependency ke folder terpisah (/install)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12.7-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ambil hasil install saja dari stage builder
COPY --from=builder /install /usr/local

# baru salin source code
COPY . .

# jalankan sebagai user biasa, bukan root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]