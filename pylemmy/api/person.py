from typing import List, Optional

from pylemmy.api.comment import CommentView
from pylemmy.api.community2 import CommunityModeratorView
from pylemmy.api.listing import SortType
from pylemmy.api.post import PostView
from pylemmy.api.utils import BaseApiModel


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


class PersonAggregates(BaseApiModel):
    comment_count: int
    comment_score: int
    id: int
    person_id: int
    post_count: int
    post_score: int


class PersonView(BaseApiModel):
    counts: PersonAggregates
    person: Person


class GetPersonDetails(BaseApiModel):
    auth: Optional[str] = None
    community_id: Optional[int] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    person_id: Optional[int] = None
    saved_only: Optional[bool] = None
    sort: Optional[SortType] = None
    username: Optional[str] = None


class GetPersonDetailsResponse(BaseApiModel):
    comments: List[CommentView]
    moderates: List[CommunityModeratorView]
    person_view: PersonView
    posts: List[PostView]
