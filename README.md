# Payroll Management

A payroll management system with a Django REST API backend and a Vue 3 admin dashboard frontend.

- `Payroll/` — Django backend (PostgreSQL, REST API, Swagger docs)
- `admin-one-vue-tailwind/` — Vue 3 + Tailwind frontend

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (running locally, or accessible over the network)

## Backend setup

```bash
cd Payroll
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create your local config from the example file:

```bash
cp .env.example .env
```

Edit `.env` and set `DB_USER` / `DB_PASSWORD` to a real PostgreSQL role on your machine (the default `postgres` user works for most standard installs — Homebrew's Postgres on macOS instead defaults to a role matching your OS username, so use that if `postgres` doesn't exist for you: run `psql -l` to check).

Create the database (name must match `DB_NAME` in `.env`):

```bash
createdb payroll
```

Apply migrations and create an admin account:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the server:

```bash
python manage.py runserver
```

The API is now at `http://localhost:8000/api/`, Django admin at `http://localhost:8000/admin/`, and Swagger docs at `http://localhost:8000/api/docs/`.

## Frontend setup

```bash
cd admin-one-vue-tailwind
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173/admin-one-vue-tailwind/#/login`.

## First login

Log in with the superuser account you created above — that account has admin access to the whole dashboard. From the **Employees** page, admins can create employee records and set individual login credentials for staff (employee login username is their Employee ID).

## Troubleshooting

- **Backend won't start / database connection errors**: almost always means `Payroll/.env` is missing or has the wrong `DB_USER`/`DB_PASSWORD` for your PostgreSQL setup. `.env` is intentionally excluded from git (it's environment-specific) — copy `.env.example` and fill in your own local database credentials.
- **"database does not exist"**: run `createdb payroll` (or `psql -c "CREATE DATABASE payroll;"`).
- **Frontend shows no data / network errors**: make sure the Django server is running on port 8000 and `admin-one-vue-tailwind/.env` points `VITE_API_BASE_URL` at it.
