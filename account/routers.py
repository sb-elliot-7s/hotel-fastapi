from fastapi import APIRouter, Depends, status, Form
from .deps import get_account_service
from .schemas import CreateAccountSchema, AccountSchema, TokenSchema
from .auth_logic import AuthLogic

account_router = APIRouter(prefix='/account', tags=['account'])

router_data = {
    'registration': {
        'path': '/registration',
        'status_code': status.HTTP_201_CREATED,
        'response_model': AccountSchema,
        'response_model_by_alias': False
    },
    'login': {
        'path': '/login',
        'status_code': status.HTTP_200_OK,
        'response_model': TokenSchema
    }
}


@account_router.post(**router_data.get('registration'))
async def registration(account_data: CreateAccountSchema,
                       service_data=Depends(get_account_service)):
    return await AuthLogic(**service_data).save_user(account_data=account_data)


@account_router.post(**router_data.get('login'))
async def login(email: str = Form(...), password: str = Form(...), service_data=Depends(get_account_service)):
    return await AuthLogic(**service_data).login(email=email, password=password)
