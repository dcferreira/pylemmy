from enum import Enum
from typing import List, Optional

from pylemmy.api.base import Comment, Person, Post
from pylemmy.api.community import Community, SubscribedType
from pylemmy.api.listing import ListingType
from pylemmy.api.utils import BaseApiModel


class CommentSortType(str, Enum):
    Hot = "Hot"
    Top = "Top"
    New = "New"
    Old = "Old"


class CreateComment(BaseApiModel):
    content: str
    post_id: int
    parent_id: Optional[int] = None
    language_id: Optional[int] = None
    form_id: Optional[str] = None


class CommentAggregates(BaseApiModel):
    id: Optional[int] = None
    comment_id: int
    score: int
    upvotes: int
    downvotes: int
    published: str
    child_count: int
    hot_rank: Optional[int] = None


class CommentView(BaseApiModel):
    comment: Comment
    community: Community
    counts: CommentAggregates
    creator: Person
    creator_banned_from_community: bool
    creator_blocked: bool
    my_vote: Optional[int] = None
    post: Post
    saved: bool
    subscribed: SubscribedType


class CommentResponse(BaseApiModel):
    comment_view: CommentView
    form_id: Optional[str] = None
    recipient_ids: List[int]


class GetComment(BaseApiModel):
    id: int


class GetComments(BaseApiModel):
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    limit: Optional[int] = None
    max_depth: Optional[int] = None
    page: Optional[int] = None
    parent_id: Optional[int] = None
    post_id: Optional[int] = None
    saved_only: Optional[bool] = None
    liked_only: Optional[bool] = None
    disliked_only: Optional[bool] = None
    sort: Optional[CommentSortType] = None
    type_: Optional[ListingType] = None


class GetCommentsResponse(BaseApiModel):
    comments: List[CommentView]


class CommentReport(BaseApiModel):
    comment_id: int
    creator_id: int
    id: int
    original_comment_text: str
    published: str
    reason: str
    resolved: bool
    resolver_id: Optional[int] = None
    updated: Optional[str] = None


class CommentReportView(BaseApiModel):
    comment: Comment
    comment_creator: Person
    comment_report: CommentReport
    community: Community
    counts: CommentAggregates
    creator: Person
    creator_banned_from_community: bool
    my_vote: Optional[int] = None
    post: Post
    resolver: Optional[Person] = None


class CreateCommentReport(BaseApiModel):
    comment_id: int
    reason: str


class CommentReportResponse(BaseApiModel):
    comment_report_view: CommentReportView


class ResolveCommentReport(BaseApiModel):
    report_id: int
    resolved: bool


class CommentResolveResponse(BaseApiModel):
    comment_report_view: CommentReportView


# TODO: discuss removal of this class.


class ListCommentReports(BaseApiModel):
    community_id: Optional[int] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    unresolved_only: Optional[bool] = False


class ListCommentReportsResponse(BaseApiModel):
    comment_reports: List[CommentReportView]
