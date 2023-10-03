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


class Comment(BaseApiModel):
    id: int
    creator_id: int
    post_id: int
    content: str
    removed: bool
    published: str
    updated: Optional[str]
    deleted: bool
    ap_id: str
    local: bool
    path: str
    distinguished: bool
    language_id: int


class Post(BaseApiModel):
    ap_id: str
    body: Optional[str]
    community_id: int
    creator_id: int
    deleted: bool
    embed_description: Optional[str]
    embed_title: Optional[str]
    embed_video_url: Optional[str]
    featured_community: bool
    featured_local: bool
    id: int
    language_id: int
    local: bool
    locked: bool
    name: str
    nsfw: bool
    published: str
    removed: bool
    thumbnail_url: Optional[str]
    updated: Optional[str]
    url: Optional[str]


class Person(BaseApiModel):
    actor_id: str
    # admin: bool
    # not to specification. Change to accept non-conforming API responses
    admin: Optional[bool]
    avatar: Optional[str]
    ban_expires: Optional[str]
    banned: bool
    banner: Optional[str]
    bio: Optional[str]
    bot_account: bool
    deleted: bool
    display_name: Optional[str]
    id: int
    inbox_url: str
    instance_id: int
    local: bool
    matrix_user_id: Optional[str]
    name: str
    published: str
    updated: Optional[str]


class SubscribedType(Enum):
    NotSubscribed = "NotSubscribed"
    Pending = "Pending"
    Subscribed = "Subscribed"
