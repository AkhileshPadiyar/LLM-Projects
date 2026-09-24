from pydantic import BaseModel

class RagResponse(BaseModel):
    answer : str
    confidence : float
    sources : list[str]