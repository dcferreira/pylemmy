from typing import Optional

from pylemmy.api.utils import BaseApiModel


class Site(BaseApiModel):
    actor_id: str
    banner: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    id: int
    inbox_url: str
    instance_id: int
    last_refreshed_at: str
    name: str
    private_key: Optional[str] = None
    public_key: str
    published: str
    sidebar: Optional[str] = None
    updated: Optional[str] = None
