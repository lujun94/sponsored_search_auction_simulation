#!/usr/bin/env python

# http://pytest.org/
# run py.test to run the tests (it magically finds things
# called test_blah and runs them)

from vcg import VCG

# vcg payment: util to others without you - util to others with you
# for ad slots: no change for slots above yours. So
#   sum_{i \in higher-num-slots} (clicks_{i-1} - click_{i}) b_i
#   + clicks{n} * b_{n+1}  # (first not-allocated slot)
# if we want per-click payments, need to normalize by click_{i}...

def test_mechanism():
    num_slots = 4
    slot_clicks = [4,3,2,1]
    bids = zip(range(1,6), [10, 12, 18, 14, 20])
    # values, clicks: (20, 4); (18, 3); (14, 2); (12, 1); (10, 0)
    # payments: [18+14+12+10 = 54, 14+12+10 = 36, 10+12 = 22, 10] = [54, 36, 22, 10]

    def norm(totals):
        """Normalize total payments by the clicks in each slot"""
        return map(lambda (x,y): x/y, zip(totals, slot_clicks))
    
    # Allocs same as GSP, but payments are different
    reserve = 0
    (alloc, payments) = VCG.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3,4,2]
    assert payments == norm([54, 36, 22, 10])

    reserve = 11
    (alloc, payments) = VCG.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3,4,2]
    assert payments == norm([55, 37, 23, 11])

    reserve = 14
    (alloc, payments) = VCG.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3,4]
    # values, clicks: (20, 4); (18, 3); (14, 2); "(14, 1)"; "(14,0)"
    # payments: [18+14+14+14 = 60, 14+14+14 = 42, 14, "14'] = 

    assert payments == norm([60, 42, 28])

    reserve = 15
    (alloc, payments) = VCG.compute(slot_clicks, reserve, bids)
    assert alloc == [5,3]
    assert payments == norm([63, 45])

    reserve = 19
    (alloc, payments) = VCG.compute(slot_clicks, reserve, bids)
    assert alloc == [5]
    assert payments == norm([76])

    reserve = 22
    (alloc, payments) = VCG.compute(slot_clicks, reserve, bids)
    assert alloc == []
    assert payments == []


def test_bid_ranges():
    # Same as for GSP--the bid ranges don't change if the bids are the same
    num_slots = 4
    slot_clicks = [4,3,2,1]
    bids = zip(range(1,6), [10, 12, 18, 14, 20])

    def bid_range(slot, reserve):
        return VCG.bid_range_for_slot(slot, slot_clicks, reserve, bids)

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
