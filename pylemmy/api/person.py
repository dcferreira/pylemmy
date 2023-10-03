from typing import List, Optional

from pylemmy.api.base import Person
from pylemmy.api.comment import CommentView
from pylemmy.api.community import CommunityModeratorView
from pylemmy.api.listing import SortType
from pylemmy.api.post import PostView
from pylemmy.api.utils import BaseApiModel


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
