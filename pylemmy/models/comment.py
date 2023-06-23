"""Implements the Comment class."""
from typing import Optional

import pylemmy
from pylemmy import api
from pylemmy.endpoints import LemmyAPI


class Comment:
    """A class for Comments."""

    def __init__(
        self,
        lemmy: "pylemmy.Lemmy",
        comment: api.comment.CommentView,
        community: Optional["pylemmy.models.community.Community"] = None,
        post: Optional["pylemmy.models.post.Post"] = None,
    ):
        """Initialize a Comment instance.

        :param lemmy: A Lemmy instance.
        :param comment: A [CommentView](
        https://join-lemmy.org/api/interfaces/CommentView.html).
        :param community: The Community in which this was posted.
        :param post: The Post under which this comment was posted.
        """
        self.lemmy = lemmy
        self.comment_view = comment

        self._post = post
        self._community = community

    @property
    def post(self) -> "pylemmy.models.post.Post":
        """The Post under which this comment was posted."""
        if self._post is None:
            self._post = self.lemmy.get_post(post_id=self.comment_view.post.id)
        return self._post

    @property
    def community(self) -> "pylemmy.models.community.Community":
        """The Community in which this was posted."""
        if self._community is None:
            self._community = self.lemmy.get_community(self.comment_view.community.id)
        return self._community

    def create_report(self, reason: str) -> api.comment.CommentReportView:
        """Report this comment.

        :param reason: A reason for the report.
        """
        payload = api.comment.CreateCommentReport(
            auth=self.lemmy.get_token(),
            comment_id=self.comment_view.post.id,
            reason=reason,
        )
        result = self.lemmy.post_request(LemmyAPI.CreateCommentReport, params=payload)
        parsed_result = api.comment.CommentReportResponse(**result)

        return parsed_result.comment_report_view
