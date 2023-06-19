from typing import Optional

from pylemmy.api.utils import BaseApiModel


class Login(BaseApiModel):
    username_or_email: str
    password: str


class LoginResponse(BaseApiModel):
    jwt: Optional[str]
    registration_created: bool
    verify_email_sent: bool
