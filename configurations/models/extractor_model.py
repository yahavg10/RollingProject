from pydantic import BaseModel


class Extractor(BaseModel):
    extraction_function: str
    strategy_module: str
    input_path: str
