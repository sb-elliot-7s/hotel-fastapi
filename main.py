from fastapi import FastAPI
from hotel.routers import hotel_router

app = FastAPI(title='hotel')
app.include_router(hotel_router)
