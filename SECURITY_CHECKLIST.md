# Security Checklist

Review this checklist before deploying or sharing code.

- [ ] Never commit secrets or API keys; store them in `.env` files.
- [ ] Rotate JWT `SECRET_KEY` in production and keep it private.
- [ ] Serve the app over HTTPS and enable HSTS.
- [ ] Validate and sanitize all user input on both client and server.
- [ ] Keep dependencies up to date (`npm audit`, `pip install -r requirements.txt`).
- [ ] Restrict CORS origins to trusted domains.
- [ ] Enforce strong passwords; hash using bcrypt.
- [ ] Log and monitor authentication attempts and errors.
