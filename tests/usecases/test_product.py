from store.usecases.product import usecase


async def test_usecases_should_return_success(product_id):
    result = await usecase.create(body=product_id)

    assert isinstance(result, ProductOut)