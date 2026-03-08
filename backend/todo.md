# Backend TODO — Pending Improvements

## Security (High Priority)

### #15 — No JWT auth middleware on protected routes
**File:** `app/api/v1/routes/`

All routes are currently unprotected. There is no `get_current_user` dependency.
Fix: Create a `get_current_user` dependency that decodes the access token and
inject it into routes that require authentication.

### #27 — OTP not invalidated after use
**File:** `app/repository/otp.py`

After a successful `POST /api/auth/verify`, the verified OTP record remains in
`VERIFIED` status and can be re-submitted to `POST /api/otp/verify`.
Fix: Check that the OTP has not already been used for token generation, or
add a `used_at` timestamp and reject re-use.

---

## Configuration

### #16 — SQL echo always enabled
**File:** `app/database.py:10`

`echo=True` logs every SQL query including values, leaking sensitive data in production.
Fix:
```python
engine = create_async_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "false") == "true")
```

### #17 — debug=True hardcoded in app
**File:** `app/main.py:26`

`debug=True` exposes stack traces in HTTP error responses.
Fix:
```python
debug=os.getenv("APP_DEBUG", "false") == "true"
```

---

## Code Quality

### #8 (Remaining) — Redundant logic in UserService.delete_user_by_id
**File:** `app/service/userService.py:19-24`

`user.status = False` on line 22 is set before calling `self.repo.delete_user_by_id`,
which fetches the user again and also sets `status = False`. The status assignment
in the service is redundant and causes the user to be fetched twice.
Also, `self.db` stored in `__init__` is now unused.
Fix: Remove line 22 (`user.status = False`) and the `self.db = db` assignment.

### #18 — Inconsistent filename casing
**File:** `app/service/userService.py`

All other service files use snake_case (`organization.py`, `otp.py`, `auth.py`).
Fix: Rename to `user.py` or `user_service.py` and update the import in `routes/users.py`.

### #19 — Inconsistent route function naming
**File:** `app/api/v1/routes/users.py`

Functions use camelCase (`getAllUsers`, `getUserById`, `deleteUserById`, `createUser`, `updateUser`)
while `organization.py` uses snake_case. FastAPI function names show up in tracebacks and logs.
Fix: Rename to snake_case (`get_all_users`, `get_user_by_id`, etc.).

### #20 — Unnecessary try/except in create_org
**File:** `app/repository/organization.py:20-23`

```python
try:
    payload = org_data.model_dump()
except Exception:
    raise ValueError("Invalid organization data")
```
`model_dump()` on a valid Pydantic model never raises a generic `Exception`.
This swallows real errors (e.g. DB errors, attribute errors) and replaces them with a misleading message.
Fix: Remove the try/except entirely.

### #21 — Dead return value in OtpService.verify_otp
**File:** `app/service/otp.py:56`

The dict returned includes `"verified": True`, but the route handler only reads
`message` and `otp_id`. The `verified` key is never used.
Fix: Remove it from the return dict.

### #22 — Duplicate OTP verification flows
**File:** `app/service/otp.py`, `app/service/auth.py`

`POST /api/otp/verify` (OtpService) and `POST /api/auth/verify` (AuthService) both verify
OTPs using `OtpRepository.verify_otp`. The difference is only the response shape.
Consider consolidating or clearly documenting which endpoint is intended for which flow.

### Unused imports (new)
- `app/repository/otp.py:1` — `import time` is unused, should be removed.
- `app/schema/users.py:3` — `BaseModel, ConfigDict` are imported but unused since
  schemas now extend `BaseSchema`.

---

## Missing Features

### #23 — No pagination on list endpoints
**File:** `app/repository/users.py`, `app/repository/organization.py`

`get_all_users` and `get_all_orgs` return all rows with no limit.
Fix: Add `limit` and `offset` (or cursor) parameters.

### #24 — No phone number format validation
**File:** `app/schema/users.py`, `app/schema/otp.py`

`phone` and `phone_number` are plain `str` with no format check.
Fix: Use `pydantic-extra-types` `PhoneNumber` type or a regex validator.

### #25 — No health check endpoint
Fix: Add `GET /api/health` returning `{"status": "ok"}`, useful for load balancers
and deployment readiness probes.

### #26 — No database connection pool configuration
**File:** `app/database.py`

`create_async_engine` uses asyncpg defaults. Under load this can exhaust connections.
Fix: Configure explicitly:
```python
create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)
```