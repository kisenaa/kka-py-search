from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from searchV2 import search_destinations

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def dispatch(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@router.get("/status")
async def message():
    return {"message": "Hello Word"}


@router.get("/search")
async def search(max_days:int, max_budget:int, current_location:tuple[float,float] = (112.75, -7.25)):
    return search_destinations(max_days, max_budget, current_location)


app.include_router(router, prefix='/api')