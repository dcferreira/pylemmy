"""Lists Lemmy endpoints."""
from enum import Enum

base_api_path = "/api/v3/"


class LemmyAPI(Enum):
    """Possible Lemmy endpoints."""

    Login = base_api_path + "user/login"
    Community = base_api_path + "community"
    Post = base_api_path + "post"
    Comment = base_api_path + "comment"
    GetComments = base_api_path + "comment/list"
    GetSite = base_api_path + "site"
    GetPosts = base_api_path + "post/list"
    ListCommunities = base_api_path + "community/list"
    CreatePostReport = base_api_path + "post/report"
    CreateCommentReport = base_api_path + "comment/report"
    ListPostReports = base_api_path + "post/report/list"
    ListCommentReports = base_api_path + "comment/report/list"
    ResolvePostReport = base_api_path + "post/report/resolve"
    ResolveCommentReport = base_api_path + "comment/report/resolve"
