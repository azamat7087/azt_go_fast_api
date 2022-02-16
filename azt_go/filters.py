from typing import Optional
from fastapi import Query


def link_filter(category_id: Optional[int] = Query(None, )):
    return {"category_id": category_id, }


