import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from pylemmy.endpoints import LemmyAPI

pytest_plugins = ["docker_compose"]


@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter):
    """Wait for the api from lemmy to become responsive."""
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    service = function_scoped_container_getter.get_request("lemmy").network_info[0]
    api_url = f"http://{service.hostname}:{service.host_port}"
    assert request_session.get(api_url)
    return request_session, api_url


def test_get_site(wait_for_api):
    request_session, api_url = wait_for_api

    url = f"{api_url}{LemmyAPI.get_site}"
    response = request_session.get_request(url)
    assert response.status_code == 200


@pytest.fixture()
def login(wait_for_api):
    request_session, api_url = wait_for_api
    url = f"{api_url}{LemmyAPI.login}"
    response = request_session.post_request(
        url, json={"username_or_email": "lemmy", "password": "lemmylemmy"}
    )
    return response.json()["jwt"]


def test_login(wait_for_api):
    request_session, api_url = wait_for_api
    url = f"{api_url}{LemmyAPI.login}"
    response = request_session.post_request(
        url, json={"username_or_email": "lemmy", "password": "lemmylemmy"}
    )
    return response


@pytest.fixture
def create_community(wait_for_api, login):
    request_session, api_url = wait_for_api
    url = f"{api_url}{LemmyAPI.community}"
    name = "testcom"
    title = "Test Community"
    response = request_session.post_request(
        url, json={"auth": login, "name": name, "title": title}
    )
    return response


def test_create_community(wait_for_api, create_community):
    request_session, api_url = wait_for_api

    assert create_community.status_code == 200
    community_created = create_community.json()["community_view"]["community"]

    list_url = f"{api_url}{LemmyAPI.list_communities}"
    list_response = request_session.get_request(list_url)
    communities_list = list_response.json()["communities"]
    assert len(communities_list) == 1
    community = communities_list[0]["community"]
    assert community["name"] == community_created["name"]
    assert community["title"] == community_created["title"]
    assert community["id"] == community_created["id"]


@pytest.fixture
def create_post(wait_for_api, login, create_community):
    request_session, api_url = wait_for_api
    community_created = create_community.json()["community_view"]["community"]

    post_url = f"{api_url}{LemmyAPI.post}"
    post_response = request_session.post_request(
        post_url,
        json={
            "auth": login,
            "community_id": community_created["id"],
            "name": "Test post",
        },
    )
    return post_response


def test_create_post(wait_for_api, create_post):
    request_session, api_url = wait_for_api
    assert create_post.status_code == 200

    post_created = create_post.json()["post_view"]["post"]

    list_posts = f"{api_url}{LemmyAPI.get_posts}"
    list_response = request_session.get_request(list_posts)
    posts_list = list_response.json()["posts"]
    assert len(posts_list) == 1
    community = posts_list[0]["post"]
    assert community["name"] == post_created["name"]
    assert community["id"] == post_created["id"]


@pytest.fixture
def create_comment(wait_for_api, login, create_post):
    request_session, api_url = wait_for_api
    post_created = create_post.json()["post_view"]["post"]

    comment_url = f"{api_url}{LemmyAPI.comment}"
    comment_response = request_session.post_request(
        comment_url,
        json={
            "auth": login,
            "post_id": post_created["id"],
            "content": "This is a test comment",
        },
    )
    return comment_response


def test_create_comment(wait_for_api, create_comment):
    request_session, api_url = wait_for_api
    assert create_comment.status_code == 200

    comment_created = create_comment.json()["comment_view"]["comment"]

    list_comments = f"{api_url}{LemmyAPI.get_comments}"
    list_response = request_session.get_request(list_comments)
    posts_list = list_response.json()["comments"]
    assert len(posts_list) == 1
    community = posts_list[0]["comment"]
    assert community["content"] == comment_created["content"]
    assert community["id"] == comment_created["id"]
