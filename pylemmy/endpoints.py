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
