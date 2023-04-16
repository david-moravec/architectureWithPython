from domainmodel import Order, Batch, SkuErorr

from pytest import raises, fixture


def make_batch_orderline(sku, batch_qty, line_qty):
    return Batch(
        reference=1, contents=Order(sku=sku, quantity=batch_qty), eta=""
    ), Order(sku=sku, quantity=line_qty)


@fixture
def order_big():
    return Order(sku="test", quantity=20)


@fixture
def order_small():
    return Order(sku="est", quantity=5)


def test_order_post_init():
    with raises(ValueError):
        Order(sku="test", quantity=-1)


def test_order_sub(order_big, order_small):
    order2 = Order(sku="test", quantity=1)

    with raises(ValueError):
        order3 = order_big - order_small

    order3 = order_big - order2

    assert order2.sku == order_big.sku
    assert order3.sku == order_big.sku
    assert order3.quantity == order_big.quantity - order2.quantity


def test_order_eq(order_big, order_small):
    order2 = order_big

    assert order_small != order_big
    assert order2 == order_big


def test_batch_add_available_quantity(order_big):
    b = Batch(reference=1, contents=order_big, eta=None)
    b.add_available_quantity(order_big)

    assert b.available.quantity == 2 * order_big.quantity


def test_can_allocate_if_available_greater_than_requested():
    large_batch, small_order = make_batch_orderline("ELEGANT-LAMP", 20, 10)

    assert large_batch.can_allocate(small_order)


def test_cannot_allocate_if_available_smaller_than_requested():
    small_batch, large_order = make_batch_orderline("ELEGANT-LAMP", 10, 20)

    assert small_batch.can_allocate(large_order) is False


def test_raise_error_if_sku_non_compatible(order_small):
    batch, _ = make_batch_orderline("TEST", 20, 10)

    assert batch.can_allocate(order_small) is False
