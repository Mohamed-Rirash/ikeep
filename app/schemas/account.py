from pydantic import BaseModel, HttpUrl, EmailStr


class AddNewAcountRequest(BaseModel):
    web_name: str
    url: HttpUrl
    email: EmailStr
    password: str
