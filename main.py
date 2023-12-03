from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from searchV2 import search_destinations

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/status")
async def message():
    return {"message": "Hello Word"}


@router.get("/search")
async def search(max_days:int, max_budget:int, current_location:tuple[float,float] = (112.75, -7.25)):
    return search_destinations(max_days, max_budget, current_location)


app.include_router(router, prefix='/api')