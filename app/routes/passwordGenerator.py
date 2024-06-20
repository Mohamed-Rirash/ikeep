from fastapi import APIRouter, Depends, HTTPException, Query,status

from app.schemas.passwordgenerator import PasswordGeneratorRequest
from app.utils.password_chartset import easy, medium, hard
from app.services.passwordGenerator import generate_password

ppassword_generator_router = APIRouter(
    prefix="/passwordgenerator",
    tags=["passwordgenerator"],
    responses={404: {"description": "Not found"}},

)


@ppassword_generator_router.get("/generate")
async def generate_password_endpoint(
    mode: PasswordGeneratorRequest,
    length: int = Query(
        default=8, ge=8, description="Number of characters you want your password to be")
):
    if mode == PasswordGeneratorRequest.easy:
        char_set = easy
    elif mode == PasswordGeneratorRequest.medium:
        char_set = medium
    elif mode == PasswordGeneratorRequest.hard:
        char_set = hard
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Please choose a valid mode"
        )

    password = await generate_password(length, char_set)
    return {"password": password}
