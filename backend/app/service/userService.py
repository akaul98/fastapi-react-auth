from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repository.users import UserRepository
from backend.app.schema.users.main import UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)

    async def get_all_users(self, org_id: str) -> list[UserResponse]:
        users = await self.repo.get_all_users(org_id)
        return [UserResponse.model_validate(user) for user in users]