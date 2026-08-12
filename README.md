# Expense Tracker - Flask + Blueprint + SQLAlchemy + Vercel + PostgreSQL

## Local setup

```powershell
py -m pip install -r requirements.txt
py run.py
```

Open http://127.0.0.1:5000/

Local development uses SQLite if DATABASE_URL is not set.

## Vercel deployment

1. Push this project to GitHub.
2. Import the repository into Vercel.
3. Vercel detects `vercel.json` and `api/index.py`.
4. Add these Environment Variables in Vercel:

- `DATABASE_URL` = your PostgreSQL connection string
- `SECRET_KEY` = a long random secret

5. Redeploy.

### PostgreSQL

Create a PostgreSQL database using a provider such as Neon, Supabase, or another PostgreSQL host. Copy its connection string into Vercel as `DATABASE_URL`.

Do not use the local SQLite database for production data on Vercel. Vercel's serverless filesystem should not be treated as permanent application storage.

## Features

- Signup and login
- Password hashing
- Session-based authentication
- Add expenses
- View expenses
- Update expenses
- Delete expenses
- Total expenses
- Category totals
- User-specific expense records
- Flask Blueprint architecture
- SQLAlchemy ORM
- SQLite locally / PostgreSQL on Vercel
