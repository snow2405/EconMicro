import numpy as np
from main import PayoffMatrices, NashEquilibrium

def test_payoff_matrices():
    """Test that PayoffMatrices generates correct payoffs"""
    print("=" * 50)
    print("Testing PayoffMatrices function...")
    print("=" * 50)
    
    # Test FPA with simple example
    v1, v2 = 50, 50
    A, B = PayoffMatrices(v1, v2, "FPA")
    
    # Test case: b1=20, b2=10 -> bidder 1 wins, pays 20
    b1, b2 = 20, 10
    expected_payoff_1 = v1 - b1  # 50 - 20 = 30
    expected_payoff_2 = 0
    assert abs(A[b1, b2] - expected_payoff_1) < 1e-9, f"FPA: Expected A[{b1},{b2}]={expected_payoff_1}, got {A[b1, b2]}"
    assert abs(B[b2, b1] - expected_payoff_2) < 1e-9, f"FPA: Expected B[{b2},{b1}]={expected_payoff_2}, got {B[b2, b1]}"
    print(f"✓ FPA case v1=50, v2=50, b1=20, b2=10: A[20,10]={A[b1, b2]} (expected 30)")
    
    # Test case: tie b1=b2=20 
    b1, b2 = 20, 20
    expected_payoff_1 = 0.5 * (v1 - b1)  # 0.5 * (50-20) = 15
    expected_payoff_2 = 0.5 * (v2 - b2)  # 0.5 * (50-20) = 15
    assert abs(A[b1, b2] - expected_payoff_1) < 1e-9, f"FPA tie: Expected A[{b1},{b2}]={expected_payoff_1}, got {A[b1, b2]}"
    assert abs(B[b2, b1] - expected_payoff_2) < 1e-9, f"FPA tie: Expected B[{b2},{b1}]={expected_payoff_2}, got {B[b2, b1]}"
    print(f"✓ FPA tie case b1=b2=20: A[20,20]={A[b1, b2]} (expected 15)")
    
    # Test SPA
    A, B = PayoffMatrices(v1, v2, "SPA")
    b1, b2 = 20, 10
    expected_payoff_1 = v1 - b2  # 50 - 10 = 40 (winner pays opponent's bid)
    expected_payoff_2 = 0
    assert abs(A[b1, b2] - expected_payoff_1) < 1e-9, f"SPA: Expected A[{b1},{b2}]={expected_payoff_1}, got {A[b1, b2]}"
    assert abs(B[b2, b1] - expected_payoff_2) < 1e-9, f"SPA: Expected B[{b2},{b1}]={expected_payoff_2}, got {B[b2, b1]}"
    print(f"✓ SPA case v1=50, v2=50, b1=20, b2=10: A[20,10]={A[b1, b2]} (expected 40)")
    
    print("\n✅ All PayoffMatrices tests passed!\n")


def test_nash_equilibrium():
    """Test NashEquilibrium function with known results"""
    print("=" * 50)
    print("Testing NashEquilibrium function...")
    print("=" * 50)
    
    # Test SPA with equal values - should have equilibrium at (v, v)
    v1, v2 = 50, 50
    A, B = PayoffMatrices(v1, v2, "SPA")
    print(f"\nTest case: SPA with v1={v1}, v2={v2}")
    equilibria = NashEquilibrium(A, B, v1, v2, "SPA")
    print(f"Found {len(equilibria)} equilibrium/equilibria")
    
    # Test FPA with equal values
    A, B = PayoffMatrices(v1, v2, "FPA")
    print(f"\nTest case: FPA with v1={v1}, v2={v2}")
    equilibria = NashEquilibrium(A, B, v1, v2, "FPA")
    print(f"Found {len(equilibria)} equilibrium/equilibria")
    
    # Test with asymmetric values
    v1, v2 = 70, 50
    A, B = PayoffMatrices(v1, v2, "SPA")
    print(f"\nTest case: SPA with v1={v1}, v2={v2}")
    equilibria = NashEquilibrium(A, B, v1, v2, "SPA")
    print(f"Found {len(equilibria)} equilibrium/equilibria")
    
    A, B = PayoffMatrices(v1, v2, "FPA")
    print(f"\nTest case: FPA with v1={v1}, v2={v2}")
    equilibria = NashEquilibrium(A, B, v1, v2, "FPA")
    print(f"Found {len(equilibria)} equilibrium/equilibria")
    
    print("\n✅ NashEquilibrium function tests completed!\n")


def run_full_analysis():
    """Run the complete analysis as specified in the assignment"""
    print("=" * 50)
    print("FULL ANALYSIS - All Required Cases")
    print("=" * 50)
    
    value_profiles = [(50, 50), (70, 50), (49, 50)]
    formats = ["FPA", "SPA"]
    
    for (v1, v2) in value_profiles:
        print(f"\n{'='*50}")
        print(f"Value profile: v1={v1}, v2={v2}")
        print('='*50)
        for F in formats:
            print(f"\n--- {F} ---")
            A, B = PayoffMatrices(v1, v2, F)
            equilibria = NashEquilibrium(A, B, v1, v2, F)
            
            # Additional analysis
            if equilibria:
                print(f"Total equilibria found: {len(equilibria)}")
                if len(equilibria) <= 10:
                    for (b1, b2) in equilibria:
                        payoff1 = A[b1, b2]
                        payoff2 = B[b2, b1]
                        print(f"  -> ({b1}, {b2}): Payoffs = ({payoff1:.2f}, {payoff2:.2f})")
                else:
                    print(f"  (Showing first 5 of {len(equilibria)})")
                    for (b1, b2) in equilibria[:5]:
                        payoff1 = A[b1, b2]
                        payoff2 = B[b2, b1]
                        print(f"  -> ({b1}, {b2}): Payoffs = ({payoff1:.2f}, {payoff2:.2f})")


if __name__ == "__main__":
    # Run tests
    test_payoff_matrices()
    test_nash_equilibrium()
    
    # Run full analysis
    print("\n\n")
    run_full_analysis()
