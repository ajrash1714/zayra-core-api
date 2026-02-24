# zayra-core-api

Zayra ECG FastAPI backend - Core endpoints for user management, ECG data ingestion, and event processing

## Setup & Development

### Prerequisites
- Python 3.9+
- pip/conda

### Installation

```bash
git clone https://github.com/ajrash1714/zayra-core-api.git
cd zayra-core-api
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at `http://localhost:8000`
Swagger Docs: `http://localhost:8000/docs`

## API Endpoints

- `GET /users` - Get all users
- `POST /users` - Create new user
- `POST /ingest` - Ingest ECG data
- `GET /events` - Get recorded events
- `POST /events` - Create new event

## Deployment

Deploy to Render, Railway, or Fly.io using GitHub integration.
