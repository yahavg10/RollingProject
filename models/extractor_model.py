from pydantic import BaseModel


class Extractor(BaseModel):
    extraction_function: str
    package_name: str
    sub_package_name: str
    strategy_module: str
    extract_method: str
    input_path: str
