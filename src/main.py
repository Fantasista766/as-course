from pathlib import Path
import sys

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.bookings import router as router_bookings
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
