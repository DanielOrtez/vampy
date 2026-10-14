from pydantic import BaseModel, ConfigDict


class ResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
