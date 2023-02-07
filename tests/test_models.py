from flaskapp.models.product import ProductModel


def test_new_product():
    """
    GIVEN a Product model
    WHEN a new Product is created
    THEN check the id and price fields are defined correctly
    """
    product = ProductModel(id="10056", price=100)
    assert product.id == "10056"
    assert product.price == 100.0
