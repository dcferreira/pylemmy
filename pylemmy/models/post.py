from typing import List, Optional

import pylemmy
from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.comment import Comment


class Post:
    def __init__(
        self,
        lemmy: "pylemmy.Lemmy",
        post: api.post.PostView,
        community: Optional["pylemmy.models.community.Community"] = None,
    ):
        self.lemmy = lemmy
        self.post_view = post

        self._community = community

    @property
    def community(self) -> "pylemmy.models.community.Community":
        if self._community is None:
            self._community = self.lemmy.get_community(self.post_view.community.id)
        return self._community

    def create_comment(self, content: str, **kwargs) -> Comment:
        payload = api.comment.CreateComment(
            auth=self.lemmy.get_token(),
            content=content,
            post_id=self.post_view.post.id,
            **kwargs,
        )
        result = self.lemmy.post_request(LemmyAPI.comment, params=payload)
        parsed_result = api.comment.CommentResponse(**result)

        return Comment(
            self.lemmy, parsed_result.comment_view, post=self, community=self._community
        )

    def get_comments(self, **kwargs) -> List[Comment]:
        payload = api.comment.GetComments(
            auth=self.lemmy.get_token(), post_id=self.post_view.post.id, **kwargs
        )
        result = self.lemmy.get_request(LemmyAPI.get_comments, params=payload)
        parsed_result = api.comment.GetCommentsResponse(**result)

        return [
            Comment(self.lemmy, comment, post=self, community=self._community)
            for comment in parsed_result.comments
        ]
