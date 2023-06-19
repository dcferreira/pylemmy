import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import pylemmy

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


@pytest.fixture
def lemmy(wait_for_api):
    request_session, api_url = wait_for_api

    client = pylemmy.Lemmy(
        lemmy_url=api_url,
        username="lemmy",
        password="lemmylemmy",
        user_agent="pylemmy tests",
    )
    return client


@pytest.fixture
def create_community(lemmy):
    return lemmy.create_community(name="testcom", title="Test Community")


def test_create_community(lemmy, create_community):
    community_created = create_community.safe
    communities_list = lemmy.list_communities()
    assert len(communities_list) == 1
    community = communities_list[0].safe
    assert community.name == community_created.name
    assert community.title == community_created.title
    assert community.id == community_created.id


@pytest.fixture
def create_post(create_community):
    return create_community.create_post(name="Test post")


def test_create_post(create_post):
    post_created = create_post.post_view.post
    posts_list = create_post.community.get_posts()
    assert len(posts_list) == 1
    post = posts_list[0].post_view.post_request
    assert post.name == post_created.name
    assert post.id == post_created.id


@pytest.fixture
def create_comment(create_post):
    return create_post.create_comment(content="This is a test comment")


def test_create_comment(create_comment):
    comment_created = create_comment.comment_view.comment
    comments_list = create_comment.post.get_comments()
    assert len(comments_list) == 1
    comment = comments_list[0].comment_view.comment
    assert comment.content == comment_created.content
    assert comment.id == comment_created.id
