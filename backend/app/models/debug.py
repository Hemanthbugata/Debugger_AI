from pydantic import BaseModel
from typing import List

class SourceReference(BaseModel):
    title: str
    link: str

class DebugRequest(BaseModel):
    error: str

class DebugResponse(BaseModel):
    summary: str
    fix: str
    sources: List[SourceReference]