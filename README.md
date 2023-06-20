# pylemmy

[![PyPI - Version](https://img.shields.io/pypi/v/pylemmy.svg)](https://pypi.org/project/pylemmy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pylemmy.svg)](https://pypi.org/project/pylemmy)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
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

## License

`pylemmy` is distributed under the terms of the 
[MIT](https://spdx.org/licenses/MIT.html) license.
