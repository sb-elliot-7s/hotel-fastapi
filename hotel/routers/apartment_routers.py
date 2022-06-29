from fastapi import APIRouter, Depends, status
from .deps import get_hotel_collection

hotel_router = APIRouter(prefix='/hotel', tags=['hotel'])
