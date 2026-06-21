from src.axentx_product.product import Product

def test_product_creation():
    product = Product("Test Product", "This is a test product", 10.99)
    assert product.name == "Test Product"
    assert product.description == "This is a test product"
    assert product.price == 10.99

def test_product_string_representation():
    product = Product("Test Product", "This is a test product", 10.99)
    assert str(product) == "Test Product: This is a test product, $10.99"
