"""Lists Lemmy endpoints."""


from enum import Enum

base_api_path = "/api/v3/"


class LemmyAPI(str, Enum):
    """Possible Lemmy endpoints."""

    login = base_api_path + "user/login"
    community = base_api_path + "community"
    post = base_api_path + "post"
    comment = base_api_path + "comment"
    get_comments = base_api_path + "comment/list"
    get_site = base_api_path + "site"
    get_posts = base_api_path + "post/list"
    list_communities = base_api_path + "community/list"
