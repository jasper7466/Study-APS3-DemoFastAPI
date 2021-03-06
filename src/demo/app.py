import shutil
from typing import (
    List,
    Optional,
)
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Response,
    Form,
    HTTPException,
    status,
)
from fastapi.staticfiles import StaticFiles
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound
)

from .database import (
    Account,
    Session,
)
from .config import (
    settings,
    PROJECT_ROOT,
)
from .models import AccountModel

app = FastAPI()
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')


@app.get('/')
def root():
    return 'Hello, World!'


@app.post('/create-account')
def create_account(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
):
    with Session() as session:
        account = Account(
            email=email,
            username=username,
            password=pbkdf2_sha256.hash(password),
        )
        session.add(account)
        try:
            session.commit()
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT) from None
    return Response()


@app.get('/get-accounts', response_model=List[AccountModel])
def get_accounts():
    with Session() as session:
        accounts = session.execute(
            select(Account)
        ).scalars().all()
    return accounts


@app.get('/get-account/{account_id}', response_model=AccountModel)
def get_account(account_id: int):
    with Session() as session:
        try:
            account = session.execute(
                select(Account)
                .where(Account.id == account_id)
            ).scalar_one()
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from None
    return account


@app.patch('/edit-account/{account_id}')
def edit_account(
    account_id: int,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
):
    with Session() as session:
        try:
            account = session.execute(
                select(Account)
                .where(Account.id == account_id)
            ).scalar_one()
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from None

        if not first_name and not last_name and not avatar:
            return Response()

        account.first_name = first_name or account.first_name
        account.last_name = last_name or account.last_name

        if avatar:
            filepath = PROJECT_ROOT / settings.static_directory / avatar.filename
            with filepath.open(mode='wb') as f:
                shutil.copyfileobj(avatar.file, f)
            file_url = f'{settings.static_url}/{avatar.filename}'
            account.avatar = file_url

        session.commit()
        return Response()
