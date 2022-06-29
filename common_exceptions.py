from fastapi import HTTPException


def raise_exception(status: int, detail: str):
    raise HTTPException(status_code=status, detail=detail)
