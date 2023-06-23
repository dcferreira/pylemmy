from typing import List, Optional

from pylemmy.api.community import (
    Community,
    CommunityModeratorView,
    CommunityView,
    SubscribedType,
)
from pylemmy.api.listing import ListingType, SortType
from pylemmy.api.person import Person
from pylemmy.api.utils import BaseApiModel


class CreatePost(BaseApiModel):
    auth: str
    body: Optional[str]
    community_id: int
    honeypot: Optional[str]
    language_id: Optional[int]
    name: str
    nsfw: Optional[bool]
    url: Optional[str]


class Post(BaseApiModel):
    ap_id: str
    body: Optional[str]
    community_id: int
    creator_id: int
    deleted: bool
    embed_description: Optional[str]
    embed_title: Optional[str]
    embed_video_url: Optional[str]
    featured_community: bool
    featured_local: bool
    id: int
    language_id: int
    local: bool
    locked: bool
    name: str
    nsfw: bool
    published: str
    removed: bool
    thumbnail_url: Optional[str]
    updated: Optional[str]
    url: Optional[str]


class PostAggregates(BaseApiModel):
    comments: int
    downvotes: int
    featured_community: bool
    featured_local: bool
    id: int
    newest_comment_time: str
    newest_comment_time_necro: str
    post_id: int
    score: int
    upvotes: int


class PostView(BaseApiModel):
    community: Community
    counts: PostAggregates
    creator: Person
    creator_banned_from_community: bool
    creator_blocked: bool
    my_vote: Optional[int]
    post: Post
    read: bool
    saved: bool
    subscribed: SubscribedType
    unread_comments: int


class PostResponse(BaseApiModel):
    post_view: PostView


class GetPost(BaseApiModel):
    auth: Optional[str] = None
    comment_id: Optional[int] = None
    id: Optional[int] = None


class GetPostResponse(BaseApiModel):
    community_view: CommunityView
    moderators: List[CommunityModeratorView]
    online: int
    post_view: PostView


class GetPosts(BaseApiModel):
    auth: Optional[str]
    community_id: Optional[int]
    community_name: Optional[str]
    limit: Optional[int]
    page: Optional[int]
    saved_only: Optional[bool]
    sort: Optional[SortType]
    type_: Optional[ListingType]


class GetPostsResponse(BaseApiModel):
    posts: List[PostView]


class PostReport(BaseApiModel):
    id: int
    creator_id: int
    post_id: int
    original_post_name: str
    original_post_url: Optional[str]
    original_post_body: Optional[str]
    reason: str
    resolved: bool
    resolved_id: Optional[int]
    published: str
    updated: Optional[str]


class PostReportView(BaseApiModel):
    post_report: PostReport
    post: Post
    community: int
    creator: Person
    post_creator: Person
    creator_banned_from_community: bool
    my_vote: Optional[int]
    counts: PostAggregates
    resolve: Optional[Person]


class CreatePostReport(BaseApiModel):
    auth: str
    post_id: int
    reason: str


class PostReportResponse(BaseApiModel):
    post_report_view: PostReportView


class ResolvePostReport(BaseApiModel):
    auth: str
    report_id: int
    resolved: bool


class PostResolveResponse(BaseApiModel):
    post_report_view: PostReportView


class ListPostReports(BaseApiModel):
    auth: str
    page: int
    limit: int
    unresolved_only: Optional[bool]
    community_id: Optional[int]


class ListPostReportsResponse(BaseApiModel):
    post_reports: List[PostReportView]
