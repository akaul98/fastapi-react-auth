# Backend TODO — Pending Improvements

## Bugs

### #28 — Wrong column in login query
**File:** `app/repository/auth.py:18`

`Organization.id == org_code` compares the UUID primary key against the org_code string.
Should be:
```python
Organization.org_code == org_code
```
This means login currently only works if the client passes the org's UUID, not its human-readable code.

---

## Security (High Priority)

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

### #29 — No logout / token revocation
There is no `POST /api/auth/logout` endpoint and no token blacklist.
An access token remains valid for 15 minutes after logout; a refresh token for 7 days.
Fix: Introduce a Redis-backed blacklist and check it in `get_current_user`.

### #30 — OTP brute force not fully mitigated
Rate limiting is per IP (5/minute). An attacker rotating IPs can still brute-force a 5-digit OTP (100,000 combinations).
Fix: Track failed OTP attempts per `user_id` in the DB or Redis and lock after N failures.

---

## Configuration

### #31 — No .env.example
There is no template documenting required environment variables.
Fix: Add `.env.example` with:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db
JWT_SECRET_KEY=changeme
CORS_ORIGINS=http://localhost:3000
SQL_ECHO=false
APP_DEBUG=false
```

---

## Code Quality

### #8 — Unused `self.db` in services
**File:** `app/service/userService.py:8`, `app/service/otp.py:8`

Both services store `self.db = db` in `__init__` but only use `self.repo`.
Fix: Remove the `self.db = db` line in both.

### #18 — Inconsistent filename casing
**File:** `app/service/userService.py`

All other service files use snake_case (`organization.py`, `otp.py`, `auth.py`).
Fix: Rename to `user_service.py` and update the import in `routes/users.py`.

### #19 — Inconsistent route function naming
**File:** `app/api/v1/routes/users.py`

Functions use camelCase (`getAllUsers`, `getUserById`, etc.)
while `organization.py` uses snake_case. FastAPI function names appear in tracebacks and logs.
Fix: Rename to snake_case (`get_all_users`, `get_user_by_id`, etc.).

### #20 — Unnecessary try/except in create_org
**File:** `app/repository/organization.py:20-23`

```python
try:
    payload = org_data.model_dump()
except Exception:
    raise ValueError("Invalid organization data")
```
`model_dump()` on a valid Pydantic model never raises. This swallows real errors (DB errors,
attribute errors) and replaces them with a misleading message.
Fix: Remove the try/except entirely.

### #21 — Dead return value in OtpService.verify_otp
**File:** `app/service/otp.py:57`

The dict returned includes `"verified": True`, but the route handler only reads
`message` and `otp_id`. The `verified` key is never used.
Fix: Remove it from the return dict.

### #22 — Duplicate OTP verification flows
**File:** `app/service/otp.py`, `app/service/auth.py`

`POST /api/otp/verify` (OtpService) and `POST /api/auth/verify` (AuthService) both call
`OtpRepository.verify_otp`. The difference is only the response shape (OtpResponse vs TokenResponse).
Consider removing `POST /api/otp/verify` entirely and making `/api/auth/verify` the single verify endpoint.

### #32 — POST create endpoints return 200 instead of 201
**File:** `app/api/v1/routes/users.py:27`, `app/api/v1/routes/organization.py:25`

`create_user` and `create_org` do not declare `status_code=201`.
Fix:
```python
@router.post("create_user", response_model=UserResponse, status_code=201)
```

### Unused imports
- `app/repository/otp.py:1` — `import time` is unused, remove it.
- `app/schema/users.py:3` — `BaseModel, ConfigDict` are imported but unused since
  schemas extend `BaseSchema`. Remove them.

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
