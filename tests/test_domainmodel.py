from domainmodel import Order, Batch

from pytest import raises, fixture

@fixture
def order():
    return Order(sku='test', quantity=2)

@fixture
def order1():
    return Order(sku='est', quantity=1)

def test_order_post_init():
    with raises(ValueError):
        a = Order(sku="test", quantity=-1)

def test_order_sub(order, order1):
    order2 = Order(sku="test", quantity=1)

    with raises(ValueError):
        order3 = order - order1

    order3 = order - order2

    assert order2.sku == order.sku
    assert order3.sku == order.sku
    assert order3.quantity == order.quantity - order2.quantity

def test_order_eq(order, order1):
    order2 = order

    assert order1 != order
    assert order2 == order