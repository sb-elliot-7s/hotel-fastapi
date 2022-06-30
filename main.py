from fastapi import FastAPI
from booking.routers import booking_router
from account.routers import account_router
from hotel_service.hotel.hotel_routers import hotel_routers

app = FastAPI(title='hotel_service')

app.include_router(hotel_routers)
app.include_router(booking_router)
app.include_router(account_router)
