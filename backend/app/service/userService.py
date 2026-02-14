from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users import UserRepository
from app.schema.users.main import UserCreate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)

    async def get_all_users(self, org_id: str) -> list[UserResponse]:
        users = await self.repo.get_all_users(org_id)
        return [UserResponse.model_validate(user) for user in users]
    
    async def get_user_by_id(self, user_id: str, org_id: str) -> UserResponse:
        user = await self.repo.get_user_by_id(user_id, org_id)
        return UserResponse.model_validate(user)
    
    async def delete_user_by_id(self, user_id: str, org_id: str) -> None:
        user = await self.repo.get_user_by_id(user_id, org_id)
        if user:
            user.status = False
            await self.db.commit()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = await self.repo.create_user(user_data)
        return UserResponse.model_validate(user)
    
    async def update_user(self, user_id: str, org_id: str, user_data: UserCreate) -> UserResponse:
        user = await self.repo.update_user(user_id, org_id, user_data)
        return UserResponse.model_validate(user)