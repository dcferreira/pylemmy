from typing import List, Optional

from pylemmy.api.base import Person, Post
from pylemmy.api.community import (
    Community,
    CommunityModeratorView,
    CommunityView,
    SubscribedType,
)
from pylemmy.api.listing import ListingType, SortType
from pylemmy.api.utils import BaseApiModel


class CreatePost(BaseApiModel):
    body: Optional[str] = None
    community_id: int
    honeypot: Optional[str] = None
    language_id: Optional[int] = None
    name: str
    nsfw: Optional[bool] = False
    url: Optional[str] = None


class PostAggregates(BaseApiModel):
    comments: int
    downvotes: int
    featured_community: Optional[bool] = False
    featured_local: Optional[bool] = False
    hot_rank: Optional[int] = None
    hot_rank_active: Optional[int] = None
    id: Optional[int] = None
    newest_comment_time: str
    newest_comment_time_necro: Optional[str] = None
    post_id: int
    published: str
    score: int
    upvotes: int


class PostView(BaseApiModel):
    community: Community
    counts: PostAggregates
    creator: Person
    creator_banned_from_community: bool
    creator_blocked: bool
    my_vote: Optional[int] = None
    post: Post
    read: bool
    saved: bool
    subscribed: SubscribedType
    unread_comments: int


class PostResponse(BaseApiModel):
    post_view: PostView


class GetPost(BaseApiModel):
    comment_id: Optional[int] = None
    id: Optional[int] = None


class GetPostResponse(BaseApiModel):
    community_view: CommunityView
    cross_posts: List[PostView]
    moderators: List[CommunityModeratorView]
    post_view: PostView


class GetPosts(BaseApiModel):
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    saved_only: Optional[bool] = None
    liked_only: Optional[bool] = None
    disliked_only: Optional[bool] = None
    show_hidden: Optional[bool] = None
    sort: Optional[SortType] = None
    type_: Optional[ListingType] = None


class GetPostsResponse(BaseApiModel):
    posts: List[PostView]


class PostReport(BaseApiModel):
    creator_id: int
    id: int
    original_post_body: Optional[str] = None
    original_post_name: str
    original_post_url: Optional[str] = None
    post_id: int
    published: str
    reason: str
    resolved: bool
    resolver_id: Optional[int] = None
    updated: Optional[str] = None


class PostReportView(BaseApiModel):
    community: Community
    counts: PostAggregates
    creator: Person
    creator_banned_from_community: bool
    my_vote: Optional[int] = None
    post: Post
    post_creator: Person
    post_report: PostReport
    resolver: Optional[Person] = None


class CreatePostReport(BaseApiModel):
    post_id: int
    reason: str


class PostReportResponse(BaseApiModel):
    post_report_view: PostReportView


class ResolvePostReport(BaseApiModel):
    report_id: int
    resolved: bool


class PostResolveResponse(BaseApiModel):
    post_report_view: PostReportView


# TODO: Discuss removal as not in the API


class ListPostReports(BaseApiModel):
    community_id: Optional[int] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    unresolved_only: Optional[bool] = False


class ListPostReportsResponse(BaseApiModel):
    post_reports: List[PostReportView]
