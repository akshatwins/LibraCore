# Architecture

## Layers

```text
Browser
   |
   v
Flask Routes / Controllers
   |
   +--> Services (business rules)
   |
   +--> SQLAlchemy Models
   |
   v
SQLite / PostgreSQL
```

### Routes

Routes handle HTTP concerns: authentication, request parsing, redirects, and rendering.

### Services

Business-critical operations such as issue, return, and renewal live in `app/services/`. This keeps transaction logic out of templates and makes it testable.

### Models

SQLAlchemy models represent users, books, circulation records, and audit events.

### Templates / Static

Jinja templates provide server-rendered HTML. CSS and JavaScript are kept separately under `app/static`.

## Data relationships

- One `User` can have many circulation records.
- One `Book` can have many circulation records.
- One circulation record references exactly one book and one member.
- Audit events optionally reference the user who performed the action.

## Design decisions

SQLite is used for frictionless local development. The configuration accepts PostgreSQL URLs so the same application can move to a managed relational database without rewriting its domain model.

The service layer explicitly controls inventory mutation during issue and return. This is preferable to letting individual HTTP routes directly alter stock values.
