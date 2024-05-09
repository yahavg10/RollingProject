from pydantic import BaseModel


class Loader(BaseModel):
    loading_function: str
    package_name: str
    sub_package_name: str
    strategy_module: str
    load_method: str
