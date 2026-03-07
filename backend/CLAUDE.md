# CLAUDE.md — fastapi-react-auth backend

## Project Overview
Async FastAPI backend with PostgreSQL, providing organization/user management and OTP-based authentication.

## Tech Stack
- **Framework**: FastAPI (async)
- **ORM**: SQLAlchemy (async) with `asyncpg`
- **Database**: PostgreSQL
- **Migrations**: Alembic (async mode)
- **Validation**: Pydantic v2
- **Runtime**: Python 3.10+

## Project Structure
```
backend/
└── app/
    ├── main.py              # App factory (create_app)
    ├── database.py          # Async engine, session, Base
    ├── api/v1/routes/       # FastAPI routers
    │   ├── users.py
    │   ├── organization.py
    │   ├── otp.py
    │   └── auth.py          # Not yet registered in main.py
    ├── service/             # Business logic layer
    ├── repository/          # DB query layer
    ├── model/               # SQLAlchemy ORM models
    │   ├── common.py        # CommonBase mixin
    │   ├── user.py
    │   ├── organization.py
    │   └── otp.py
    ├── schema/              # Pydantic request/response schemas
    └── migrations/alembic/  # Alembic migration scripts
```

## Architecture Pattern
```
routes → service → repository → model
```
- Routes handle HTTP, delegate to services
- Services contain business logic, raise `ValueError` for domain errors
- Repositories contain all SQLAlchemy queries
- Routes catch `ValueError` and raise `HTTPException`

## Key Conventions

### Models
- All models inherit `CommonBase` + `Base`
- `CommonBase` provides: `id` (str, UUID PK), `created_at`, `updated_at`, `status` (bool)
- **Exception**: `OTP.status` is `OTPStatusEnum`, overriding `CommonBase.status`
- UUIDs are generated in the repository layer: `str(uuid.uuid4())`
- Soft deletes: set `instance.status = False`, never hard delete

### Schemas
- `UserCreate` / `UserResponse`, `OrganizationCreate` / `OrganizationResponse`, `OtpRequest` / `OtpVerifyRequest` / `OtpResponse`
- ORM → Pydantic: always use `Model.model_validate(orm_obj)`
- Response schemas include `status`, `created_at`, `updated_at`

### Database
- `DATABASE_URL` loaded from `.env` (default: `postgresql+asyncpg://myuser:mypassword@127.0.0.1:5432/mydatabase`)
- Session: `AsyncSession`, `expire_on_commit=False`
- SQL echo enabled (disable in production)

### Migrations
Run from `backend/` directory:
```bash
# Generate migration
alembic -c app/alembic.ini revision --autogenerate -m "description"

# Apply migrations
alembic -c app/alembic.ini upgrade head
```

## Running the Server
```bash
cd backend
uvicorn app.main:app --reload --log-level debug
```

API docs: `http://localhost:8000/api/docs`

## API Routes
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/organizations/` | Create org |
| GET | `/api/organizations/` | List all orgs |
| GET | `/api/organizations/{org_id}` | Get org |
| PUT | `/api/organizations/{org_id}` | Update org |
| DELETE | `/api/organizations/{org_id}` | Soft-delete org |
| POST | `/api/users/` | Create user |
| GET | `/api/users/{org_id}` | List users in org |
| GET | `/api/users/{user_id}/{org_id}` | Get user |
| PUT | `/api/users/{user_id}/{org_id}` | Update user |
| DELETE | `/api/users/{user_id}/{org_id}` | Soft-delete user |
| POST | `/api/otp/send` | Send OTP |
| POST | `/api/otp/verify` | Verify OTP |

## OTP Flow
1. `POST /api/otp/send` — validates user+org exist, generates 5-digit code via `secrets.randbelow`, stores with 5-min expiry
2. `POST /api/otp/verify` — validates code, checks expiry, marks status `VERIFIED`
3. SMS delivery is a TODO (Twilio integration placeholder in `otp.py`)

## Dependencies
See `app/requirement.txt`. Key packages: `fastapi`, `sqlalchemy`, `asyncpg`, `alembic`, `pydantic[email]`, `python-dotenv`.
