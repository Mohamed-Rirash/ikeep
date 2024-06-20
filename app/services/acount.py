from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.config.security import verify_password
from app.models.accounts import Account
from app.responses.account import NewAccountResponse
from app.models.user import User
from app.services.encription import decrypt_data, encrypt_data


async def add_New_Account(data, session: Session, user):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )

    authenticated_user_id = user.id
    url_str = str(data.url)

    # Fetch all accounts for the user to compare emails after decryption
    accounts = session.query(Account).filter(
        and_(
            Account.user_id == authenticated_user_id,
            Account.web_name == data.web_name,
            Account.url == url_str,
        )
    ).all()

    # Compare decrypted email to check for existing account
    for account in accounts:
        decrypted_email = decrypt_data(account.email, user.private_key)
        if decrypted_email == data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
            )

    # Encrypt data before storing
    encrypted_email = encrypt_data(data.email, user.public_key)
    encrypted_password = encrypt_data(data.password, user.public_key)

    # Create new account
    new_account = Account(
        web_name=data.web_name,
        url=url_str,
        email=encrypted_email,
        password=encrypted_password,
        user_id=authenticated_user_id
    )

    session.add(new_account)
    session.commit()
    session.refresh(new_account)

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


async def decrypted_data(user, session, skip, limit, password):
    
    # replace with your password verification function
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    accounts = session.query(Account).filter(
        Account.user_id == user.id).offset(skip).limit(limit).all()

    decrypted_accounts = []
    for account in accounts:
        try:
            decrypted_email = decrypt_data(account.email, user.private_key)
            decrypted_password = decrypt_data(
                account.password, user.private_key)
            decrypted_accounts.append({
                "web_name": account.web_name,
                "url": account.url,
                "email": decrypted_email,
                "password": decrypted_password
            })
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Decryption error: {str(e)}")

    return decrypted_accounts
