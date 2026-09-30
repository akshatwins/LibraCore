# LibraCore — Professional Library Management System

A professional, full-stack Library Management System designed as a portfolio-ready software project. It goes beyond basic student CRUD functionality by combining role-based access control, circulation workflows, analytics, catalog search, overdue management, audit logging, REST APIs, responsive UI, automated tests, and production-oriented project structure.

## Highlights

- Flask application with application factory architecture
- SQLite database by default, PostgreSQL-ready configuration
- Secure password hashing and session-based authentication
- Admin and librarian roles
- Dashboard with circulation and inventory KPIs
- Book catalog with search, filtering, pagination, and stock visibility
- Member management
- Issue / return / renewal workflow
- Automatic overdue detection and fine calculation
- Audit log for important administrative actions
- Reservations / waitlist workflow
- In-app due-date and overdue notifications
- Operational analytics dashboard
- Fine payment data model
- Book cover/language/page metadata
- REST API endpoints for books, members, circulation, reservations and analytics
- Seeded demo data for quick evaluation
- Responsive interface for desktop and mobile
- Unit tests with pytest
- Environment-based configuration
- Docker support
- Clean separation of models, services, routes, templates, and static assets

## Tech Stack

**Backend:** Python, Flask, SQLAlchemy, Flask-Login, Flask-Migrate  
**Database:** SQLite (development), PostgreSQL compatible  
**Frontend:** HTML5, Jinja2, CSS3, Vanilla JavaScript, Bootstrap 5  
**Testing:** pytest  
**Deployment:** Gunicorn + Docker-ready

## Project Structure

```text
library-management-system/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── book.py
│   │   ├── circulation.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── circulation.py
│   │   ├── dashboard.py
│   │   ├── members.py
│   │   └── api.py
│   ├── services/
│   │   ├── circulation.py
│   │   └── dashboard.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/login.html
│   │   ├── dashboard/index.html
│   │   ├── books/index.html
│   │   ├── books/form.html
│   │   ├── members/index.html
│   │   ├── members/form.html
│   │   ├── circulation/index.html
│   │   ├── circulation/form.html
│   │   ├── errors/403.html
│   │   ├── errors/404.html
│   │   └── errors/500.html
│   └── static/
│       ├── css/app.css
│       └── js/app.js
├── migrations/
├── seed/
│   └── seed.py
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── LICENSE
```

## Quick Start

### 1. Clone

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and set a strong secret key.

### 5. Create the database and demo data

```bash
python seed/seed.py
```

### 6. Start the application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

### Demo Accounts

The seed script creates:

- Admin: `admin@library.local` / `Admin@123`
- Librarian: `librarian@library.local` / `Librarian@123`

Change these credentials before any real deployment.

## Core Workflows

### Book circulation

1. Librarian opens **Issue Book**
2. Selects an active member
3. Selects an available book
4. System creates a circulation record
5. Available copy count decreases
6. Return records the actual return time
7. Available copy count is restored
8. Overdue fines are calculated automatically

### Overdue logic

A loan becomes overdue when its due date is before the current date and it has not been returned.

Default fine configuration:

```text
₹5 per overdue day
```

This value is configurable through the application configuration.

## API

Authenticated API endpoints include:

```text
GET    /api/books
GET    /api/members
GET    /api/circulation
POST   /api/books
POST   /api/members
```

The API is intentionally small and portfolio-friendly. Authentication and authorization should be extended before exposing it publicly.

## Testing

```bash
pytest -q
```

## Docker

```bash
docker compose up --build
```

The application is then available at:

```text
http://localhost:5000
```

## Production Notes

For production use:

- Use PostgreSQL instead of SQLite
- Set a long random `SECRET_KEY`
- Set `FLASK_ENV=production`
- Run behind a reverse proxy such as Nginx
- Use HTTPS
- Disable demo credentials
- Configure backups
- Add CSRF protection for production forms
- Use a production identity provider if integrating with an institutional SSO
- Add rate limiting to public-facing endpoints

## Portfolio Talking Points

This project demonstrates:

- MVC-style application architecture
- Relational database design
- Authentication and authorization
- Business-rule implementation
- REST API design
- Search and pagination
- Data validation
- Error handling
- Dashboard analytics
- Automated testing
- Containerization
- Production-readiness considerations

## License

MIT License. See `LICENSE`.
