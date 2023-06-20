"""Implements the Community class."""
from typing import List

import pylemmy
from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.comment import Comment
from pylemmy.models.post import Post
from pylemmy.utils import stream_generator


class Community:
    """A class for Communities.

    To obtain an instance of this class for c/test run:

        community = lemmy.get_community("test")
    """

    def __init__(self, lemmy: "pylemmy.Lemmy", community: api.community.CommunityView):
        """Initialize a Community instance.

        :param lemmy: A Lemmy instance.
        :param community: A [CommunityView](
        https://join-lemmy.org/api/interfaces/CommunityView.html).
        """
        self.lemmy = lemmy
        self.blocked = community.blocked
        self.safe = community.community
        self.counts = community.counts
        self.subscribed = community.subscribed

    def create_post(self, name: str, **kwargs) -> Post:
        """Create a new post in this Community.

        :param name: Name of the post.
        :param kwargs: See optional arguments in [CreatePost](
        https://join-lemmy.org/api/interfaces/CreatePost.html).
        :return: The created Post.
        """
        payload = api.post.CreatePost(
            auth=self.lemmy.get_token(), name=name, community_id=self.safe.id, **kwargs
        )
        result = self.lemmy.post_request(LemmyAPI.Post, params=payload)
        parsed_result = api.post.PostResponse(**result)

        return Post(self.lemmy, parsed_result.post_view, community=self)

    def get_posts(self, **kwargs) -> List[Post]:
        """Gets a list of Posts from this community.

        :param kwargs: See optional arguments in [GetPosts](
        https://join-lemmy.org/api/interfaces/GetPosts.html).
        """
        payload = api.post.GetPosts(
            auth=self.lemmy.get_token_optional(), community_id=self.safe.id, **kwargs
        )
        result = self.lemmy.get_request(LemmyAPI.GetPosts, params=payload)
        parsed_result = api.post.GetPostsResponse(**result)

        return [Post(self.lemmy, post, community=self) for post in parsed_result.posts]

    def get_comments(self, **kwargs) -> List[Comment]:
        """Gets a list of Comments from this community.

        :param kwargs: See optional arguments in [GetComments](
        https://join-lemmy.org/api/interfaces/GetComments.html).
        """
        payload = api.comment.GetComments(
            auth=self.lemmy.get_token_optional(), community_id=self.safe.id, **kwargs
        )
        result = self.lemmy.get_request(LemmyAPI.GetComments, params=payload)
        parsed_result = api.comment.GetCommentsResponse(**result)

        return [Comment(self.lemmy, comment) for comment in parsed_result.comments]

    @property
    def stream(self) -> "CommunityStream":
        """Returns a stream of content.

        This stream is to be used to monitor posts or comments.

        Example:

            community = lemmy.get_community("test")
            for post in community.stream.get_posts():
                process_post(post)
        """
        return CommunityStream(self)


class CommunityStream:
    """Helper class to stream content from a specific community.

    This class shouldn't be directly initialized, but rather accessed through
    Community.

    Example:

        community = lemmy.get_community("test")
        for post in community.stream.get_posts():
            process_post(post)
    """

    def __init__(self, community: Community):
        """Initialize a CommunityStream.

        :param community: A Community to run the stream on.
        """
        self.community = community

    def get_posts(self, **kwargs):
        """Get a stream of Posts in the Community.

        :param kwargs: See the arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        return stream_generator(
            self.community.get_posts,
            lambda x: str(x.post_view.post.ap_id),
            **kwargs,
        )

    def get_comments(self, **kwargs):
        """Get a stream of Comments in the Community.

        :param kwargs: See the arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        return stream_generator(
            self.community.get_comments,
            lambda x: str(x.comment_view.comment.ap_id),
            **kwargs,
        )
