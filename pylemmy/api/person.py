from typing import List, Optional

from pylemmy.api.comment import CommentView
from pylemmy.api.community import CommunityModeratorView
from pylemmy.api.listing import SortType
from pylemmy.api.post import PostView
from pylemmy.api.utils import BaseApiModel


class Person(BaseApiModel):
    actor_id: str
    # admin: bool
    admin: Optional[bool]  # not to specification. change to accept non-conforming API responses
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
    auth: Optional[str]
    community_id: Optional[int]
    limit: Optional[int]
    page: Optional[int]
    person_id: Optional[int]
    saved_only: Optional[bool]
    sort: Optional[SortType]
    username: Optional[str]


class GetPersonDetailsResponse(BaseApiModel):
    comments: List[CommentView]
    moderates: List[CommunityModeratorView]
    person_view: PersonView
    posts: List[PostView]
