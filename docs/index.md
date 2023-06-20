# pylemmy

pylemmy enables simple access to [Lemmy](https://join-lemmy.org/)'s API with Python.

## Installation

```commandline
pip install pylemmy
```

## Usage

Simple example of running a Python function on new posts, as they are created.

```python
from pylemmy import Lemmy

def process_post(post):
    ...

lemmy = Lemmy(
    lemmy_url="http://127.0.0.1:8536",
    username="lemmy",
    password="lemmylemmy",
    user_agent="custom user agent (by u/USERNAME)",
)

community = lemmy.get_community("test")
for post in community.stream.get_posts():
    process_post(post)
```

For more examples, see [the examples directory on GitHub](https://github.com/dcferreira/pylemmy/tree/main/examples).
