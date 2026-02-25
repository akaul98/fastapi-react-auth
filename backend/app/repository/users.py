
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.users import UserCreate, UserResponse
from app.model.user import User
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self, org_id: str) -> list[UserResponse]:
        result = await self.db.execute(select(User).where(
        (User.status == True) & 
        (User.organization_id == org_id)
    )
)

        return list(result.scalars().all())
    
    async def get_user_by_id(self, user_id: str, org_id: str) -> UserResponse | None:
        result =await self.db.execute(select(User).where((User.id == user_id) & (User.organization_id == org_id)))
        return result.scalars().first()
    
    async def delete_user_by_id(self, user_id: str, org_id: str) -> None:
        user = await self.get_user_by_id(user_id, org_id)
        if user:
            user.status = False
            await self.db.commit()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        new_user = UserResponse(**user_data.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def update_user(self, user_id: str, org_id: str, user_data: UserCreate) -> UserResponse | None:
        user = await self.get_user_by_id(user_id, org_id)
        if user:
            for key, value in user_data.model_dump().items():
                setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user