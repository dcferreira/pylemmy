from typing import List, Optional

from pylemmy.api.base import Community, Person, SubscribedType
from pylemmy.api.listing import ListingType, SortType
from pylemmy.api.site import Site
from pylemmy.api.utils import BaseApiModel


class GetCommunity(BaseApiModel):
    id: Optional[int] = None
    name: Optional[str] = None


class CommunityAggregates(BaseApiModel):
    comments: int
    community_id: int
    hot_rank: Optional[int] = None
    id: Optional[int] = None
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
    site: Optional[Site] = None


class CreateCommunity(BaseApiModel):
    banner: Optional[str] = None
    description: Optional[str] = None
    discussion_languages: Optional[List[int]] = None
    icon: Optional[str] = None
    name: str
    nsfw: Optional[bool] = False
    posting_restricted_to_mods: Optional[bool] = False
    title: str


class CommunityResponse(BaseApiModel):
    community_view: CommunityView
    discussion_languages: List[int]


class ListCommunities(BaseApiModel):
    limit: Optional[int] = None
    page: Optional[int] = None
    show_nsfw: Optional[bool] = None
    sort: Optional[SortType] = None
    type_: Optional[ListingType] = None


class ListCommunitiesResponse(BaseApiModel):
    communities: List[CommunityView]
