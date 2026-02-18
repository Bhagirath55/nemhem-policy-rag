from pydantic import BaseModel
from typing import Optional
from datetime import date

class Section(BaseModel):
    act_id: int
    section_id: int
    section_number: str
    title: Optional[str]
    full_text: str
    effective_from: Optional[date]
    effective_to: Optional[date]