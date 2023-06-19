from typing import List, Optional

from pydantic import BaseModel

from pylemmy.api.community import (
    Community,
    CommunityModeratorView,
    CommunityView,
    SubscribedType,
)
from pylemmy.api.listing import ListingType, SortType
from pylemmy.api.person import Person


class CreatePost(BaseModel):
    auth: str
    body: Optional[str]
    community_id: int
    honeypot: Optional[str]
    language_id: Optional[int]
    name: str
    nsfw: Optional[bool]
    url: Optional[str]


class Post(BaseModel):
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


class PostAggregates(BaseModel):
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


class PostView(BaseModel):
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


class PostResponse(BaseModel):
    post_view: PostView


class GetPost(BaseModel):
    auth: Optional[str] = None
    comment_id: Optional[int] = None
    id: Optional[int] = None


class GetPostResponse(BaseModel):
    community_view: CommunityView
    moderators: List[CommunityModeratorView]
    online: int
    post_view: PostView


class GetPosts(BaseModel):
    auth: Optional[str]
    community_id: Optional[int]
    community_name: Optional[str]
    limit: Optional[int]
    page: Optional[int]
    saved_only: Optional[bool]
    sort: Optional[SortType]
    type_: Optional[ListingType]


class GetPostsResponse(BaseModel):
    posts: List[PostView]
