from fastapi import APIRouter

router=APIRouter()

@router.get("/")
async def read_user():
  return [{"Name":"Jon Doe"},{"Name":"Jane Doe"}]

@router.get("/id/")
async def read_user_by_id():
  return [{"Name:Jon Doe"},{"Name":"Jane Doe"}]

@router.post("create")
async def create_user():
  return [{"Name:Jon Doe"},{"Name":"Jane Doe"}]

@router.put("update")
async def update_user():
  return [{"Name:Jon Doe"},{"Name":"Jane Doe"}]

@router.delete("delete")
async def delete_user():
  return [{"Name:Jon Doe"},{"Name":"Jane Doe"}]
