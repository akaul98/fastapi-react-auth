# FastAPI React Auth - Backend

A modern, high-performance backend API built with FastAPI, featuring async SQLAlchemy, JWT authentication, and PostgreSQL database.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [API Endpoints](#api-endpoints)

## Features

- **Async FastAPI** - High-performance async web framework
- **PostgreSQL** - Robust relational database with async support
- **SQLAlchemy ORM** - Modern async ORM with type hints
- **JWT Authentication** - Secure token-based authentication (in development)
- **Database Migrations** - Alembic for version-controlled schema changes
- **Clean Architecture** - Layered architecture with repositories, services, and routes
- **API Documentation** - Auto-generated Swagger UI and ReDoc
- **Type Safety** - Pydantic schemas for request/response validation

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Authentication**: Python-jose (JWT), Passlib (bcrypt)
- **Validation**: Pydantic
- **Testing**: pytest, httpx

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # Application entry point
│   ├── database.py             # Database configuration
│   │
│   ├── api/                    # API routes
│   │   └── v1/
│   │       └── routes/
│   │           ├── users.py           # User endpoints
│   │           ├── organization.py    # Organization endpoints
│   │           └── auth.py            # Authentication endpoints
│   │
│   ├── model/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── organization.py
│   │   └── otp.py
│   │
│   ├── schema/                 # Pydantic schemas
│   │   └── organization/
│   │       └── main.py
│   │
│   ├── service/                # Business logic layer
│   │   └── organization.py
│   │
│   ├── repository/             # Data access layer
│   │   └── organization.py
│   │
│   └── migrations/             # Alembic migrations
│       └── alembic/
│           └── versions/
│
├── alembic.ini                 # Alembic configuration
├── requirement.txt             # Python dependencies
└── .env                        # Environment variables
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-react-auth/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   cd app
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Database Setup

### Database Configuration

The application uses PostgreSQL with async support. Update your `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/dbname
```

### Running Migrations

Create a new migration after model changes:
```bash
cd app
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

Rollback a migration:
```bash
alembic downgrade -1
```

### Database Schema

**Organizations Table**
- `id` (String, Primary Key)
- `org_code` (String)
- `org_name` (String)
- `org_website` (String, Optional)
- `status` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**Users Table**
- `id` (String, Primary Key)
- `organization_id` (String, Foreign Key)
- `email` (String, Unique)
- `phone` (String)
- `status` (Boolean)
- `theme` (Enum: light/dark)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**OTP Table**
- `id` (String, Primary Key)
- `phone` (String, Indexed)
- `code` (String, max 5 chars)
- `created_at` (DateTime)
- `expires_at` (DateTime)
- `used` (Boolean)

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://admin:admin@127.0.0.1:5432/db` |

**Production Notes:**
- Change default database credentials
- Disable SQL echo in `database.py`
- Set up proper secret keys for JWT
- Use environment-specific configurations

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 style guidelines. Consider using:
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Adding a New Module

1. Create model in `app/model/`
2. Create Pydantic schemas in `app/schema/`
3. Create repository in `app/repository/`
4. Create service in `app/service/`
5. Create routes in `app/api/v1/routes/`
6. Register router in `app/main.py`
7. Generate migration: `alembic revision --autogenerate -m "add new module"`

## API Endpoints

### Organizations

- `GET /api/organizations/{org_id}` - Get organization by ID
  - **Response**: `200 OK` - Organization details
  - **Error**: `404 Not Found` - Organization doesn't exist

### Users (In Development)

- `GET /api/users/` - List all users
- `GET /api/users/id/` - Get user by ID
- `POST /api/users/create` - Create new user
- `PUT /api/users/update` - Update user
- `DELETE /api/users/delete` - Delete user

### Authentication (Planned)

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout

## Architecture

The project follows Clean Architecture principles with clear separation of concerns:

- **Routes**: HTTP request/response handling
- **Schemas**: Request/response validation and serialization
- **Services**: Business logic and orchestration
- **Repositories**: Database queries and data access
- **Models**: SQLAlchemy ORM definitions

### Async Support

The entire stack is async-enabled:
- FastAPI async route handlers
- SQLAlchemy async engine and sessions
- Asyncpg PostgreSQL driver

This provides excellent performance for I/O-bound operations.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Specify your license here]

## Contact

[Your contact information]