from pydantic import BaseModel
from typing import List, Optional

class SourceReference(BaseModel):
    title: str
    link: str

class DebugRequest(BaseModel):
    error: str
    code: Optional[str] = None

class DebugResponse(BaseModel):
    summary: str
    fix: str
    sources: List[SourceReference]