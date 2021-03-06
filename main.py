from fastapi import FastAPI
from booking.routers import booking_router
from account.routers import account_router
from hotel_service.hotel.hotel_routers import hotel_routers
from hotel_service.apartment.apartment_routers import apartment_router
from hotel_service.favorite.favorite_routers import favorite_router
from hotel_service.review.review_routers import review_router
from hotel_service.rating.routers import rating_router

from payment.payment_routers import payment_router

from producer import producer

app = FastAPI(title='hotel_service')


@app.on_event("startup")
async def startup_event():
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()


app.include_router(hotel_routers)
app.include_router(booking_router)
app.include_router(account_router)
app.include_router(apartment_router)
app.include_router(favorite_router)
app.include_router(review_router)
app.include_router(rating_router)
app.include_router(payment_router)
