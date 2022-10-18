from domainmodel import Order, Batch

from pytest import raises

def test_order_post_init():
    with raises(ValueError):
        a = Order(sku="test", quantity=-1)