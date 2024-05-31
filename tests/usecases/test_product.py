from typing import List
from uuid import UUID

import pytest

from store.schemas.product import ProductOut
from store.usecases.product import usecase


async def test_usecases_create_should_return_success(product_in):
    result = await usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_return_success(product_id):
    result = await usecase.get(id=product_id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_return_not_found(product_id):
    with pytest.raises(Exception) as err:
        await usecase.get(id=UUID('1e4f214e-85f7-461a-89d0-a751a32e3bb9'))

    assert err.value.args[0] == f"Product not found with filter: {UUID('1e4f214e-85f7-461a-89d0-a751a32e3bb9')}"


async def test_usecases_query_should_return_success():
    result = await usecase.query()

    assert isinstance(result, List)


async def test_usecases_update_should_return_success(product_id, product_up):
    result = await usecase.update(id=product_id, body=product_up)

    assert isinstance(result, ProductOut)

