# Database Schema

## users

Stores staff and member identities.

Key fields:
- id
- name
- email
- password_hash
- role
- is_active_user
- created_at

## books

Stores bibliographic and inventory information.

Key fields:
- id
- isbn
- title
- author
- category
- publisher
- publication_year
- total_copies
- available_copies
- shelf
- description

## circulation

Stores each lending transaction.

Key fields:
- id
- book_id
- member_id
- issued_at
- due_date
- returned_at
- renewal_count
- fine_amount

## audit_logs

Stores important administrative events.

Key fields:
- id
- actor_id
- action
- entity
- entity_id
- details
- created_at
