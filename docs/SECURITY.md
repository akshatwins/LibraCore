# Security Notes

This project demonstrates baseline application security practices:

- Passwords are hashed with Werkzeug.
- Authentication uses Flask-Login.
- Staff-only operations are protected by role checks.
- Secrets are loaded from environment variables.
- Database queries use SQLAlchemy rather than string-built SQL.
- Production deployment should use HTTPS.

Before public deployment, add:

1. CSRF protection for state-changing forms.
2. Secure cookie configuration.
3. Rate limiting.
4. Account lockout / suspicious login monitoring.
5. Strong password policy and password reset.
6. Security headers.
7. PostgreSQL with restricted database credentials.
8. Centralized logging and alerting.
9. Regular dependency updates.
