# from typing import Dict
# from fastapi import HTTPException, status
# from sqlalchemy import and_, or_
# from app.models.accounts import Account
# from app.responses.account import NewAccountResponse


# async def add_New_Account(data, session, user):
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
#         )

#     authenticated_user_id = user.id
   

#     url_str = str(data.url)

#     account_exist = session.query(Account)\
#         .filter(
#             and_(
#                 Account.user_id == authenticated_user_id,
#                 Account.web_name == data.web_name,
#                 Account.url == url_str,
#                 Account.email == data.email,
#             )
#     )\
#         .first()

#     if account_exist:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
#         )

#     account = Account()
#     account.web_name = data.web_name
#     account.url = url_str
#     account.email = data.email
#     account.password = data.password  # Fixed typo from `data.passwword`
#     account.user_id = authenticated_user_id
#     session.add(account)
#     session.commit()
#     session.refresh(account)

#     return {"message": "Account added successfully"}


# async def fetch_All_Accounts(session, user) -> list[NewAccountResponse]:
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
#         )

#     authenticated_user_id = user.id

#     # Fetch accounts where user_id matches the authenticated user's ID
#     accounts = session.query(Account).filter(
#         Account.user_id == authenticated_user_id).all()
#     if not accounts:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="not Accounts found")

#     # Convert SQLAlchemy objects to NewAccountResponse objects
#     accounts_list = []
#     for account in accounts:
#         account_response = NewAccountResponse(
#             id=account.id,
#             web_name=account.web_name,
#             url=account.url,
#             email=account.email,
#             password=account.password  # Include password field if needed
#         )
#         accounts_list.append(account_response)

#     return accounts_list


# async def search(query, user, session):
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
#         )

#     authenticated_user_id = user.id

#     # Base filter for the authenticated user's accounts
#     base_filter = Account.user_id == authenticated_user_id

#     # Filters for search query
#     filters = [base_filter]

#     if query:
#         # Use OR condition to match partials and case insensitive
#         filters.append(
#             or_(
#                 Account.email.ilike(f"%{query}%"),
#                 Account.web_name.ilike(f"%{query}%"),
#                 Account.url.ilike(f"%{query}%"),
#             )
#         )

#     # Fetch accounts based on constructed filters
#     accounts = session.query(Account).filter(*filters).all()
#     if not accounts:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="no data found")
#     # Convert SQLAlchemy objects to NewAccountResponse objects
#     accounts_list = []
#     for account in accounts:
#         account_response = NewAccountResponse(
#             id=account.id,
#             web_name=account.web_name,
#             url=account.url,
#             email=account.email,
#             password=account.password  # Include password field if needed
#         )
#         accounts_list.append(account_response)

#     return accounts_list


from typing import List
from fastapi import HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.accounts import Account
from app.responses.account import NewAccountResponse
from app.models.user import User


async def add_New_Account(data, session, user):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )

    authenticated_user_id = user.id

    url_str = str(data.url)

    account_exist = session.query(Account).filter(
        and_(
            Account.user_id == authenticated_user_id,
            Account.web_name == data.web_name,
            Account.url == url_str,
            Account.email == data.email,
        )
    ).first()

    if account_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )

    account = Account()
    account.web_name = data.web_name
    account.url = url_str
    account.email = data.email
    account.password = data.password  # Fixed typo from `data.passwword`
    account.user_id = authenticated_user_id
    session.add(account)
    session.commit()
    session.refresh(account)

    return {"message": "Account added successfully"}


async def fetch_All_Accounts(session: Session, user: User, skip: int = 0, limit: int = 10) -> List[NewAccountResponse]:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )

    authenticated_user_id = user.id

    # Fetch accounts where user_id matches the authenticated user's ID, with pagination
    accounts = session.query(Account).filter(
        Account.user_id == authenticated_user_id
    ).offset(skip).limit(limit).all()

    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No accounts found"
        )

    # Convert SQLAlchemy objects to NewAccountResponse objects
    accounts_list = []
    for account in accounts:
        account_response = NewAccountResponse(
            id=account.id,
            web_name=account.web_name,
            url=account.url,
            email=account.email,
            password=account.password  # Include password field if needed
        )
        accounts_list.append(account_response)

    return accounts_list


async def search(query: str, user: User, session: Session, skip: int = 0, limit: int = 10) -> List[NewAccountResponse]:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )

    authenticated_user_id = user.id

    # Base filter for the authenticated user's accounts
    base_filter = Account.user_id == authenticated_user_id

    # Filters for search query
    filters = [base_filter]

    if query:
        # Use OR condition to match partials and case insensitive
        filters.append(
            or_(
                Account.email.ilike(f"%{query}%"),
                Account.web_name.ilike(f"%{query}%"),
                Account.url.ilike(f"%{query}%"),
            )
        )

    # Fetch accounts based on constructed filters and pagination
    accounts = session.query(Account).filter(
        *filters).offset(skip).limit(limit).all()

    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No accounts found"
        )

    # Convert SQLAlchemy objects to NewAccountResponse objects
    accounts_list = []
    for account in accounts:
        account_response = NewAccountResponse(
            id=account.id,
            web_name=account.web_name,
            url=account.url,
            email=account.email,
            password=account.password  # Include password field if needed
        )
        accounts_list.append(account_response)

    return accounts_list
