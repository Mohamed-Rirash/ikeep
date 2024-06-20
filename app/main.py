from fastapi import FastAPI
from app.routes import account, user,passwordGenerator
from app.config.database import Base,engine

def create_application():
    application = FastAPI()
    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
    application.include_router(account.account_router)
    application.include_router(passwordGenerator.ppassword_generator_router)
    return application


app = create_application()

Base.metadata.create_all(bind=engine)
@app.get("/")
async def root():
    return {"message": "every thing is working good."}