"""LMGTFY Post Stream Reply Bot Example.

Example on how to use pylemmy for monitoring the stream of posts on a particular
community.

This example was heavily inspired by
[PRAW's tutorial](https://praw.readthedocs.io/en/stable/tutorials/reply_bot.html).
"""

from urllib.parse import quote_plus

from pylemmy import Lemmy
from pylemmy.models.post import Post

QUESTIONS = ["what is", "who is", "what are"]
REPLY_TEMPLATE = "[Let me google that for you](https://lmgtfy.com/?q={})"


def main():
    lemmy = Lemmy(
        lemmy_url="http://127.0.0.1:8536",
        username="lemmy",
        password="lemmylemmy",
        user_agent="LMGTFY (by u/USERNAME)",
    )

    community = lemmy.get_community("test")
    for post in community.stream.get_posts():
        process_post(post)


def process_post(post: Post):
    # Ignore titles with more than 10 words as they probably are not simple questions.
    title = post.post_view.post.name
    if len(title.split()) > 10:
        return

    normalized_title = title.lower()
    for question_phrase in QUESTIONS:
        if question_phrase in normalized_title:
            url_title = quote_plus(title)
            reply_text = REPLY_TEMPLATE.format(url_title)
            print(f"Replying to: {title}")
            post.create_comment(reply_text)
            # A reply has been made so do not attempt to match other phrases.
            break


if __name__ == "__main__":
    main()
