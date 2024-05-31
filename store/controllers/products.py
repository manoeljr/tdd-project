from typing import List

from fastapi import APIRouter, status, Body, Depends, Path, HTTPException
from pydantic import UUID4

from store import usecases
from store.schemas.product import ProductIn, ProductOut, ProductUpdate

router = APIRouter(tags=['products'])


@router.post(path='/', status_code=status.HTTP_201_CREATED)
async def post(body: ProductIn = Body(...), usecase: usecases = Depends()) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path='/{id}', status_code=status.HTTP_200_OK)
async def get(id: UUID4 = Path(alias='id'), usecase: usecases = Depends()) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(path='/', status_code=status.HTTP_200_OK)
async def query(usecase: usecases = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(path='/{id}', status_code=status.HTTP_200_OK)
async def patch(
        id: UUID4 = Path(alias='id'), body: ProductUpdate = Body(...), usecase: usecases = Depends()
) -> ProductOut:
    return await usecase.update(id=id)


@router.delete(path='/{id}', status_code=status.HTTP_200_OK)
async def delete(id: UUID4 = Path(alias='id'), usecase: usecases = Depends()) -> None:
    await usecase.delete(id=id)
