from typing import Optional

from pydantic import BaseModel


class Site(BaseModel):
    actor_id: str
    banner: Optional[str]
    description: str
    icon: str
    id: int
    inbox_url: str
    instance_id: int
    last_refreshed_at: str
    name: str
    private_key: Optional[str]
    public_key: str
    published: str
    sidebar: Optional[str]
    updated: Optional[str]
