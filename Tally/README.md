# Tally

Expense splitting API built with FastAPI.

## Project Structure

```
Tally/
├── app/
│   ├── core/           # Security (JWT auth) and shared dependencies
│   ├── models/         # SQLAlchemy models (user, expense, group, etc.)
│   ├── routes/         # API endpoints (auth, groups, expenses, balances, export)
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business logic
│   ├── database.py     # DB engine/session setup
│   └── main.py         # FastAPI app entrypoint
├── analysis/           # Pandas analysis scripts
├── sql/                # SQL queries
├── test/               # Pytest test suite
├── seed.py             # Script to seed the database with sample data
├── requirements.txt
└── .env.example
```

## How to Run

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set the required environment variables (e.g. `SECRET_KEY`).

3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## Running Tests

```bash
pytest
```
