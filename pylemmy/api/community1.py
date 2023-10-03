from enum import Enum
from typing import Optional

from pylemmy.api.utils import BaseApiModel


class Community(BaseApiModel):
    actor_id: str
    banner: Optional[str]
    deleted: bool
    description: Optional[str]
    followers_url: str
    hidden: bool
    icon: Optional[str]
    id: int
    inbox_url: str
    instance_id: int
    local: bool
    name: str
    nsfw: bool
    posting_restricted_to_mods: bool
    published: str
    removed: bool
    title: str
    updated: Optional[str]


class SubscribedType(Enum):
    NotSubscribed = "NotSubscribed"
    Pending = "Pending"
    Subscribed = "Subscribed"
