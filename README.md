# Nash Equilibrium in First-Price and Second-Price Auctions

## How to Run

```bash
python main.py
```

The script will analyze all required cases:
- Value profiles: (50, 50), (70, 50), (49, 50)
- Auction formats: FPA (First-Price Auction), SPA (Second-Price Auction)

Output will show all pure-strategy Nash equilibria for each combination.

## How to Check Results

**Expected behavior:**
1. **FPA with equal values (50, 50)**: Should find equilibria around (48,48), (49,49), (50,50) - bidding at or near value
2. **SPA cases**: Will find many more equilibria (thousands) - this is correct! In second-price auctions, any bid at or above your value can be part of an equilibrium
3. **Asymmetric values**: Higher-value player should win in equilibrium

**Quick validation:**
```bash
python test_auction.py  # Run the test suite
```

Tests verify:
- Payoff calculations match examples from assignment
- Matrix dimensions are correct (101×101)
- Best-response logic works properly

## Interpretation 

### Are the equilibria unique?

**No, the equilibria are not unique in most cases:**

- **FPA (First-Price Auction)**: When both players have equal values (50, 50), we observe multiple equilibria including (48, 48), (49, 49), and (50, 50). This occurs because when values are equal, any symmetric bid profile where both players bid the same amount between 0 and their value can be an equilibrium - neither player can profitably deviate by bidding slightly more or less if it results in a loss or no gain.

- **SPA (Second-Price Auction)**: We observe thousands of equilibria. For example, with values (49, 50), we found over 5,000 equilibria. This is theoretically expected because in second-price auctions, bidding your true value (or higher) is a weakly dominant strategy. Any combination where both players bid at or above their values forms an equilibrium. Because the bid doesn't affect the price (unless it changes who wins), there are infinite ways to "threaten" other bidders by bidding extremely high or low, creating "bad" equilibria where the highest-value person doesn't even win. Another example could be if the item is 100 CHF and a bidder bids 5000 CHF and the another bids 0 CHF. Bidder 1 doesn't want to change (they won for free). Bidder 2 doesn't want to change because to win, they would have to bid over $1,000,000, which is more than the item is worth. In SPA therefore, many more possibilities exist as there is no trade-off compared to FPA.

### Do the equilibria differ between FPA and SPA?

**Yes, significantly:**

1. **Number of equilibria**: 
   - FPA has relatively few equilibria (often just a handful)
   - SPA has many equilibria (thousands in our results)

2. **Bidding behavior**:
   - **FPA**: Players face a trade-off between bidding and their own profit and often bid at or slightly below their values. There's strategic underbidding to maximize profit margin (value minus payment). Bidding exactly at value yields zero profit when winning.
   - **SPA**: Many equilibria include bids at or above true values. Since winners pay the second-highest bid, there's no penalty for overbidding as long as you win. As mentioned before, there are infinite ways to threaten other bidders by bidding extremly high without risking any loss of profit.

3. **Winner determination**:
   - **FPA with asymmetric values**: The higher-value player typically wins by bidding more aggressively
   - **SPA with asymmetric values**: The higher-value player wins in most equilibria, but the equilibrium bid profiles are more varied

### Why do these patterns emerge?

**FPA Strategic Considerations:**
- Players face a trade-off: bidding higher increases win probability but reduces profit margin
- When values differ (e.g., 70 vs 50), the high-value player can afford to bid more aggressively
- Symmetric equilibria emerge when values are equal because both players face identical incentives

**SPA Theoretical Properties (Vickrey Auction):**
- Bidding your true value is a weakly dominant strategy: you can't improve your outcome by lying about your value
- Since the winner pays the second-highest bid, not their own bid, overbidding doesn't hurt (as long as you value the item enough)
- This explains the massive number of equilibria: any bid profile where players bid at least their true values works
- The SPA is "strategy-proof" in this sense - truthful bidding is always safe

**Economic Insight:**
The fundamental difference is that FPA makes bidders internalize the payment (you pay what you bid), leading to more conservative bidding. SPA separates the winning decision from the payment, encouraging more aggressive/truthful bidding. This is why second-price auctions are often preferred in practice - they induce truthful revelation of values.