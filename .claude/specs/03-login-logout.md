# Spec: Login and Logout

## Overview
This step implements authentication for existing users. The `/login` route
currently only handles `GET` and renders a static form; this step adds the
`POST` handler that verifies email/password against the `users` table and
starts a session. It also implements the `/logout` stub, clearing the session.
Together with registration (Step 2), this completes the authentication flow
and is a prerequisite for the profile page (Step 4) and all expense management
routes, which need to know which user is acting.

## Depends on
- Step 1 (Database Setup) — requires `get_db()` and the `users` table.
- Step 2 (Registration) — requires `create_user()`, `get_user_by_email()`, and
  the existing `app.secret_key` / `session` usage pattern established in
  `register()`.

## Routes
- `POST /login` — verify credentials, start session, redirect to profile — public
- `GET /login` — already implemented, unchanged
- `GET /logout` — clear session, redirect to landing page — logged-in
  (safe to hit while logged out too; simply becomes a no-op redirect)

## Database changes
No database changes. `get_user_by_email()` (added in Step 2) already returns
everything needed to verify credentials — no new `db.py` functions required.

## Templates
- **Create:** none
- **Modify:** `templates/login.html` — change `action="/login"` to
  `action="{{ url_for('login') }}"` to comply with the no-hardcoded-URLs rule.
  Add support for re-rendering with `{{ error }}` and a previously entered
  `email` value on validation failure (form already has an `{% if error %}`
  block, matching the pattern used in `register.html`).

## Files to change
- `app.py` — update `login()` route to accept `GET` and `POST`, verify
  credentials with `werkzeug.security.check_password_hash`, set session,
  redirect on success; implement `logout()` to clear the session and redirect
- `templates/login.html` — fix hardcoded form action to use `url_for()`;
  preserve entered email on error

## Files to create
None.

## New dependencies
No new dependencies. `check_password_hash` is part of `werkzeug.security`,
already a project dependency (same package `generate_password_hash` comes from).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders, never f-strings in SQL) —
  N/A directly here since no new queries are added, but `get_user_by_email`
  (reused) already follows this
- Passwords verified with `werkzeug.security.check_password_hash` against the
  stored `password_hash` — never compare plaintext passwords
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic lives only in `database/db.py`, never inline in `app.py`
- Use `url_for()` for all internal links — never hardcode URLs
- On login failure (unknown email OR wrong password), show one single generic
  error message — do not reveal whether the email exists, to avoid user
  enumeration
- On validation failure, re-render `login.html` with an `error` message and
  preserve the previously entered `email` — do not redirect
- On success, store the user's id in `session["user_id"]` (same key
  registration already uses) and redirect to `/profile`
- `logout()` must clear `session["user_id"]` (e.g. `session.pop("user_id",
  None)`) and redirect to the landing page (`/`) — must not error if the user
  was already logged out

## Definition of done
- [ ] Submitting the login form with the seeded demo user's credentials
      (`demo@spendly.com` / `demo123`) logs in successfully and redirects to
      `/profile`, with `session["user_id"]` set to that user's id
- [ ] Submitting with a correct email but wrong password shows a generic
      error on the same page, does not log in, and preserves the entered email
- [ ] Submitting with an email that doesn't exist shows the same generic
      error message (not a different one), and preserves the entered email
- [ ] Submitting with a missing email or password shows an error and does not
      attempt a DB lookup with empty values
- [ ] Visiting `/logout` after being logged in clears the session and
      redirects to `/`; visiting `/profile` afterward no longer reflects that
      session (manually verifiable once Step 4 exists, but for this step it's
      enough that `session.get("user_id")` is confirmed empty)
- [ ] Visiting `/logout` while not logged in does not raise an error and
      still redirects to `/`
- [ ] The login form's action uses `url_for('login')`, not a hardcoded string
- [ ] App starts without errors and `GET /login` still renders correctly
