from uuid import UUID

import pymongo
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection('products')

    async def create(self, body: ProductIn) -> ProductOut:
        product = ProductOut(**body.model_dump())
        await self.collection.insert_one(product.model_dump())
        return product

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({'_id': id})

        if not result:
            raise HTTPException(status_code=404, detail='Product not found')
        return ProductOut(**result)

    async def query(self) -> list[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={'id': id},
            update={'$set': body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER
        )
        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.delete_one({'id': id})

        return True if result.deleted_count > 0 else False


usecase = ProductUsecase()
