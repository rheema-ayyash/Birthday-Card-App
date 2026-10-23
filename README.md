# Birthday Card App

An enterprise-grade, production-ready backend service built with FastAPI, SQLAlchemy, PostgreSQL, Pydantic v2, and JWT authentication. This application features modular service-oriented architecture, secure token-based authorization, server-to-server API communication via `httpx`, and asynchronous background task processing.

---

## Key Features

* **Secure Authentication & Authorization:** Implements OAuth2 Password Flow with JSON Web Tokens (JWT) and bcrypt password hashing via `passlib`.
* **Relational Database Architecture:** Manages relational user accounts and scheduled greeting cards using SQLAlchemy 2.0 ORM.
* **Public UUID Slug Sharing:** Generates secure, unguessable public URLs (`/cards/{uuid}`) for recipients to view cards without requiring an account.
* **Recipient Vault:** Authenticated users can view a secure vault listing all cards sent directly to their registered email address.
* **Asynchronous Server-to-Server Integrations:** Communicates with external email delivery services using `httpx` and FastAPI `BackgroundTasks` for non-blocking execution.
* **Enterprise Containerization:** Fully containerized with Docker and orchestrated alongside PostgreSQL via Docker Compose.

---

## Technology Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Server:** Uvicorn (ASGI)
* **ORM:** SQLAlchemy 2.0
* **Validation:** Pydantic v2 (`email-validator`)
* **Security:** `passlib[bcrypt]`, `python-jose[cryptography]`
* **HTTP Client:** `httpx`
* **Database:** PostgreSQL (Production) / SQLite (Local Prototyping)
* **Containerization:** Docker & Docker Compose

---

## System Architecture & File Structure

```text
Birthday-Card-App/
├── app/
│   ├── __init__.py          # Package initialization marker
│   ├── database.py          # SQLAlchemy engine, session factory, and get_db dependency
│   ├── models.py            # SQLAlchemy database ORM models (User, Card)
│   ├── schemas.py           # Pydantic validation models for request/response payloads
│   ├── auth.py              # JWT encoding, decoding, password hashing, and user dependency
│   ├── routers/
│   │   ├── auth.py          # Authentication routes (/auth/register, /auth/token)
│   │   └── cards.py         # Card management routes (POST /, GET /vault, GET /{uuid})
│   └── services/
│       └── email.py         # External server-to-server email dispatch client (httpx)
├── Dockerfile               # Container build instructions for FastAPI app
├── docker-compose.yml       # Orchestrates web service and PostgreSQL database containers
├── requirements.txt         # Pinned project dependencies
└── .env                     # Environment variables (SECRET_KEY, DATABASE_URL, API keys)