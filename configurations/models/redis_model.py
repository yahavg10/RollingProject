from pydantic import BaseModel, Field


class RedisModel(BaseModel):
    host: str = Field(default="localhost", frozen=True)
    port: int = Field(default=6379, frozen=True)
    db: int = Field(default=0, frozen=True)
