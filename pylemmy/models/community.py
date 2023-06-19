from typing import List

import pylemmy
from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.comment import Comment
from pylemmy.models.post import Post
from pylemmy.utils import stream_generator


class Community:
    def __init__(self, lemmy: "pylemmy.Lemmy", community: api.community.CommunityView):
        self.lemmy = lemmy
        self.blocked = community.blocked
        self.safe = community.community
        self.counts = community.counts
        self.subscribed = community.subscribed

    def create_post(self, name: str, **kwargs) -> Post:
        payload = api.post.CreatePost(
            auth=self.lemmy.get_token(), name=name, community_id=self.safe.id, **kwargs
        )
        result = self.lemmy.post_request(LemmyAPI.post, params=payload)
        parsed_result = api.post.PostResponse(**result)

        return Post(self.lemmy, parsed_result.post_view, community=self)

    def get_posts(self, **kwargs) -> List[Post]:
        payload = api.post.GetPosts(
            auth=self.lemmy.get_token(), community_id=self.safe.id, **kwargs
        )
        result = self.lemmy.get_request(LemmyAPI.get_posts, params=payload)
        parsed_result = api.post.GetPostsResponse(**result)

        return [Post(self.lemmy, post, community=self) for post in parsed_result.posts]

    def get_comments(self, **kwargs) -> List[Comment]:
        payload = api.comment.GetComments(
            auth=self.lemmy.get_token(), community_id=self.safe.id, **kwargs
        )
        result = self.lemmy.get_request(LemmyAPI.get_comments, params=payload)
        parsed_result = api.comment.GetCommentsResponse(**result)

        return [Comment(self.lemmy, comment) for comment in parsed_result.comments]

    @property
    def stream(self):
        return CommunityStream(self)


class CommunityStream:
    def __init__(self, community: Community):
        self.community = community

    def get_posts(self, **kwargs):
        return stream_generator(
            self.community.get_posts,
            lambda x: str(x.post_view.post_request.ap_id),
            **kwargs,
        )

    def get_comments(self, **kwargs):
        return stream_generator(
            self.community.get_comments,
            lambda x: str(x.comment_view.comment.ap_id),
            **kwargs,
        )
