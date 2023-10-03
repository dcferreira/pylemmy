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
    parent_id: Optional[int]
    language_id: Optional[int]
    form_id: Optional[str]
    auth: str


class CommentAggregates(BaseApiModel):
    id: int
    comment_id: int
    score: int
    upvotes: int
    downvotes: int
    published: str
    child_count: int
    hot_rank: int


class CommentView(BaseApiModel):
    comment: Comment
    community: Community
    counts: CommentAggregates
    creator: Person
    creator_banned_from_community: bool
    creator_blocked: bool
    my_vote: Optional[int]
    post: Post
    saved: bool
    subscribed: SubscribedType


class CommentResponse(BaseApiModel):
    comment_view: CommentView
    form_id: Optional[str]
    recipient_ids: List[int]


class GetComment(BaseApiModel):
    auth: Optional[str]
    id: int


class GetComments(BaseApiModel):
    auth: Optional[str]
    community_id: Optional[int]
    community_name: Optional[str]
    limit: Optional[int]
    max_depth: Optional[int]
    page: Optional[int]
    parent_id: Optional[int]
    post_id: Optional[int]
    saved_only: Optional[bool]
    sort: Optional[CommentSortType]
    type_: Optional[ListingType]


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
    resolver_id: Optional[int]
    updated: Optional[str]


class CommentReportView(BaseApiModel):
    comment: Comment
    comment_creator: Person
    comment_report: CommentReport
    community: Community
    counts: CommentAggregates
    creator: Person
    creator_banned_from_community: bool
    my_vote: Optional[int]
    post: Post
    resolver: Optional[Person]


class CreateCommentReport(BaseApiModel):
    auth: str
    comment_id: int
    reason: str


class CommentReportResponse(BaseApiModel):
    comment_report_view: CommentReportView


class ResolveCommentReport(BaseApiModel):
    auth: str
    report_id: int
    resolved: bool


class CommentResolveResponse(BaseApiModel):
    comment_report_view: CommentReportView


# TODO: discuss removal of this class.


class ListCommentReports(BaseApiModel):
    auth: str
    community_id: Optional[int]
    limit: Optional[int]
    page: Optional[int]
    unresolved_only: Optional[bool]


class ListCommentReportsResponse(BaseApiModel):
    comment_reports: List[CommentReportView]
