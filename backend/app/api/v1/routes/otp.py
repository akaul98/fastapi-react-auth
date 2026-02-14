from fastapi import APIRouter


router=APIRouter()

@router.post("/sendOtp")
async def sendOtp():

