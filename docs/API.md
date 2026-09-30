# API Reference

All API endpoints require an authenticated session.

## GET /api/books

Returns the catalog.

Example:

```json
{
  "data": [
    {
      "id": 1,
      "isbn": "9780132350884",
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "category": "Software Engineering",
      "total_copies": 4,
      "available_copies": 3
    }
  ]
}
```

## GET /api/members

Returns registered members.

## GET /api/circulation

Returns recent circulation records and their computed status.

## POST /api/books

Required JSON:

```json
{
  "isbn": "9780000000000",
  "title": "Example",
  "author": "Author",
  "category": "Programming",
  "total_copies": 2
}
```

## POST /api/members

Required JSON:

```json
{
  "name": "New Member",
  "email": "new@example.com",
  "password": "SecurePassword"
}
```

## HTTP status conventions

- `200` successful read
- `201` successful creation
- `400` validation error
- `401` unauthenticated
- `403` unauthorized
- `404` resource not found
- `409` conflict


## GET /api/reservations

Returns reservation records.

## GET /api/analytics

Returns computed circulation and operational analytics.

