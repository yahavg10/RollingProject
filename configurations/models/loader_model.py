from pydantic import BaseModel


class Loader(BaseModel):
    loading_function: str
    strategy_module: str
