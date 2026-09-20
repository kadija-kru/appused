# Secure Access Control API

A security-focused backend portfolio project demonstrating authentication, authorization, database-backed users, role-based access control (RBAC), password hashing, JWT access tokens, transactional writes, automated tests, Docker, and CI.

## Engineering goals

This project is designed around production concerns rather than basic CRUD:

- Passwords are never stored in plaintext
- JWTs are signed and expire
- Protected endpoints require authentication
- Admin-only routes enforce role checks
- Duplicate usernames are rejected at the database layer
- Database operations use transactional commits/rollbacks
- Tests exercise authentication and authorization behavior
- Docker Compose provides a reproducible PostgreSQL environment

## Stack

FastAPI, SQLAlchemy 2, PostgreSQL, Pydantic, PyJWT, Argon2, Pytest, Docker, GitHub Actions.

## API

- `POST /auth/register`
- `POST /auth/login`
- `GET /me`
- `GET /admin/users`
- `GET /health`

## Run locally

```bash
docker compose up --build
```

API docs: `http://localhost:8000/docs`

## Security notes

This is a portfolio implementation, not an identity-provider replacement. A production deployment should additionally use managed secret storage, TLS, audit logging, token rotation, rate limiting, monitoring, and MFA when appropriate.

## What this project demonstrates

Backend engineering, API security, OWASP-aware design, authentication, authorization, relational persistence, transaction handling, testing, containerization, and CI.
