#!/usr/bin/env python

# http://pytest.org/
# run py.test to run the tests (it magically finds things
# called test_blah and runs them)

from gsp import GSP

def test_mechanism():
    num_slots = 4
    slot_clicks = [1] * 4   # don't actually matter for gsp
    bids = zip(range(1,6), [10, 12, 18, 14, 20])

    reserve = 0

    (alloc, payments) = GSP.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3,4,2]
    assert payments == [18, 14, 12, 10]

    reserve = 11
    (alloc, payments) = GSP.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3,4,2]
    assert payments == [18, 14, 12, 11]

    reserve = 14
    (alloc, payments) = GSP.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3,4]
    assert payments == [18, 14, 14]

    reserve = 15
    (alloc, payments) = GSP.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3]
    assert payments == [18, 15]

    reserve = 19
    (alloc, payments) = GSP.compute(slot_clicks, reserve, bids)
    assert alloc == [5]
    assert payments == [19]


    reserve = 22
    (alloc, payments) = GSP.compute(slot_clicks, reserve, bids)
    assert alloc == []
    assert payments == []


def test_bid_ranges():
    num_slots = 4
    slot_clicks = [1] * 4   # don't actually matter for gsp
    bids = zip(range(1,6), [10, 12, 18, 14, 20])

    def bid_range(slot, reserve):
        return GSP.bid_range_for_slot(slot, slot_clicks, reserve, bids)

    reserve = 0
    assert bid_range(0, reserve) == (20, None)
    assert bid_range(1, reserve) == (18, 20)
    assert bid_range(2, reserve) == (14, 18)
    assert bid_range(3, reserve) == (12, 14)
    assert bid_range(4, reserve) == (10, 12)
    assert bid_range(7, reserve) == (0, 10)

    reserve = 15
    assert bid_range(0, reserve) == (20, None)
    assert bid_range(1, reserve) == (18, 20)
    assert bid_range(2, reserve) == (15, 18)
    assert bid_range(3, reserve) == (15, 18)
    assert bid_range(7, reserve) == (15, 18)

    reserve = 22
    assert bid_range(0, reserve) == (22, None)
    assert bid_range(1, reserve) == (22, 22)
    assert bid_range(2, reserve) == (22, 22)
