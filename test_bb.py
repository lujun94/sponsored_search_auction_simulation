#!/usr/bin/env python

# http://pytest.org/
# run py.test to run the tests (it magically finds things
# called test_blah and runs them)

from auction import History
from bbagent import BBAgent


def dual_assert(x,y):
    B = (x==y or int(x)==int(y))
    assert B

def test_bb():
    budget = 1000  # don't want binding budget for this test 
    t = 1  # considering the decision for round 1, after the hard-coded round 0
    # Hand-constructed example

    # values [8, 10, 20]
    # clicks [3, 2, 0]
    # reserve = 0

    reserve = 0
     
    bids = [[(3, 10), (2, 5), (1, 4)]]
    occupants = [[3, 2, 1]]
    slot_clicks = [[3, 2, 0]]
    per_click_payments = [[5, 4, 0]]
    slot_payments = [[15, 8, 0]]
     
    history = History(bids, occupants, slot_clicks, per_click_payments, slot_payments)

    a1 = BBAgent(1, 8, budget)
    a2 = BBAgent(2, 10, budget)
    a3 = BBAgent(3, 20, budget)

    # a1's utils for slots: [3 * (8-10), 2*(8-5), 0] = [-6, 6, 0]
    assert a1.expected_utils(t, history, reserve) == [-6, 6, 0]
    assert a1.target_slot(t, history, reserve) == (1, 5, 10)
    # bid for slot 1: 8 - 2/3 * (8 - 5) = 8 - 2/3(3) = 6
    dual_assert(a1.bid(t, history, reserve), 6)

    # a2's utils for slots: [3 * (10 - 10), 2*(10-4), 0] = [0, 12, 0]
    assert a2.expected_utils(t, history, reserve) == [0, 12, 0]
    assert a2.target_slot(t, history, reserve) == (1, 4, 10)
    # bid for slot 1: 10 - 2/3 * (10 - 4) = 10 - 4 = 6
    dual_assert (a2.bid(t, history, reserve) , 6)

    # a3's utils for slots: [3 * (20 - 5), 2*(20-4), 0] = [45, 32, 0]
    assert a3.expected_utils(t, history, reserve) == [45, 32, 0]
    assert a3.target_slot(t, history, reserve) == (0, 5, 10)
    # bid for slot 0: 20 (your value)   
    dual_assert (a3.bid(t, history, reserve), 20)
    print "\n\tFinished test_bb"
    
def test_bb_reserve():
    budget = 1000  # don't want binding budget for this test 
    t = 1  # considering the decision for round 1, after the hard-coded round 0

    # Hand-constructed example:
    # values [8, 10, 20]
    # clicks [3, 2, 1]
    # reserve = 0

    reserve = 5
     
    bids = [[(3, 10), (2, 7), (1, 6)]]
    occupants = [[3, 2, 1]]
    slot_clicks = [[3, 2, 1]]
    per_click_payments = [[7, 6, 5]]
    slot_payments = [[21, 12, 5]]
     
    history = History(bids, occupants, slot_clicks, per_click_payments, slot_payments)

    a1 = BBAgent(1, 8, budget)
    a2 = BBAgent(2, 10, budget)
    a3 = BBAgent(3, 20, budget)

    # Test both with reserve and without
    # a1's utils for slots: [3 * (8-10), 2*(8-7), 1*(8-5)] = [-6, 2, 3]
    assert a1.expected_utils(t, history, reserve) == [-6, 2, 3]
    assert a1.target_slot(t, history, reserve) == (2, 5, 7)
    # bid for slot 1: 8 - 1/2 * (8 - 5) = 8 - 1.5 = 6.5 -> 6
    dual_assert(a1.bid(t, history, reserve), 6.5)

    # a2's utils for slots: [3 * (10 - 10), 2*(10-6), 1*(10-5)] = [0, 8, 5]
    assert a2.expected_utils(t, history, reserve) == [0, 8, 5]
    assert a2.target_slot(t, history, reserve) == (1, 6, 10)
    # bid for slot 1: 10 - 2/3 * (10 - 6) = 10 - 8/3 = 7.333 -> 7
    dual_assert(a2.bid(t, history, reserve),  10-8.0/3)

    # a3's utils for slots: [3 * (20 - 7), 2 * (20-6), 1*(20-5)] = [39, 28, 15]
    assert a3.expected_utils(t, history, reserve) == [39, 28, 15]
    assert a3.target_slot(t, history, reserve) == (0, 7, 14)
    # bid for slot 0: 20 (your value)
    dual_assert(a3.bid(t, history, reserve), 20)
    print "\n\tFinidhed test_bb_reserve.."

def test_bb_overbid():
    # Test that agents don't overbid
    budget = 1000  # don't want binding budget for this test 
    t = 1  # considering the decision for round 1, after the hard-coded round 0
    # Hand-constructed example

    # values [8, 15, 20]
    # clicks [3, 2, 0]
    # reserve = 0

    reserve = 0
     
    bids = [[(3, 16), (2, 14), (1, 4)]]
    occupants = [[3, 2, 1]]
    slot_clicks = [[3, 2, 0]]
    per_click_payments = [[14, 4, 0]]
    slot_payments = [[42, 8, 0]]
     
    history = History(bids, occupants, slot_clicks, per_click_payments, slot_payments)

    a1 = BBAgent(1, 8, budget)
    a2 = BBAgent(2, 15, budget)
    a3 = BBAgent(3, 20, budget)

    # a1's utils for slots: [3 * (8-16), 2*(8-14), 0] = [-24, -12, 0]
    assert a1.expected_utils(t, history, reserve) == [-24, -12, 0]
    assert a1.target_slot(t, history, reserve) == (2, 0, 14)
    # bid for slot 2 = value = 8
    dual_assert (a1.bid(t, history, reserve), 8)
    print "\n\tFinished test_bb_overbid.."

test_bb();
test_bb_reserve();
test_bb_overbid();
