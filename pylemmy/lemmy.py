"""Implements the Lemmy class."""
import urllib.parse
from typing import List, Optional, Union

import requests
from pydantic import AnyUrl, BaseModel, parse_obj_as

from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.community import Community
from pylemmy.models.post import Post


class Lemmy:
    """The Lemmy class provides the main entrypoint for pylemmy, and Lemmy's API.

    This class manages all the settings relating how to access your chosen
    Lemmy instance, and implements the Lemmy API.

    Example:

        from pylemmy import Lemmy

        lemmy = Lemmy(
            lemmy_url="http://127.0.0.1:8536",
            username="lemmy",
            password="lemmylemmy",
            user_agent="custom user-agent (by u/USERNAME)",
        )
    """

    def __init__(
        self,
        lemmy_url: Union[str, AnyUrl],
        username: Optional[str],
        password: Optional[str],
        user_agent: str,
        request_timeout: int = 30,
    ):
        """Initialize a Lemmy instance.

        :param lemmy_url: The URL for the Lemmy instance you want to access.
        :param username: Your Lemmy username or email.
        :param password: Your Lemmy password
        :param user_agent: The user agent the requests will use.
        :param request_timeout: A maximum timeout to wait for requests (in seconds).
        """
        self.lemmy_url = (
            lemmy_url
            if isinstance(lemmy_url, AnyUrl)
            else parse_obj_as(AnyUrl, lemmy_url)
        )
        self.username = username
        self.password = password
        self.user_agent = user_agent

        self.request_timeout = request_timeout

        self._login_response: Optional[api.auth.LoginResponse] = None

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def _get_url(self, path: LemmyAPI):
        return urllib.parse.urljoin(self.lemmy_url, path)

    def login(self) -> api.auth.LoginResponse:
        """Login to Lemmy.

        If the user is already logged in, return the response to the original login
        request, with the session information.
        """
        if self._login_response is None:
            if self.username is not None and self.password is not None:
                response = self.post_request(
                    LemmyAPI.login,
                    params=api.auth.Login(
                        username_or_email=self.username, password=self.password
                    ),
                )
                parsed_response = api.auth.LoginResponse(**response)
                if parsed_response.jwt is None:
                    msg = "Couldn't login! Have you verified your email?"
                    raise RuntimeError(msg)
                self._login_response = parsed_response
            else:
                msg = "Need to provide username and password!"
                raise ValueError(msg)
        return self._login_response

    def get_token(self) -> str:
        """Get the jwt session token."""
        jwt = self.login().jwt
        if jwt is None:
            msg = "No jwt token was found, try logging in again."
            raise RuntimeError(msg)
        return jwt

    def get_community(self, community: Union[str, int]) -> Community:
        """Get a community by id or name.

        :param community: Either a community id (int) or name (str).
        """
        if isinstance(community, str):
            payload = api.community.GetCommunity(auth=self.get_token(), name=community)
        elif isinstance(community, int):
            payload = api.community.GetCommunity(auth=self.get_token(), id=community)
        else:
            raise ValueError()

        result = self.get_request(LemmyAPI.community, params=payload)
        parsed_result = api.community.GetCommunityResponse(**result)
        return Community(self, parsed_result.community_view)

    def create_community(self, name: str, title: str, **kwargs) -> Community:
        """Create a community with the given name and title.

        :param name: Name of the community (stub-like, this will be in the URL).
        :param title: Title of the community, in natural language.
        :param kwargs: See optional arguments in [CreateCommunity](
        https://join-lemmy.org/api/interfaces/CreateCommunity.html).
        """
        payload = api.community.CreateCommunity(
            auth=self.get_token(), name=name, title=title, **kwargs
        )
        result = self.post_request(LemmyAPI.community, params=payload)
        parsed_result = api.community.CommunityResponse(**result)

        return Community(self, parsed_result.community_view)

    def list_communities(self, **kwargs) -> List[Community]:
        """List the communities in the current Lemmy instance.

        :param kwargs: See optional arguments in [ListCommunities](
        https://join-lemmy.org/api/interfaces/ListCommunities.html).
        """
        payload = api.community.ListCommunities(auth=self.get_token(), **kwargs)
        result = self.get_request(LemmyAPI.list_communities, params=payload)
        parsed_result = api.community.ListCommunitiesResponse(**result)

        return [Community(self, view) for view in parsed_result.communities]

    def get_post(
        self, *, post_id: Optional[int] = None, comment_id: Optional[int] = None
    ) -> Post:
        """Get a post from its id.

        :param post_id: Id of the post.
        :param comment_id: Id of the comment.
        """
        if post_id is not None:
            payload = api.post.GetPost(auth=self.get_token(), id=post_id)
        elif comment_id is not None:
            payload = api.post.GetPost(auth=self.get_token(), comment_id=comment_id)
        else:
            msg = "Need to give either a post id or a comment id."
            raise ValueError(msg)

        result = self.get_request(LemmyAPI.post, params=payload)
        parsed_result = api.post.GetPostResponse(**result)

        return Post(self, parsed_result.post_view)

    def post_request(
        self,
        path: LemmyAPI,
        params: Optional[BaseModel] = None,
    ):
        """Send a POST request to the desired path.

        :param path: A Lemmy endpoint.
        :param params: Parameters to send with the request (in the body).
        """
        response = self.session.post(
            self._get_url(path),
            json=params.dict() if params is not None else {},
            timeout=self.request_timeout,
        )
        return response.json()

    def get_request(
        self,
        path: LemmyAPI,
        params: Optional[BaseModel] = None,
    ):
        """Send a GET request to the desired path.

        :param path: A Lemmy endpoint.
        :param params: Parameters to send with the request (in the URL).
        """
        response = self.session.get(
            self._get_url(path),
            params=params.dict() if params is not None else {},
            timeout=self.request_timeout,
        )
        return response.json()
