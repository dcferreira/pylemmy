from pydantic import BaseModel, ConfigDict


class BaseApiModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
