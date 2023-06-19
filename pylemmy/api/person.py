from typing import Optional

from pylemmy.api.utils import BaseApiModel


class Person(BaseApiModel):
    actor_id: str
    admin: bool
    avatar: Optional[str]
    ban_expires: Optional[str]
    banned: bool
    banner: Optional[str]
    bio: Optional[str]
    bot_account: bool
    deleted: bool
    display_name: Optional[str]
    id: int
    instance_id: int
    local: bool
    matrix_user_id: Optional[str]
    name: str
    published: str
    updated: Optional[str]
