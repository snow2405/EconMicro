import numpy as np

BIDS = range(101)
EPS = 1e-12

def PayoffMatrices(v1, v2, F):
    A = np.zeros((101, 101), dtype=float)  # A[b1, b2] create an array of zeros for player 1 payoffs
    B = np.zeros((101, 101), dtype=float)  # B[b2, b1] create an array of zeros for player 2 payoffs

    #Goes through all bid profiles and fills in the payoff matrices
    for b1 in BIDS:
        for b2 in BIDS:
            if b1 > b2: #If bidder 1 wins
                if F == "FPA":
                    A[b1, b2] = v1 - b1
                    B[b2, b1] = 0.0
                elif F == "SPA":
                    A[b1, b2] = v1 - b2
                    B[b2, b1] = 0.0
                else:
                    raise ValueError("F must be 'FPA' or 'SPA'")
            elif b2 > b1: #If bidder 2 wins
                if F == "FPA":
                    A[b1, b2] = 0.0
                    B[b2, b1] = v2 - b2
                elif F == "SPA":
                    A[b1, b2] = 0.0
                    B[b2, b1] = v2 - b1
                else:
                    raise ValueError("F must be 'FPA' or 'SPA'")
            else:  #If there is a tie
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
    br1 = [set() for _ in BIDS]  # br1[b2] = set of best-response b1 (use a set to only keep unique best responses)
    br2 = [set() for _ in BIDS]  # br2[b1] = set of best-response b2 (use a set to only keep unique best responses)

    #Determine best responses for bidder 2
    for b2 in BIDS:
        col = A[:, b2]
        #Determine the maximum value in the column (best response)
        m = np.max(col)
        #Find all indices where the value is within EPS to find all best responses
        br1[b2] = set(np.where(np.abs(col - m) <= EPS)[0].tolist())

    #Determine best responses for bidder 1
    for b1 in BIDS:
        col = B[:, b1]
        m = np.max(col)
        br2[b1] = set(np.where(np.abs(col - m) <= EPS)[0].tolist())

    equilibria = []
    for b1 in BIDS:
        for b2 in BIDS:
            if (b1 in br1[b2]) and (b2 in br2[b1]):
                equilibria.append((b1, b2))

    if equilibria:
        for (b1, b2) in equilibria:
            print(f"When the values are ({v1}, {v2}), the bid profile ({b1}, {b2}) is a Nash equilibrium in the {F}.")
    else:
        print(f"When the value profile is ({v1}, {v2}), no equilibrium exists in {F}.")

    return equilibria


def main():
    value_profiles = [(50, 50), (70, 50), (49, 50)]
    formats = ["FPA", "SPA"]

    for (v1, v2) in value_profiles:
        for F in formats:
            A, B = PayoffMatrices(v1, v2, F)
            NashEquilibrium(A, B, v1, v2, F)


if __name__ == "__main__":
    main()
