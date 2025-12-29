# FastAPI Debugging Guide

A comprehensive guide to debugging FastAPI applications with various methods and tools.

## Table of Contents
1. [Basic Logging](#1-basic-logging)
2. [Using Python Debugger (pdb)](#2-using-python-debugger-pdb)
3. [VS Code Debugging](#3-vs-code-debugging)
4. [PyCharm Debugging](#4-pycharm-debugging)
5. [Request/Response Inspection](#5-requestresponse-inspection)
6. [Database Query Debugging](#6-database-query-debugging)
7. [Exception Handling](#7-exception-handling)
8. [Performance Debugging](#8-performance-debugging)

---

## 1. Basic Logging

### Already Configured!
The application now has logging configured in `main.py` with request/response middleware.

### Usage in Routes

```python
import logging

logger = logging.getLogger(__name__)

@router.get("/{org_id}")
async def get_organization(org_id: str):
    logger.info(f"Fetching organization: {org_id}")
    logger.debug(f"Additional debug info: {some_variable}")
    logger.warning(f"Warning message")
    logger.error(f"Error occurred: {error}")
```

### Log Levels
```bash
# Run with different log levels
uvicorn app.main:app --reload --log-level debug    # Most verbose
uvicorn app.main:app --reload --log-level info     # Default
uvicorn app.main:app --reload --log-level warning
uvicorn app.main:app --reload --log-level error
```

### What You'll See
```
2025-12-29 10:30:45 - app.main - INFO - Creating FastAPI application...
2025-12-29 10:30:45 - app.main - DEBUG - Request: GET http://localhost:8000/api/organizations/123
2025-12-29 10:30:45 - app.api.v1.routes.organization - INFO - Fetching organization with ID: 123
```

---

## 2. Using Python Debugger (pdb)

### Interactive Debugging with pdb

Add breakpoints directly in your code:

```python
@router.get("/{org_id}")
async def get_organization(org_id: str, db: AsyncSession = Depends(get_db)):
    # Add a breakpoint
    import pdb; pdb.set_trace()

    # Code execution will pause here
    result = await OrganizationService(db).get_org(org_id)
    return result
```

### Or use `breakpoint()` (Python 3.7+)

```python
@router.get("/{org_id}")
async def get_organization(org_id: str):
    breakpoint()  # Modern way - cleaner syntax
    result = await OrganizationService(db).get_org(org_id)
    return result
```

### pdb Commands
```
(Pdb) n          # Next line
(Pdb) s          # Step into function
(Pdb) c          # Continue execution
(Pdb) l          # List code around current line
(Pdb) p var      # Print variable
(Pdb) pp var     # Pretty print variable
(Pdb) w          # Show stack trace
(Pdb) q          # Quit debugger
```

### Install ipdb for Better Experience
```bash
pip install ipdb

# Use it in code
import ipdb; ipdb.set_trace()
```

---

## 3. VS Code Debugging

### Step 1: Create Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "jinja": true,
            "justMyCode": true,
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

### Step 2: Set Breakpoints
- Click in the gutter (left of line numbers) to set breakpoints
- Red dots will appear

### Step 3: Start Debugging
- Press `F5` or click "Run and Debug"
- Make a request to your API
- Execution will pause at breakpoints

### Debug Controls
- `F5` - Continue
- `F10` - Step Over
- `F11` - Step Into
- `Shift+F11` - Step Out
- `Shift+F5` - Stop Debugging

### Inspect Variables
- Hover over variables to see values
- Use the "Variables" panel
- Use the "Debug Console" to evaluate expressions

---

## 4. PyCharm Debugging

### Step 1: Create Run Configuration
1. Click "Add Configuration" in the top right
2. Click "+" and select "Python"
3. Configure:
   - **Script path**: Select `uvicorn`
   - **Parameters**: `app.main:app --reload --host 0.0.0.0 --port 8000`
   - **Working directory**: `/path/to/backend`
   - **Python interpreter**: Your virtual environment

### Step 2: Set Breakpoints
- Click in the gutter to set breakpoints

### Step 3: Debug
- Click the debug icon (bug symbol)
- Make requests to your API

---

## 5. Request/Response Inspection

### Using Middleware (Already Added!)

The middleware in `main.py` logs all requests:

```python
@app.middleware("http")
async def log_requests(request, call_next):
    logger.debug(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {request.headers}")
    response = await call_next(request)
    logger.debug(f"Response status: {response.status_code}")
    return response
```

### Inspect Request in Route

```python
from fastapi import Request

@router.post("/")
async def create_org(request: Request, org: OrganizationCreate):
    # Access request details
    logger.debug(f"Headers: {request.headers}")
    logger.debug(f"Client: {request.client.host}")
    logger.debug(f"Body: {await request.body()}")  # Raw body
    logger.debug(f"Parsed data: {org.model_dump()}")

    # Process request
    result = await service.create_org(org)
    return result
```

### Use FastAPI's Interactive Docs

Navigate to `http://localhost:8000/api/docs` to:
- Test endpoints interactively
- See request/response schemas
- Inspect validation errors
- Try different inputs

---

## 6. Database Query Debugging

### SQL Echo (Already Enabled!)

In `database.py`, SQL echo is enabled:

```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # This logs all SQL queries
)
```

You'll see SQL queries in the console:
```sql
INFO sqlalchemy.engine.Engine BEGIN (implicit)
INFO sqlalchemy.engine.Engine SELECT * FROM organizations WHERE id = $1
INFO sqlalchemy.engine.Engine [generated in 0.00012s] ('123',)
```

### Disable in Production
For production, disable SQL echo:
```python
engine = create_async_engine(DATABASE_URL, echo=False)
```

### Debug Queries in Repository

```python
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

async def get_org_by_id(self, org_id: str):
    stmt = select(Organization).where(Organization.id == org_id)

    # Log the query
    logger.debug(f"Executing query: {stmt}")

    result = await self.db.execute(stmt)
    org = result.scalar_one_or_none()

    logger.debug(f"Query result: {org}")
    return org
```

---

## 7. Exception Handling

### Global Exception Handler

Add to `main.py`:

```python
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {exc}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if app.debug else "An error occurred"
        }
    )
```

### Detailed Error Responses (Development)

```python
@router.get("/{org_id}")
async def get_organization(org_id: str):
    try:
        result = await service.get_org(org_id)
        return result
    except ValueError as e:
        logger.error(f"ValueError: {e}", exc_info=True)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")  # Logs full traceback
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 8. Performance Debugging

### Time Function Execution

```python
import time
from functools import wraps

def time_it(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@time_it
async def get_org(self, org_id: str):
    return await self.repository.get_org_by_id(org_id)
```

### Profile with cProfile

```bash
python -m cProfile -o profile.stats -m uvicorn app.main:app

# Analyze results
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"
```

### Monitor Memory Usage

```python
import tracemalloc

tracemalloc.start()

# Your code here

current, peak = tracemalloc.get_traced_memory()
logger.info(f"Current memory: {current / 10**6:.2f} MB")
logger.info(f"Peak memory: {peak / 10**6:.2f} MB")

tracemalloc.stop()
```

---

## Quick Debugging Checklist

1. **First Step**: Check logs
   ```bash
   uvicorn app.main:app --reload --log-level debug
   ```

2. **API Not Working?**
   - Check `http://localhost:8000/api/docs`
   - Test endpoint directly in Swagger UI
   - Check request/response in browser Network tab

3. **Database Issues?**
   - Check SQL echo in logs
   - Verify database connection in `.env`
   - Test connection: `psql -U admin -d db -h localhost`

4. **Logic Errors?**
   - Add `logger.debug()` statements
   - Use `breakpoint()` for interactive debugging
   - Use VS Code debugger with breakpoints

5. **Performance Issues?**
   - Enable SQL echo to see slow queries
   - Use `@time_it` decorator
   - Check for N+1 query problems

---

## Common Debug Scenarios

### Scenario 1: Endpoint Returns 404

```python
@router.get("/{org_id}")
async def get_organization(org_id: str):
    logger.info(f"Requested org_id: {org_id}, type: {type(org_id)}")
    # Check if ID format matches database
```

### Scenario 2: Database Query Returns None

```python
async def get_org_by_id(self, org_id: str):
    logger.debug(f"Searching for org_id: {org_id}")
    result = await self.db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()
    logger.debug(f"Found organization: {org}")
    if not org:
        logger.warning(f"Organization {org_id} not found in database")
    return org
```

### Scenario 3: Validation Error

```python
@router.post("/")
async def create_organization(org: OrganizationCreate):
    logger.debug(f"Received data: {org.model_dump()}")
    # If validation fails, FastAPI will return 422 with details
```

---

## Best Practices

1. **Use appropriate log levels**:
   - `DEBUG` - Detailed info for diagnosing problems
   - `INFO` - General informational messages
   - `WARNING` - Warning messages
   - `ERROR` - Error messages
   - `CRITICAL` - Critical errors

2. **Remove debug code before production**:
   - Remove `breakpoint()` and `pdb.set_trace()`
   - Disable SQL echo
   - Set log level to INFO or WARNING

3. **Use structured logging**:
   ```python
   logger.info("Organization created", extra={
       "org_id": org.id,
       "user_id": current_user.id
   })
   ```

4. **Don't log sensitive data**:
   - Avoid logging passwords, tokens, or PII
   - Use `***` to mask sensitive fields

5. **Use exception handlers**:
   - Catch specific exceptions
   - Log full traceback with `logger.exception()`
   - Return user-friendly error messages

---

## Additional Tools

### HTTPie (Command-line HTTP client)
```bash
pip install httpie

# Test your API
http GET localhost:8000/api/organizations/123
http POST localhost:8000/api/organizations/ id=123 org_name="Test"
```

### Postman
- Visual API testing
- Save requests and organize collections
- Environment variables for different configs

### FastAPI TestClient
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_organization():
    response = client.get("/api/organizations/123")
    print(response.json())
    assert response.status_code == 200
```

---

## Need More Help?

- FastAPI docs: https://fastapi.tiangolo.com/
- SQLAlchemy debugging: https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging
- Python logging: https://docs.python.org/3/library/logging.html
