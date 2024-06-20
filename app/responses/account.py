from pydantic import BaseModel
from typing import List


class NewAccountResponse(BaseModel):
    id: int
    web_name: str
    url: str
    email: str
    password: str  # Include password field if needed


AccountsResponse = List[NewAccountResponse]
