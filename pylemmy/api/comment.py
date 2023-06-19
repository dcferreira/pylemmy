from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from pylemmy.api.community import Community, SubscribedType
from pylemmy.api.listing import ListingType
from pylemmy.api.person import Person
from pylemmy.api.post import Post


class CommentSortType(str, Enum):
    Hot = "Hot"
    Top = "Top"
    New = "New"
    Old = "Old"


class CreateComment(BaseModel):
    content: str
    post_id: int
    parent_id: Optional[int]
    language_id: Optional[int]
    form_id: Optional[str]
    auth: str


class Comment(BaseModel):
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


class CommentAggregates(BaseModel):
    id: int
    comment_id: int
    score: int
    upvotes: int
    downvotes: int
    published: str
    child_count: int
    hot_rank: int


class CommentView(BaseModel):
    comment: Comment
    creator: Person
    post: Post
    community: Community
    counts: CommentAggregates
    creator_banned_from_community: bool
    subscribed: SubscribedType
    saved: bool
    creator_blocked: bool
    my_vote: Optional[int]


class CommentResponse(BaseModel):
    comment_view: CommentView
    recipient_ids: List[int]
    form_id: Optional[str]


class GetComments(BaseModel):
    auth: Optional[str]
    community_id: Optional[int]
    community_name: Optional[str]
    limit: Optional[int]
    max_depth: Optional[int]
    page: Optional[int]
    parent_id: Optional[int]
    post_id: Optional[int]
    saved_only: Optional[int]
    sort: Optional[CommentSortType]
    type_: Optional[ListingType]


class GetCommentsResponse(BaseModel):
    comments: List[CommentView]
