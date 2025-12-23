import numpy as np

# all possible bids from 0 to 100 CHF
BIDS = range(101)

# tiny number for comparing floats (avoids rounding issues)
EPS = 1e-12

def PayoffMatrices(v1, v2, F):
    """
    Builds payoff matrices A and B for the two-bidder auction.
    
    Parameters:
        v1: how much bidder 1 values the item
        v2: how much bidder 2 values the item       
        F:  "FPA" (first-price) or "SPA" (second-price)
    
    Returns:
        A: payoffs for bidder 1, A[i,j] = payoff if bidder 1 bids i and bidder 2 bids j
        B: payoffs for bidder 2, B[i,j] = payoff if bidder 2 bids i and bidder 1 bids j
    
    Rules:
        - highest bid wins
        - tie = 50/50 coin flip
        - loser gets 0
        - FPA: winner pays own bid (utility = value - own bid)
        - SPA: winner pays other's bid (utility = value - opponent bid)
    """

    # create empty 101x101 matrices
    A = np.zeros((101, 101), dtype=float)
    B = np.zeros((101, 101), dtype=float)

    # go through all bid combinations
    for b1 in BIDS:
        for b2 in BIDS:   
            if b1 > b2:
                # bidder 1 wins
                if F == "FPA":
                    A[b1, b2] = v1 - b1  # pays own bid
                    B[b2, b1] = 0.0
                elif F == "SPA":
                    A[b1, b2] = v1 - b2  # pays opponent's bid
                    B[b2, b1] = 0.0
                else:
                    raise ValueError("F must be 'FPA' or 'SPA'")
                    
            elif b2 > b1:
                # bidder 2 wins
                if F == "FPA":
                    A[b1, b2] = 0.0
                    B[b2, b1] = v2 - b2
                elif F == "SPA":
                    A[b1, b2] = 0.0
                    B[b2, b1] = v2 - b1
                else:
                    raise ValueError("F must be 'FPA' or 'SPA'")
                    
            else:
                # tie: each wins with 50% chance
                if F == "FPA":
                    A[b1, b2] = 0.5 * (v1 - b1)
                    B[b2, b1] = 0.5 * (v2 - b2)
                elif F == "SPA":
                    A[b1, b2] = 0.5 * (v1 - b2)
                    B[b2, b1] = 0.5 * (v2 - b1)
                else:
                    raise ValueError("F must be 'FPA' or 'SPA'")

    return A, B


def NashEquilibrium(A, B, v1, v2, F):
    """
    Finds all pure-strategy Nash equilibria.
    
    Nash equilibrium = both players are playing best responses to each other
    (nobody wants to change their bid)
    
    Parameters:
        A, B: payoff matrices
        v1, v2: valuations (just for printing)
        F: auction format (just for printing)
    
    Returns:
        list of (b1, b2) tuples that are Nash equilibria
    """

    # br1[b2] = set of best responses for bidder 1 when opponent bids b2
    br1 = [set() for _ in BIDS]
    # br2[b1] = set of best responses for bidder 2 when opponent bids b1
    br2 = [set() for _ in BIDS]

    # find best responses for bidder 1
    for b2 in BIDS:
        col = A[:, b2]  # column = all payoffs against this opponent bid
        max_payoff = np.max(col)
        # get all bids that give max payoff (might be multiple)
        br1[b2] = set(np.where(np.abs(col - max_payoff) <= EPS)[0].tolist())

    # same thing for bidder 2
    for b1 in BIDS:
        col = B[:, b1]
        max_payoff = np.max(col)
        br2[b1] = set(np.where(np.abs(col - max_payoff) <= EPS)[0].tolist())

    # Nash eq = both are best responding to each other
    equilibria = []
    for b1 in BIDS:
        for b2 in BIDS:
            if (b1 in br1[b2]) and (b2 in br2[b1]):
                equilibria.append((b1, b2))

    # print results
    if equilibria:
        for (b1, b2) in equilibria:
            print(f"When the values are ({v1}, {v2}), the bid profile ({b1}, {b2}) is a Nash equilibrium in the {F}.")
    else:
        print(f"When the value profile is ({v1}, {v2}), no equilibrium exists in {F}.")

    return equilibria


def main():
    """
    Run the analysis for all cases from the assignment.
    """
    value_profiles = [(50, 50), (70, 50), (49, 50)]
    formats = ["FPA", "SPA"]

    for (v1, v2) in value_profiles:
        for F in formats:
            A, B = PayoffMatrices(v1, v2, F)
            NashEquilibrium(A, B, v1, v2, F)

if __name__ == "__main__":
    main()
