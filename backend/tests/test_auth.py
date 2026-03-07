import uuid

import pytest

from app.model.organization import Organization
from app.model.user import User, ThemeEnum


async def _seed_user(db_session):
    org = Organization()
    org.id = str(uuid.uuid4())
    org.org_code = "TESTORG"
    org.org_name = "Test Organization"
    org.org_website = None
    org.status = True
    db_session.add(org)
    await db_session.flush()

    user = User()
    user.id = str(uuid.uuid4())
    user.organization_id = org.id
    user.name = "Test User"
    user.email = "test@example.com"
    user.phone = "1234567890"
    user.theme = ThemeEnum.light
    user.status = True
    db_session.add(user)
    await db_session.commit()
    return org, user


class TestLogin:
    async def test_login_unknown_email_returns_401(self, client):
        response = await client.post(
            "/api/auth/login",
            json={"email": "nobody@example.com", "org_code": "NOPE"},
        )
        assert response.status_code == 401

    async def test_login_wrong_org_code_returns_401(self, client, db_session):
        await _seed_user(db_session)
        response = await client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "org_code": "WRONG"},
        )
        assert response.status_code == 401

    async def test_login_valid_returns_otp_id(self, client, db_session):
        await _seed_user(db_session)
        response = await client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "org_code": "TESTORG"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "OTP sent successfully"
        assert "otp_id" in data
        assert data["otp_id"] is not None


class TestRefresh:
    async def test_refresh_with_garbage_token_returns_401(self, client):
        response = await client.post(
            "/api/auth/refresh",
            json={"refresh_token": "not.a.token"},
        )
        assert response.status_code == 401

    async def test_refresh_with_access_token_returns_401(self, client, db_session):
        """Access tokens must not be accepted as refresh tokens."""
        from app.service.auth import _create_token
        from datetime import timedelta

        token = _create_token(
            {"sub": "user-id", "type": "access", "theme": "light", "org_id": "o", "org_code": "X"},
            timedelta(minutes=15),
        )
        response = await client.post(
            "/api/auth/refresh",
            json={"refresh_token": token},
        )
        assert response.status_code == 401


class TestProtectedRoutes:
    async def test_users_route_requires_auth(self, client):
        response = await client.get("/api/users/some-org-id")
        assert response.status_code == 401

    async def test_organizations_route_requires_auth(self, client):
        response = await client.get("/api/organizations/some-org-id")
        assert response.status_code == 401

    async def test_users_route_rejects_invalid_token(self, client):
        response = await client.get(
            "/api/users/some-org-id",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401
