# ScamShield AI (Beginner Version)

Simple scam detector API for beginners.

It uses:
- **Python**
- **REST API (FastAPI)**
- **SQL database (SQLite now, PostgreSQL later)**
- **AI model (scikit-learn)**
- **AI-generated dataset (`data/ai_generated_scam_dataset.csv`)**

## What this API returns

For each suspicious message/email it returns:
- scam risk score (`confidence`)
- scam type (`scam_type`)
- explanation (`reasons`)
- recommended next step (`recommended_action`)

## Simple architecture

`User text -> /detect endpoint -> AI model + rules -> save to SQL DB -> JSON response`

## Endpoints

- `POST /detect`
- `POST /feedback`
- `GET /messages`
- `GET /messages/{id}`
- `GET /stats`
- `GET /health`

## 1) Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) (Optional) Regenerate AI dataset

This creates a larger synthetic training dataset:

```bash
python3 app/ml/generate_dataset.py
```

## 3) Run API

```bash
uvicorn app.main:app --reload
```

Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Open Simple Web App: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Open History Page: [http://127.0.0.1:8000/history](http://127.0.0.1:8000/history)

## 4) Test detection

```bash
curl -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"Your bank account is locked. Click now to verify now.","channel":"email"}'
```

## Notes for class/hackathon

- Database tables are created automatically when app starts.
- Data is stored in `scamshield.db` (SQLite).
- To switch to PostgreSQL later, set `DATABASE_URL`.