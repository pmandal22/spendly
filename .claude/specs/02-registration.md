# Spec: Registration

## Overview
This step implements user registration for Spendly. The `/register` route currently
only handles `GET` and renders a static form; this step adds the `POST` handler that
validates input, hashes the password, inserts a new user into the `users` table, and
starts a logged-in session. Registration is the entry point into the app for new
users and is a prerequisite for login, logout, profile, and expense management.

## Depends on
- Step 1 (Database Setup) — requires `get_db()`, `init_db()`, and the `users` table
  to already exist and work correctly.

## Routes
- `POST /register` — accept form submission, validate input, create user, start
  session, redirect to profile/dashboard — public
  
- `GET /register` — already implemented, unchanged

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at)
already supports registration as defined in `database/db.py`. This step adds a new
`create_user()` function to `database/db.py` — a function, not a schema change.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — change `action="/register"` to
  `action="{{ url_for('register') }}"` to comply with the no-hardcoded-URLs rule.
  Add support for re-rendering with `{{ error }}` and previously entered `name`/`email`
  values on validation failure (form already has an `{% if error %}` block).

## Files to change
- `app.py` — update `register()` route to accept `GET` and `POST`, handle form
  validation, call `database/db.py` helper, set session, redirect on success
- `database/db.py` — add `create_user(name, email, password)` and
  `get_user_by_email(email)` helper functions
- `templates/register.html` — fix hardcoded form action to use `url_for()`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders, never f-strings in SQL)
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic lives only in `database/db.py`, never inline in `app.py`
- Use `url_for()` for all internal links — never hardcode URLs
- Validate: name and email required, password minimum 8 characters, email not
  already registered (catch `sqlite3.IntegrityError` on the unique email constraint
  as a backstop, but check first for a clean error message)
- On validation failure, re-render `register.html` with an `error` message and
  preserve previously entered `name`/`email` — do not redirect
- On success, store the new user's id in the session and redirect (session/login
  mechanics beyond storing `session["user_id"]` are out of scope until Step 3)

## Definition of done
- [ ] Submitting the register form with valid name/email/password (8+ chars) creates
      a row in `users` with a hashed password (verify it is not stored in plaintext)
- [ ] Submitting with a duplicate email shows an error on the same page, no new row
      is created, and previously entered form values are preserved
- [ ] Submitting with a password under 8 characters shows an error and creates no row
- [ ] Submitting with a missing name or email shows an error and creates no row
- [ ] On successful registration, `session["user_id"]` is set to the new user's id
- [ ] The register form's action uses `url_for('register')`, not a hardcoded string
- [ ] App starts without errors and `GET /register` still renders correctly
