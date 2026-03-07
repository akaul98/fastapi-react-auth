import uuid

import pytest

from app.model.organization import Organization
from app.model.otp import OTP, OTPStatusEnum
from app.model.user import User, ThemeEnum


async def _seed_user(db_session, org_code="OTPTEST", email="otp@example.com"):
    org = Organization()
    org.id = str(uuid.uuid4())
    org.org_code = org_code
    org.org_name = "OTP Test Org"
    org.org_website = None
    org.status = True
    db_session.add(org)
    await db_session.flush()

    user = User()
    user.id = str(uuid.uuid4())
    user.organization_id = org.id
    user.name = "OTP User"
    user.email = email
    user.phone = "9876543210"
    user.theme = ThemeEnum.light
    user.status = True
    db_session.add(user)
    await db_session.commit()
    return org, user


class TestOtpSend:
    async def test_send_unknown_user_returns_400(self, client):
        response = await client.post(
            "/api/otp/send",
            json={"user_id": "nope", "organization_id": "nope", "phone_number": "0000"},
        )
        assert response.status_code == 400

    async def test_send_valid_returns_otp_id(self, client, db_session):
        org, user = await _seed_user(db_session)
        response = await client.post(
            "/api/otp/send",
            json={"user_id": user.id, "organization_id": org.id, "phone_number": user.phone},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "OTP sent successfully"
        assert data["otp_id"] is not None

    async def test_second_send_expires_first_otp(self, client, db_session):
        from sqlalchemy import select

        org, user = await _seed_user(db_session, org_code="EXPIRE", email="expire@example.com")
        payload = {"user_id": user.id, "organization_id": org.id, "phone_number": user.phone}

        r1 = await client.post("/api/otp/send", json=payload)
        r2 = await client.post("/api/otp/send", json=payload)

        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r1.json()["otp_id"] != r2.json()["otp_id"]

        # First OTP should now be EXPIRED
        first_id = r1.json()["otp_id"]
        result = await db_session.execute(select(OTP).where(OTP.id == first_id))
        first_otp = result.scalar_one()
        assert first_otp.status == OTPStatusEnum.EXPIRED


class TestOtpVerify:
    async def test_verify_wrong_code_returns_400(self, client, db_session):
        org, user = await _seed_user(db_session, org_code="VFY1", email="vfy1@example.com")
        await client.post(
            "/api/otp/send",
            json={"user_id": user.id, "organization_id": org.id, "phone_number": user.phone},
        )
        response = await client.post(
            "/api/otp/verify",
            json={
                "user_id": user.id,
                "organization_id": org.id,
                "phone_number": user.phone,
                "otp_code": "00000",
            },
        )
        assert response.status_code == 400

    async def test_verify_correct_code_succeeds(self, client, db_session):
        from sqlalchemy import select

        org, user = await _seed_user(db_session, org_code="VFY2", email="vfy2@example.com")
        await client.post(
            "/api/otp/send",
            json={"user_id": user.id, "organization_id": org.id, "phone_number": user.phone},
        )

        # Retrieve the actual code from DB
        result = await db_session.execute(
            select(OTP).where(OTP.user_id == user.id, OTP.status == OTPStatusEnum.PENDING)
        )
        otp = result.scalar_one()

        response = await client.post(
            "/api/otp/verify",
            json={
                "user_id": user.id,
                "organization_id": org.id,
                "phone_number": user.phone,
                "otp_code": otp.code,
            },
        )
        assert response.status_code == 200
        assert response.json()["message"] == "OTP verified successfully"
