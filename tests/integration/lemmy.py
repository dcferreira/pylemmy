"""Test the Lemmy class and its modules."""
import pytest

import pylemmy

from .api import wait_for_api  # noqa: F401


@pytest.fixture
def lemmy(wait_for_api):  # noqa: F811
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
def create_community(lemmy):
    """Fixture to create a Community with the Lemmy client."""
    return lemmy.create_community(name="testcom", title="Test Community")


def test_create_community(lemmy, create_community):
    """Test creating a Community."""
    community_created = create_community.safe
    communities_list = lemmy.list_communities()
    assert len(communities_list) == 1
    community = communities_list[0].safe
    assert community.name == community_created.name
    assert community.title == community_created.title
    assert community.id == community_created.id


@pytest.fixture
def create_post(create_community):
    """Fixture to create a Post in the created Community."""
    return create_community.create_post(name="Test post")


def test_create_post(create_post):
    """Test creating a Post."""
    post_created = create_post.post_view.post
    posts_list = create_post.community.get_posts()
    assert len(posts_list) == 1
    post = posts_list[0].post_view.post
    assert post.name == post_created.name
    assert post.id == post_created.id


@pytest.fixture
def create_comment(create_post):
    """Fixture to create a Comment in the created Post."""
    return create_post.create_comment(content="This is a test comment")


def test_create_comment(create_comment):
    """Test creating a Comment."""
    comment_created = create_comment.comment_view.comment
    comments_list = create_comment.post.get_comments()
    assert len(comments_list) == 1
    comment = comments_list[0].comment_view.comment
    assert comment.content == comment_created.content
    assert comment.id == comment_created.id
