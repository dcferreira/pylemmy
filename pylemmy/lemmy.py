import urllib.parse
from typing import List, Optional, Union

import requests
from pydantic import AnyUrl, BaseModel, parse_obj_as

from pylemmy import api
from pylemmy.endpoints import LemmyAPI
from pylemmy.models.community import Community
from pylemmy.models.post import Post


class Lemmy:
    def __init__(
        self,
        lemmy_url: Union[str, AnyUrl],
        username: Optional[str],
        password: Optional[str],
        user_agent: str,
        request_timeout: int = 30,
    ):
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

    def _get_url(self, path: LemmyAPI):
        return urllib.parse.urljoin(self.lemmy_url, path)

    def login(self):
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

    def get_token(self):
        return self.login().jwt

    def get_community(self, community: Union[str, int]) -> Community:
        if isinstance(community, str):
            payload = api.community.GetCommunity(auth=self.get_token(), name=community)
        elif isinstance(community, int):
            payload = api.community.GetCommunity(auth=self.get_token(), id=community)
        else:
            raise ValueError()

        result = self.get_request(LemmyAPI.community, params=payload)
        parsed_result = api.community.GetCommunityResponse(**result)
        return Community(self, parsed_result.community_view)

    def create_community(
        self,
        name: str,
        title: str,
        banner: Optional[str] = None,
        description: Optional[str] = None,
        discussion_languages: Optional[List[int]] = None,
        icon: Optional[str] = None,
        nsfw: Optional[bool] = None,
        posting_restricted_to_mods: Optional[bool] = None,
    ) -> Community:
        payload = api.community.CreateCommunity(
            auth=self.get_token(),
            name=name,
            title=title,
            banner=banner,
            description=description,
            discussion_languages=discussion_languages,
            icon=icon,
            nsfw=nsfw,
            posting_restricted_to_mods=posting_restricted_to_mods,
        )
        result = self.post_request(LemmyAPI.community, params=payload)
        parsed_result = api.community.CommunityResponse(**result)

        return Community(self, parsed_result.community_view)

    def list_communities(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        sort: Optional[api.listing.SortType] = None,
        type_: Optional[api.listing.ListingType] = None,
    ) -> List[Community]:
        payload = api.community.ListCommunities(
            auth=self.get_token(), limit=limit, page=page, sort=sort, type_=type_
        )
        result = self.get_request(LemmyAPI.list_communities, params=payload)
        parsed_result = api.community.ListCommunitiesResponse(**result)

        return [Community(self, view) for view in parsed_result.communities]

    def get_post(
        self, *, post_id: Optional[int] = None, comment_id: Optional[int] = None
    ) -> Post:
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
        response = requests.post(
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
        response = requests.get(
            self._get_url(path),
            params=params.dict() if params is not None else {},
            timeout=self.request_timeout,
        )
        return response.json()
