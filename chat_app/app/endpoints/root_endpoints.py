from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.get("/")
async def top_page():
    return "日記ものせむとて買ひし册子もまだ白紙のまゝなるは、獨逸にて物學びせし間に、一種の「ニル、アドミラリイ」の氣象をや養ひ得たりけむ、あらず、これには別に故あり。 （森鴎外『舞姫』青空文庫）"