from pydantic import BaseModel


class BaseApiModel(BaseModel):
    class Config:
        use_enum_values = True
