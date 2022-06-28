from fastapi import FastAPI
from hotel.routers import hotel_router
from booking.routers import booking_router
from account.routers import account_router

app = FastAPI(title='hotel')

app.include_router(hotel_router)
app.include_router(booking_router)
app.include_router(account_router)
