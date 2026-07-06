# Spec: Profile

## Overview
This step implements the `/profile` route, replacing its current raw-string
stub with a real page that shows the logged-in user's account details (name,
email, member-since date). It is the first route that requires
authentication — visiting it while logged out must redirect to `/login`
rather than error or expose data. Profile is the landing page users reach
immediately after registration or login (both already redirect to
`url_for("profile")`), and it establishes the "logged-in" layout/nav pattern
that later expense-management routes (Steps 7–9) will reuse.

## Depends on
- Step 1 (Database Setup) — requires `get_db()` and the `users` table.
- Step 2 (Registration) — requires `create_user()` and the `session["user_id"]`
  pattern established at signup.
- Step 3 (Login and Logout) — requires working `/login` (to redirect to when
  logged out) and `/logout` (to link to from the profile page nav).

## Routes
- `GET /profile` — show the logged-in user's name, email, and member-since
  date; redirect to `/login` if no `session["user_id"]` is present —
  logged-in only

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`,
`password_hash`, `created_at`) already has everything the profile page needs.
No new `db.py` function exists yet to fetch a user by id — see below.

## Templates
- **Create:** `templates/profile.html` — displays the user's name, email, and
  `created_at` (member-since), with a link to `{{ url_for('logout') }}`
- **Modify:** `templates/base.html` — the navbar currently hardcodes the
  logged-out state (`Sign in` / `Get started` links) on every page. Add a
  conditional block driven by a `logged_in` (or equivalent) value so that
  when set, the nav shows a link to `{{ url_for('profile') }}` and
  `{{ url_for('logout') }}` instead. Keep the change minimal — only branch the
  `nav-links` block, don't restructure the rest of the layout.

## Files to change
- `app.py` — implement `profile()`: check `session.get("user_id")`, redirect
  to `url_for("login")` if absent; otherwise fetch the user via a new
  `get_user_by_id()` helper and render `profile.html` with the user data
- `database/db.py` — add `get_user_by_id(user_id)`, mirroring the existing
  `get_user_by_email()` pattern (parameterized query, returns a row or `None`)
- `templates/base.html` — add the logged-in/logged-out nav branch described
  above

## Files to create
- `templates/profile.html` — new page extending `base.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders, never f-strings in SQL)
- Passwords hashed with werkzeug — N/A here (no password handling in this
  step), but never display `password_hash` in the template
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic lives only in `database/db.py` — `get_user_by_id()` must live
  there, never as an inline query in `app.py`
- Use `url_for()` for all internal links — never hardcode URLs
- `profile()` must redirect unauthenticated visitors to `/login` — never
  render the page or leak user data without a valid `session["user_id"]`
- If `session["user_id"]` refers to a user id that no longer exists (edge
  case), treat it the same as logged-out: clear the stale session key and
  redirect to `/login` rather than raising an error
- Keep `base.html` changes scoped to the nav — don't introduce new global
  layout structures

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Logging in with the seeded demo user (`demo@spendly.com` / `demo123`)
      and being redirected to `/profile` shows that user's name, email, and
      member-since date
- [ ] Registering a new account and being redirected to `/profile` shows the
      newly created user's own name and email (not the demo user's)
- [ ] The profile page's nav includes a working link to `/logout`, and
      clicking it clears the session and lands on the landing page
- [ ] No `password_hash` value appears anywhere in the rendered HTML
- [ ] App starts without errors and previously working routes (`/`,
      `/register`, `/login`, `/logout`) still behave as before
