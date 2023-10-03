from typing import List, Optional

from pylemmy.api.base import Community, Person, SubscribedType
from pylemmy.api.listing import ListingType, SortType
from pylemmy.api.site import Site
from pylemmy.api.utils import BaseApiModel


class GetCommunity(BaseApiModel):
    auth: Optional[str] = None
    id: Optional[int] = None
    name: Optional[str] = None


class CommunityAggregates(BaseApiModel):
    comments: int
    community_id: int
    hot_rank: int
    id: int
    posts: int
    published: str
    subscribers: int
    users_active_day: int
    users_active_half_year: int
    users_active_month: int
    users_active_week: int


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
    show_nsfw: Optional[bool]
    sort: Optional[SortType]
    type_: Optional[ListingType]


class ListCommunitiesResponse(BaseApiModel):
    communities: List[CommunityView]
