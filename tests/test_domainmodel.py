from domainmodel import Batch, OrderLine

from pytest import raises, fixture


def create_batch_orderline(sku, batch_qty, line_qty):
    return Batch(reference="batch_1", sku=sku, quantity=batch_qty, eta=""), OrderLine(
        id="orderline-1", sku=sku, quantity=line_qty
    )


@fixture
def line_big():
    return OrderLine(id="orderline-big", sku="test", quantity=20)


@fixture
def line_small():
    return OrderLine(id="orderline-small", sku="est", quantity=5)


def test_line_post_init():
    with raises(ValueError):
        OrderLine(id="lil", sku="test", quantity=-1)


def test_line_eq(line_big, line_small):
    order2 = line_big

    assert line_small != line_big
    assert order2 == line_big


def test_batch_add_available_quantity(line_big):
    b = Batch(reference=1, sku=line_big.sku, quantity=line_big.quantity, eta=None)
    b.add_available_quantity(line_big)

    assert b.available == 2 * line_big.quantity


def test_can_allocate_if_available_greater_than_requested():
    large_batch, small_order = create_batch_orderline("ELEGANT-LAMP", 20, 10)

    assert large_batch.can_allocate(small_order)


def test_cannot_allocate_if_available_smaller_than_requested():
    small_batch, large_order = create_batch_orderline("ELEGANT-LAMP", 10, 20)

    assert small_batch.can_allocate(large_order) is False


def test_raise_error_if_sku_non_compatible(line_small):
    batch, _ = create_batch_orderline("TEST", 20, 10)

    assert batch.can_allocate(line_small) is False


def test_allocate_order():
    batch, orderline = create_batch_orderline(
        sku="LAMP-IKEA",
        batch_qty=20,
        line_qty=10,
    )

    batch.allocate(orderline)
    assert batch.available == 10


def test_ignore_twice_allocate_order():
    batch, orderline = create_batch_orderline(
        sku="LAMP-IKEA",
        batch_qty=20,
        line_qty=10,
    )

    batch.allocate(orderline)
    assert batch.available == 10

    batch.allocate(orderline)
    assert batch.available == 10


def test_deallocate_unallocated_order():
    batch, orderline = create_batch_orderline(
        sku="LAMP-IKEA",
        batch_qty=20,
        line_qty=10,
    )

    batch.deallocate(orderline)
    assert batch.available == 20


def test_deallocate_allocated_order():
    batch, orderline = create_batch_orderline(
        sku="LAMP-IKEA",
        batch_qty=20,
        line_qty=10,
    )

    batch.allocate(orderline)
    assert batch.available == 10

    batch.deallocate(orderline)
    assert batch.available == 20
