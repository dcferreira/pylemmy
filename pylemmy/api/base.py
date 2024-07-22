from enum import Enum
from typing import Optional

from pylemmy.api.utils import BaseApiModel


class Community(BaseApiModel):
    actor_id: str
    banner: Optional[str] = None
    deleted: bool
    description: Optional[str] = None
    followers_url: Optional[str] = None
    hidden: bool
    icon: Optional[str] = None
    id: int
    inbox_url: Optional[str] = None
    instance_id: int
    local: bool
    name: str
    nsfw: bool
    posting_restricted_to_mods: bool
    published: str
    removed: bool
    title: str
    updated: Optional[str] = None


class Comment(BaseApiModel):
    id: int
    creator_id: int
    post_id: int
    content: str
    removed: bool
    published: str
    updated: Optional[str] = None
    deleted: bool
    ap_id: str
    local: bool
    path: str
    distinguished: bool
    language_id: int


class Post(BaseApiModel):
    ap_id: str
    body: Optional[str] = None
    community_id: int
    creator_id: int
    deleted: bool
    embed_description: Optional[str] = None
    embed_title: Optional[str] = None
    embed_video_url: Optional[str] = None
    featured_community: Optional[bool] = False
    featured_local: bool
    id: int
    language_id: int
    local: bool
    locked: bool
    name: str
    nsfw: bool
    published: str
    removed: bool
    thumbnail_url: Optional[str] = None
    updated: Optional[str] = None
    url: Optional[str] = None


class Person(BaseApiModel):
    actor_id: str
    # admin: bool
    # not to specification. Change to accept non-conforming API responses
    admin: Optional[bool] = False
    avatar: Optional[str] = None
    ban_expires: Optional[str] = None
    banned: bool
    banner: Optional[str] = None
    bio: Optional[str] = None
    bot_account: bool
    deleted: bool
    display_name: Optional[str] = None
    id: int
    inbox_url: Optional[str] = None
    instance_id: int
    local: bool
    matrix_user_id: Optional[str] = None
    name: str
    published: str
    updated: Optional[str] = None


class SubscribedType(Enum):
    NotSubscribed = "NotSubscribed"
    Pending = "Pending"
    Subscribed = "Subscribed"
