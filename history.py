#!/usr/bin/env python

import copy

class History:
    class RoundHistory:
        """
        Allows agents to access the history of a previous round.
        Makes copies so clients can't change history.
        """
        def __init__(self, bids, occupants, clicks,
                     per_click_payments, slot_payments):
            """Takes the info for a _single_ round."""
            self.bids = copy.deepcopy(bids)
            self.occupants = copy.deepcopy(occupants)
            self.clicks = copy.deepcopy(clicks)
            self.per_click_payments = copy.deepcopy(per_click_payments)
            self.slot_payments = copy.deepcopy(slot_payments)

    def __init__(self, bids, occupants, clicks,
                 per_click_payments, slot_payments, n_agents=3):
        self.round = lambda t: History.RoundHistory(
            bids[t], occupants[t],
            clicks[t], per_click_payments[t],
            slot_payments[t])

        self.last_round = lambda : max(bids.keys())
        self.n_agents = n_agents
        self.num_rounds = lambda : max(bids.keys()) + 1
        ## How much the agents spend.
        self.agents_spent = [0 for i in range(n_agents)]

    def set_agent_spent(self, aid, spent):
        self.agents_spent[aid] = spent




