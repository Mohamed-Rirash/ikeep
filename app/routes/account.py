# from typing import Optional
# from fastapi import APIRouter, Depends, Query,status,HTTPException
# from sqlalchemy.orm import Session

# from app.config.database import get_session
# from app.config.security import get_current_user
# from app.models.user import User
# from app.responses.account import AccountsResponse
# from app.schemas.account import AddNewAcountRequest
# from app.services.acount import add_New_Account, fetch_All_Accounts, search

# account_router = APIRouter(
#     prefix="/Accounts",
#     tags=["Accounts"],
#     responses={404: {"description": "Not found"}}

# )

# @account_router.post("/newAccount",status_code=status.HTTP_201_CREATED)
# async def add_Account(data: AddNewAcountRequest, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
#     return await add_New_Account(data,session,user)


# @account_router.get("/allaccounts", response_model=AccountsResponse ,status_code=status.HTTP_200_OK)
# async def get_all_accounts(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
#     return  await fetch_All_Accounts(session, user)
     

# @account_router.get("/search", response_model=AccountsResponse, status_code=status.HTTP_200_OK)
# async def search_accounts(
#     query: Optional[str] = Query(None, description="Search query to filter accounts by email or web_name"),
#     user: User = Depends(get_current_user),
#     session: Session = Depends(get_session)
# ):
    
#     return await search(query,user,session)


from fastapi import APIRouter, Depends, Form, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.responses.account import AccountsResponse, NewAccountResponse

from app.models.user import User
from app.config.database import get_session
from app.config.security import get_current_user
from app.schemas.account import AddNewAcountRequest
from app.services.acount import add_New_Account, decrypted_data, fetch_All_Accounts, search

account_router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
    responses={404: {"description": "Not found"}},
)


@account_router.post("/newAccount", status_code=status.HTTP_201_CREATED)
async def add_Account(
    data: AddNewAcountRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return await add_New_Account(data, session, user)


@account_router.get("/allaccounts", response_model=List[NewAccountResponse], status_code=status.HTTP_200_OK)
async def get_all_accounts(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = Query(
        0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to limit per page"),
):
    return await fetch_All_Accounts(session, user, skip, limit)


@account_router.get("/search", response_model=List[NewAccountResponse], status_code=status.HTTP_200_OK)
async def search_accounts(
    query: str = Query(
        None, description="Search query to filter accounts by email or web_name"),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = Query(
        0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to limit per page"),
):
    return await search(query, user, session, skip, limit)

@account_router.post("/decrypt")
async def get_decrypted_data(user: User = Depends(get_current_user), session: Session = Depends(get_session), skip: int = Query(0, description="Number of records to skip for pagination"), limit: int = Query(10, description="Number of records to limit per page"), password: str = Form(..., description="Signed-in password")):
    return await decrypted_data(user, session, skip, limit, password)
