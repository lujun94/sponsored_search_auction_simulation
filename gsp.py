#!/usr/bin/env python

import random

class GSP:
    """
    Implements the generalized second price auction mechanism.
    """
    @staticmethod
    def compute(slot_clicks, reserve, bids):
        """
        Given info about the setting (clicks for each slot, and reserve price),
        and bids (list of (id, bid) tuples), compute the following:
          allocation:  list of the occupant in each slot
              len(allocation) = min(len(bids), len(slot_clicks))
          per_click_payments: list of payments for each slot
              len(per_click_payments) = len(allocation)

        If any bids are below the reserve price, they are ignored.

        Returns a pair of lists (allocation, per_click_payments):
         - allocation is a list of the ids of the bidders in each slot
            (in order)
         - per_click_payments is the corresponding payments.
        """
        valid = lambda (a, bid): bid >= reserve
        valid_bids = filter(valid, bids)

        rev_cmp_bids = lambda (a1, b1), (a2, b2): cmp(b2, b1)
        # shuffle first to make sure we don't have any bias for lower or
        # higher ids
        random.shuffle(valid_bids)
        valid_bids.sort(rev_cmp_bids)

        num_slots = len(slot_clicks)
        allocated_bids = valid_bids[:num_slots]
        if len(allocated_bids) == 0:
            return ([], [])

        (allocation, just_bids) = zip(*allocated_bids)

        # Each pays the bid below them, or the reserve
        per_click_payments = list(just_bids[1:])  # first num_slots - 1 slots
        # figure out whether the last slot payment is set by the reserve or
        # the first non-allocated bidder
        if len(valid_bids) > num_slots:
            last_payment = valid_bids[num_slots][1]
        else:
            last_payment = reserve
        per_click_payments.append(last_payment)
        return (list(allocation), per_click_payments)

    @staticmethod
    def bid_range_for_slot(slot, slot_clicks, reserve, bids):
        """
        Compute the range of bids that would result in the bidder ending up
        in slot, given that the other bidders submit bids of previous round.
        Returns a tuple (min_bid, max_bid).
        If slot == 0, returns None for max_bid, since it's not well defined.
        """
        bid_amounts = [b for (_, b) in bids if b >= reserve]
        bid_amounts.sort()
        bid_amounts.reverse()

        n = len(bid_amounts)
        if slot >= n:
            # More than reserve, less than smallest bid
            if n > 0:
                max_bid = bid_amounts[-1]
            else:
                max_bid = reserve if slot > 0 else None
            return (reserve, max_bid)

        min_bid = bid_amounts[slot]
        max_bid = bid_amounts[slot-1] if slot > 0 else None
        return (min_bid, max_bid)

