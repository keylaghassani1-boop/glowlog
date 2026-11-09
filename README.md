# GlowLog: Jurnal Skincare Pribadi ✨

GlowLog adalah aplikasi web sederhana untuk mencatat produk skincare yang
kamu pakai, menandai cocok atau tidaknya di kulit, dan mengingatkan produk
mana yang sebentar lagi kedaluwarsa. Dibuat dengan FastAPI + PostgreSQL dan
dijalankan penuh di Docker Compose (localhost).

## Mengapa proyek ini?

Saya sering membeli skincare baru, lalu terkadang lupa kapan mulai dipakai, produk mana yang bikin kulit breakout, dan kapan harus berhenti pakai karena sudah kedaluwarsa. Catatan di notes HP biasanya berantakan dan akhirnya terlupakan. Dari situ muncul ide GlowLog: satu tempat rapi untuk mencatat produk dan reaksinya.

Saya juga sengaja memilih topik yang dekat dengan keseharian saya dan tidak
umum, supaya saya bisa menjelaskan masalahnya dengan paham. Secara teknis,
proyek ini cukup kecil untuk fokus ke yang dinilai: containerization,
yaitu Dockerfile multi-stage, Docker Compose, healthcheck, network, dan
volume.

Data yang disimpan hanya nama produk, merek, kategori, tanggal, dan
catatan cocok atau tidak. Tidak ada data pribadi pengguna, dan semua data
contoh di repo ini adalah data dummy.

## Fitur dan endpoint

| Method | Endpoint | Fungsi | Status |
|--------|----------|--------|--------|
| GET | `/health` | Cek aplikasi hidup | 200 |
| GET | `/products` | Daftar semua produk | 200 |
| GET | `/products/expiring` | Produk yang kedaluwarsa dalam 30 hari | 200 |
| POST | `/products` | Tambah produk baru | 201 |

Input yang tidak valid ditolak otomatis dengan status 422.

## Arsitektur

- **app**: FastAPI (Python 3.12), port 8000 dibuka ke localhost
- **db**: PostgreSQL 16.4 dengan named volume `pgdata` dan healthcheck
- **adminer** (opsional, profile `tools`): melihat isi database lewat browser
- Semua service berada di satu user-defined network `glowlog-net`, dan app
  mengakses database lewat nama service `db`, bukan IP atau localhost.

Alur request: Browser, lalu app (port 8000), lalu db (port 5432, hanya di
dalam network).

## Cara menjalankan

Prasyarat: Docker Desktop dan Git.

```bash
git clone https://github.com/keylaghassani1-boop/glowlog.git
cd glowlog
cp .env.example .env        # Windows (PowerShell): copy .env.example .env
```

Buka file `.env`, lalu ganti `DB_PASSWORD` dengan password sendiri.

```bash
docker compose up -d --build
```

Lalu buka:
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Untuk menjalankan Adminer (opsional):

```bash
docker compose --profile tools up -d
```

Adminer ada di http://localhost:8080 (server: `db`, user dan password sesuai `.env`).

Untuk berhenti:

```bash
docker compose down        # data tetap aman di volume
docker compose down -v     # data ikut terhapus
```

## Screenshot

(Screenshot akan ditambahkan: docker compose ps, Swagger 201 dan 200, uji persistensi, docker images.)

## Tautan

- Artikel: (segera ditambahkan)
- Video YouTube: (segera ditambahkan)

## Sumber dan atribusi

Library dan image open-source yang dipakai: FastAPI, Uvicorn, psycopg2,
Pydantic, PostgreSQL, Adminer, dan image dasar `python:3.12.7-slim`.
Tidak memakai starter template khusus.

## AI Usage Declaration

- **Alat yang dipakai:** Claude (Anthropic)
- **Bagian yang dibantu AI:**
  - Brainstorming dan pemilihan topik proyek
  - Draf awal kode aplikasi FastAPI (`main.py`)
  - Draf awal `Dockerfile`, `.dockerignore`, `docker-compose.yml`, dan `.env.example`