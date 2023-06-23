"""Implements the Post class."""
from typing import List, Optional

import pylemmy
from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.comment import Comment


class PostReport:
    """A class for Post reports."""

    def __init__(
        self,
        lemmy: "pylemmy.Lemmy",
        report: api.post.PostReportView,
        post: Optional["Post"] = None,
    ):
        """Initialize a Post instance.

        :param lemmy: A Lemmy instance.
        :param report: A [PostReportView](
        https://join-lemmy.org/api/interfaces/PostReportView.html).
        :param post: The post being reported.
        """
        self.lemmy = lemmy
        self.report_view = report
        self.post = post

    def resolve(self, *, resolved: bool) -> "PostReport":
        """Resolve a post report.

        :param resolved: Either resolve or unresolve the report.
        """
        payload = api.post.ResolvePostReport(
            auth=self.lemmy.get_token(),
            report_id=self.report_view.post_report.id,
            resolved=resolved,
        )
        result = self.lemmy.put_request(LemmyAPI.ResolvePostReport, params=payload)
        parsed_result = api.post.PostReportView(**result)

        return PostReport(lemmy=self.lemmy, report=parsed_result, post=self.post)


class Post:
    """A class for Posts."""

    def __init__(
        self,
        lemmy: "pylemmy.Lemmy",
        post: api.post.PostView,
        community: Optional["pylemmy.models.community.Community"] = None,
    ):
        """Initialize a Post instance.

        :param lemmy: A Lemmy instance.
        :param post: A [PostView](
        https://join-lemmy.org/api/interfaces/PostView.html).
        :param community: The Community in which this was posted.
        """
        self.lemmy = lemmy
        self.post_view = post

        self._community = community

    @property
    def community(self) -> "pylemmy.models.community.Community":
        """The Community in which this Post was posted."""
        if self._community is None:
            self._community = self.lemmy.get_community(self.post_view.community.id)
        return self._community

    def create_comment(self, content: str, **kwargs) -> Comment:
        """Create a new Comment under this Post.

        :param content: Content of the comment.
        :param kwargs: See optional arguments in [CreateComment](
        https://join-lemmy.org/api/interfaces/CreateComment.html).
        """
        payload = api.comment.CreateComment(
            auth=self.lemmy.get_token(),
            content=content,
            post_id=self.post_view.post.id,
            **kwargs,
        )
        result = self.lemmy.post_request(LemmyAPI.Comment, params=payload)
        parsed_result = api.comment.CommentResponse(**result)

        return Comment(
            self.lemmy, parsed_result.comment_view, post=self, community=self._community
        )

    def get_comments(self, **kwargs) -> List[Comment]:
        """Get Comments under this Post.

        :param kwargs: See optional arguments in [GetComments](
        https://join-lemmy.org/api/interfaces/GetComments.html).
        """
        payload = api.comment.GetComments(
            auth=self.lemmy.get_token_optional(),
            post_id=self.post_view.post.id,
            **kwargs,
        )
        result = self.lemmy.get_request(LemmyAPI.GetComments, params=payload)
        parsed_result = api.comment.GetCommentsResponse(**result)

        return [
            Comment(self.lemmy, comment, post=self, community=self._community)
            for comment in parsed_result.comments
        ]

    def create_report(self, reason: str) -> PostReport:
        """Report this post.

        :param reason: A reason for the report.
        """
        payload = api.post.CreatePostReport(
            auth=self.lemmy.get_token(), post_id=self.post_view.post.id, reason=reason
        )
        result = self.lemmy.post_request(LemmyAPI.CreatePostReport, params=payload)
        parsed_result = api.post.PostReportResponse(**result)

        return PostReport(
            lemmy=self.lemmy, report=parsed_result.post_report_view, post=self
        )
