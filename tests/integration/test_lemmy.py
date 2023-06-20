"""Test the Lemmy class and its modules."""
import pytest

import pylemmy

from .test_api import wait_for_api  # noqa: F401


@pytest.fixture
def lemmy_auth(wait_for_api):  # noqa: F811
    """Fixture to get a Lemmy client to the locally deployed Lemmy."""
    request_session, api_url = wait_for_api

    client = pylemmy.Lemmy(
        lemmy_url=api_url,
        username="lemmy",
        password="lemmylemmy",
        user_agent="pylemmy tests",
    )
    return client


@pytest.fixture
def lemmy_noauth(wait_for_api):  # noqa: F811
    """Fixture to get a Lemmy client without logging in."""
    request_session, api_url = wait_for_api

    client = pylemmy.Lemmy(
        lemmy_url=api_url,
        username=None,
        password=None,
        user_agent="pylemmy tests without login",
    )
    return client


@pytest.fixture
def create_community(lemmy_auth):
    """Fixture to create a Community with the Lemmy client."""
    return lemmy_auth.create_community(name="testcom", title="Test Community")


@pytest.fixture(params=["lemmy_auth", "lemmy_noauth"])
def lemmy_read(request):
    """Fixture for a Lemmy client that doesn't need to login."""
    return request.getfixturevalue(request.param)


def test_create_community(lemmy_read, create_community):
    """Test creating a Community."""
    community_created = create_community.safe
    communities_list = lemmy_read.list_communities()
    assert len(communities_list) == 1
    community = communities_list[0].safe
    assert community.name == community_created.name
    assert community.title == community_created.title
    assert community.id == community_created.id


@pytest.fixture
def create_post(create_community):
    """Fixture to create a Post in the created Community."""
    return create_community.create_post(name="Test post")


def test_create_post(create_post, lemmy_read):
    """Test creating a Post."""
    post_created = create_post.post_view.post
    create_post.community.lemmy = lemmy_read  # change lemmy to the new client
    posts_list = create_post.community.get_posts()
    assert len(posts_list) == 1
    post = posts_list[0].post_view.post
    assert post.name == post_created.name
    assert post.id == post_created.id


@pytest.fixture
def create_comment(create_post):
    """Fixture to create a Comment in the created Post."""
    return create_post.create_comment(content="This is a test comment")


def test_create_comment(create_comment, lemmy_read):
    """Test creating a Comment."""
    comment_created = create_comment.comment_view.comment
    create_comment.community.lemmy = lemmy_read  # change lemmy to the new client
    comments_list = create_comment.post.get_comments()
    assert len(comments_list) == 1
    comment = comments_list[0].comment_view.comment
    assert comment.content == comment_created.content
    assert comment.id == comment_created.id


def test_stream_post(create_post, lemmy_read):
    """Test streaming Posts."""
    post_created = create_post.post_view.post
    create_post.community.lemmy = lemmy_read  # change lemmy to the new client
    community = create_post.community
    for p in community.stream.get_posts(limit=1):
        assert p.post_view.post.name == post_created.name
        assert p.post_view.post.id == post_created.id


def test_stream_comment(create_comment, lemmy_read):
    """Test streaming Comments."""
    comment_created = create_comment.comment_view.comment
    create_comment.community.lemmy = lemmy_read  # change lemmy to the new client
    community = create_comment.community
    for c in community.stream.get_comments(limit=1):
        assert c.comment_view.comment.content == comment_created.content
        assert c.comment_view.comment.id == comment_created.id
