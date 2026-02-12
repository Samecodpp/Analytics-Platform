# Analytics Platform

## Description
A web platform for project management with multi-user access support.

## MVP
- User registration and login with JWT authentication
- User and role management
- Project creation and management
- Team member management
- Get metrics from client applications

## Getting Started

### Requirements
- Python 3.8+
- PostgreSQL 12+

### Installation
1. Clone the repository and navigate to the folder
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure .env file with DATABASE_URL and SECRET_KEY

### Running the Server
```bash
uvicorn app.main:app --reload
```

API access: http://localhost:8000/docs

## Tech Stack
FastAPI, SQLAlchemy, PostgreSQL, JWT, Pydantic
