from typing import Optional

from pydantic import BaseModel


class Login(BaseModel):
    username_or_email: str
    password: str


class LoginResponse(BaseModel):
    jwt: Optional[str]
    registration_created: bool
    verify_email_sent: bool
