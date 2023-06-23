"""Implements the Community class."""
from typing import Any, Callable, Iterable, List, Union

from mypy_extensions import KwArg

import pylemmy
from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.comment import Comment
from pylemmy.models.post import Post
from pylemmy.utils import stream_apply, stream_generator


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

    def list_post_reports(self, **kwargs) -> List[api.post.PostReportView]:
        """List post reports in this community.

        :param kwargs: See optional arguments in [ListPostReports](
        https://join-lemmy.org/api/interfaces/ListPostReports.html).
        """
        return self.lemmy.list_post_reports(community_id=self.safe.id, **kwargs)

    def list_comment_reports(self, **kwargs) -> List[api.comment.CommentReportView]:
        """List comment reports in this community.

        :param kwargs: See optional arguments in [ListCommentReports](
        https://join-lemmy.org/api/interfaces/ListCommentReports.html).
        """
        return self.lemmy.list_comment_reports(community_id=self.safe.id, **kwargs)

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
    [Community][pylemmy.community.Community].

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

        :param kwargs: See the optional arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        return stream_generator(
            self.community.get_posts,
            lambda x: str(x.post_view.post.ap_id),
            **kwargs,
        )

    def get_comments(self, **kwargs):
        """Get a stream of Comments in the Community.

        :param kwargs: See the optional arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        return stream_generator(
            self.community.get_comments,
            lambda x: str(x.comment_view.comment.ap_id),
            **kwargs,
        )


class MultiCommunityStream:
    """Helper class to stream content from multiple communities.

    This class shouldn't be directly initialized, but rather accessed through
    [Lemmy][pylemmy.lemmy.Lemmy].

    Example:
    A simple example where we want to print the content of each post.

        def process_content(elem: Union[Post, Comment]):
                print(elem.post_view.post.name)

        multi_stream = lemmy.multi_communities_stream(["community1", "community2"])
        multi_stream.content_apply(process_content)
    """

    def __init__(self, communities: List[Community]):
        """Initializer for MultiCommunityStream.

        :param communities: A list of communities to monitor.
        """
        self.communities = communities

    def posts_apply(self, callback: Callable[[Post], Any], **kwargs):
        """Apply a callback function to a stream of Posts in the Communities.

        Example:
        A simple example where we want to print the content of each post.

            def process_content(elem: Union[Post, Comment]):
                print(elem.post_view.post.name)

            multi_stream = lemmy.multi_communities_stream(["community1", "community2"])
            multi_stream.content_apply(process_content)

        :param callback: Function that will be called for each Post.
        :param kwargs: See the optional arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        results_fns = [c.get_posts for c in self.communities]
        unique_keys_fns = [lambda x: str(x.post_view.post.ap_id)] * len(
            self.communities
        )
        stream_apply(results_fns, unique_keys_fns, callback, **kwargs)

    def comments_apply(self, callback: Callable[[Comment], Any], **kwargs):
        """Apply a callback function to a stream of Comments in the Communities.

        Example:
        A simple example where we want to print the content of each comment.

            def process_content(elem: Union[Post, Comment]):
                print(elem.comment_view.comment.content)

            multi_stream = lemmy.multi_communities_stream(["community1", "community2"])
            multi_stream.content_apply(process_content)

        :param callback: Function that will be called for each Comment.
        :param kwargs: See the optional arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        results_fns = [c.get_comments for c in self.communities]
        unique_keys_fns = [lambda x: str(x.comment_view.comment.ap_id)] * len(
            self.communities
        )
        stream_apply(results_fns, unique_keys_fns, callback, **kwargs)

    def content_apply(self, callback: Callable[[Union[Comment, Post]], Any], **kwargs):
        """Apply a callback function to a stream of Comments and Posts.

        Example:
        A simple example where we want to print the content of each post/comment.

            def process_content(elem: Union[Post, Comment]):
                if isinstance(Post, elem):
                    print(elem.post_view.post.name)
                elif isinstance(Comment, elem):
                    print(elem.comment_view.comment.content)

            multi_stream = lemmy.multi_communities_stream(["community1", "community2"])
            multi_stream.content_apply(process_content)


        :param callback: Function that will be called for each Comment/Post.
        :param kwargs: See the optional arguments in
        [stream_generator][pylemmy.utils.stream_generator].
        """
        posts_fns: List[Callable[[KwArg(Any)], Iterable[Union[Post, Comment]]]] = [
            c.get_posts for c in self.communities
        ]
        comments_fns: List[Callable[[KwArg(Any)], Iterable[Union[Post, Comment]]]] = [
            c.get_comments for c in self.communities
        ]

        posts_unique_keys_fns = [lambda x: "post_" + str(x.post_view.post.ap_id)] * len(
            self.communities
        )
        comments_unique_keys_fns = [
            lambda x: "comment_" + str(x.comment_view.comment.ap_id)
        ] * len(self.communities)
        stream_apply(
            posts_fns + comments_fns,
            posts_unique_keys_fns + comments_unique_keys_fns,
            callback,
            **kwargs,
        )
