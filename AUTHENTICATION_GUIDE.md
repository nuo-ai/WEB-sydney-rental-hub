# Authentication Guide

This guide explains how user authentication works in the Sydney Rental Hub backend.

## Overview
- FastAPI application uses JSON Web Tokens (JWT) for stateless auth.
- Register via `/auth/register` and log in through `/auth/login`.
- On success the server returns an access token; send it with `Authorization: Bearer <token>`.
- Tokens expire periodically; request a new token by logging in again or using a refresh endpoint if available.

## Example
```bash
curl -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"secret"}'
```
The response includes an `access_token`:
```json
{"access_token":"<token>","token_type":"bearer"}
```
Use the token on subsequent API calls:
```bash
curl -H 'Authorization: Bearer <token>' http://localhost:8000/protected-endpoint
```

## Environment
Ensure `SECRET_KEY` and `JWT_ALGORITHM` are defined in `.env`. See `SECURITY_CHECKLIST.md` for additional practices.
