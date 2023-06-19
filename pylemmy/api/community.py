from enum import Enum
from typing import List, Optional

from pylemmy.api.listing import ListingType, SortType
from pylemmy.api.person import Person
from pylemmy.api.site import Site
from pylemmy.api.utils import BaseApiModel


class GetCommunity(BaseApiModel):
    auth: Optional[str] = None
    id: Optional[int] = None
    name: Optional[str] = None


class Community(BaseApiModel):
    actor_id: str
    banner: Optional[str]
    deleted: bool
    description: Optional[str]
    hidden: bool
    icon: Optional[str]
    id: int
    instance_id: int
    local: bool
    name: str
    nsfw: bool
    posting_restricted_to_mods: bool
    published: str
    removed: bool
    title: str
    updated: Optional[str]


class CommunityAggregates(BaseApiModel):
    comments: int
    community_id: int
    id: int
    posts: int
    subscribers: int
    users_active_day: int
    users_active_half_year: int
    users_active_month: int
    users_active_week: int


class SubscribedType(Enum):
    NotSubscribed = "NotSubscribed"
    Pending = "Pending"
    Subscribed = "Subscribed"


class CommunityView(BaseApiModel):
    blocked: bool
    community: Community
    counts: CommunityAggregates
    subscribed: SubscribedType


class CommunityModeratorView(BaseApiModel):
    community: Community
    moderator: Person


class GetCommunityResponse(BaseApiModel):
    community_view: CommunityView
    discussion_languages: List[int]
    moderators: List[CommunityModeratorView]
    site: Optional[Site]


class CreateCommunity(BaseApiModel):
    auth: str
    banner: Optional[str]
    description: Optional[str]
    discussion_languages: Optional[List[int]]
    icon: Optional[str]
    name: str
    nsfw: Optional[bool]
    posting_restricted_to_mods: Optional[bool]
    title: str


class CommunityResponse(BaseApiModel):
    community_view: CommunityView
    discussion_languages: List[int]


class ListCommunities(BaseApiModel):
    auth: Optional[str]
    limit: Optional[int]
    page: Optional[int]
    sort: Optional[SortType]
    type_: Optional[ListingType]


class ListCommunitiesResponse(BaseApiModel):
    communities: List[CommunityView]
