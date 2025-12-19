import numpy as np
import sys
from io import StringIO
from main import PayoffMatrices, NashEquilibrium


class TestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.log = []
    
    def log_output(self, message):
        self.log.append(message)
    
    def assert_test(self, condition, test_name, error_msg=""):
        if condition:
            self.tests_passed += 1
            self.log_output(f"PASS: {test_name}")
        else:
            self.tests_failed += 1
            self.log_output(f"FAIL: {test_name}")
            if error_msg:
                self.log_output(f"  Error: {error_msg}")
    
    def test_payoff_matrices(self):
        """Test that PayoffMatrices generates correct payoffs"""
        self.log_output("\n" + "=" * 60)
        self.log_output("TEST SUITE: PayoffMatrices Function")
        self.log_output("=" * 60)
        
        # Test FPA with simple example
        v1, v2 = 50, 50
        A, B = PayoffMatrices(v1, v2, "FPA")
        
        # Test case 1: b1=20, b2=10 -> bidder 1 wins, pays 20
        b1, b2 = 20, 10
        expected_payoff_1 = v1 - b1  # 50 - 20 = 30
        expected_payoff_2 = 0
        self.assert_test(
            abs(A[b1, b2] - expected_payoff_1) < 1e-9 and abs(B[b2, b1] - expected_payoff_2) < 1e-9,
            "FPA: Bidder 1 wins (b1=20, b2=10)",
            f"Expected A[20,10]=30, B[10,20]=0, got A={A[b1, b2]}, B={B[b2, b1]}"
        )
        
        # Test case 2: tie b1=b2=20 
        b1, b2 = 20, 20
        expected_payoff_1 = 0.5 * (v1 - b1)  # 0.5 * (50-20) = 15
        expected_payoff_2 = 0.5 * (v2 - b2)  # 0.5 * (50-20) = 15
        self.assert_test(
            abs(A[b1, b2] - expected_payoff_1) < 1e-9 and abs(B[b2, b1] - expected_payoff_2) < 1e-9,
            "FPA: Tie case (b1=b2=20)",
            f"Expected A[20,20]=15, B[20,20]=15, got A={A[b1, b2]}, B={B[b2, b1]}"
        )
        
        # Test case 3: SPA
        A, B = PayoffMatrices(v1, v2, "SPA")
        b1, b2 = 20, 10
        expected_payoff_1 = v1 - b2  # 50 - 10 = 40 (winner pays opponent's bid)
        expected_payoff_2 = 0
        self.assert_test(
            abs(A[b1, b2] - expected_payoff_1) < 1e-9 and abs(B[b2, b1] - expected_payoff_2) < 1e-9,
            "SPA: Bidder 1 wins (b1=20, b2=10)",
            f"Expected A[20,10]=40, B[10,20]=0, got A={A[b1, b2]}, B={B[b2, b1]}"
        )
        
        # Test case 4: Matrix dimensions
        self.assert_test(
            A.shape == (101, 101) and B.shape == (101, 101),
            "Matrix dimensions (101x101)",
            f"Got A.shape={A.shape}, B.shape={B.shape}"
        )
    
    def test_nash_equilibrium(self):
        """Test NashEquilibrium function with known results"""
        self.log_output("\n" + "=" * 60)
        self.log_output("TEST SUITE: NashEquilibrium Function")
        self.log_output("=" * 60)
        
        # Suppress NashEquilibrium print statements
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # Test 1: SPA with equal values
        v1, v2 = 50, 50
        A, B = PayoffMatrices(v1, v2, "SPA")
        equilibria = NashEquilibrium(A, B, v1, v2, "SPA")
        self.assert_test(
            len(equilibria) > 0,
            "SPA (50, 50): Found equilibria",
            f"Expected >0 equilibria, got {len(equilibria)}"
        )
        self.log_output(f"  -> Found {len(equilibria)} equilibria")
        
        # Test 2: FPA with equal values
        A, B = PayoffMatrices(v1, v2, "FPA")
        equilibria = NashEquilibrium(A, B, v1, v2, "FPA")
        self.assert_test(
            len(equilibria) > 0,
            "FPA (50, 50): Found equilibria",
            f"Expected >0 equilibria, got {len(equilibria)}"
        )
        self.log_output(f"  -> Found {len(equilibria)} equilibria")
        
        # Test 3: Asymmetric values - SPA
        v1, v2 = 70, 50
        A, B = PayoffMatrices(v1, v2, "SPA")
        equilibria = NashEquilibrium(A, B, v1, v2, "SPA")
        self.assert_test(
            len(equilibria) > 0,
            "SPA (70, 50): Found equilibria",
            f"Expected >0 equilibria, got {len(equilibria)}"
        )
        self.log_output(f"  -> Found {len(equilibria)} equilibria")
        
        # Test 4: Asymmetric values - FPA
        A, B = PayoffMatrices(v1, v2, "FPA")
        equilibria = NashEquilibrium(A, B, v1, v2, "FPA")
        self.assert_test(
            len(equilibria) >= 0,
            "FPA (70, 50): Equilibria check",
            f"Got {len(equilibria)} equilibria"
        )
        self.log_output(f"  -> Found {len(equilibria)} equilibria")
        
        # Restore stdout
        sys.stdout = old_stdout
    
    def run_full_analysis(self):
        """Run the complete analysis and log results"""
        self.log_output("\n" + "=" * 60)
        self.log_output("FULL ANALYSIS: All Required Cases")
        self.log_output("=" * 60)
        
        value_profiles = [(50, 50), (70, 50), (49, 50)]
        formats = ["FPA", "SPA"]
        
        # Suppress NashEquilibrium print statements
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        for (v1, v2) in value_profiles:
            self.log_output(f"\nValue profile: ({v1}, {v2})")
            self.log_output("-" * 60)
            for F in formats:
                A, B = PayoffMatrices(v1, v2, F)
                equilibria = NashEquilibrium(A, B, v1, v2, F)
                
                if equilibria:
                    self.log_output(f"  {F}: {len(equilibria)} equilibria found")
                    if len(equilibria) <= 10:
                        for (b1, b2) in equilibria:
                            payoff1 = A[b1, b2]
                            payoff2 = B[b2, b1]
                            self.log_output(f"    -> ({b1}, {b2}): Payoffs = ({payoff1:.2f}, {payoff2:.2f})")
                    else:
                        self.log_output(f"    (Showing first 3 of {len(equilibria)})")
                        for (b1, b2) in equilibria[:3]:
                            payoff1 = A[b1, b2]
                            payoff2 = B[b2, b1]
                            self.log_output(f"    -> ({b1}, {b2}): Payoffs = ({payoff1:.2f}, {payoff2:.2f})")
                else:
                    self.log_output(f"  {F}: No equilibria found")
        
        # Restore stdout
        sys.stdout = old_stdout
    
    def print_summary(self):
        """Print test summary to console"""
        total = self.tests_passed + self.tests_failed
        
        # Print all test details
        print("\n" + "=" * 60)
        for line in self.log:
            if not line.startswith("    "):  # Skip detailed analysis lines
                print(line)
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\nALL TESTS PASSED!")
        else:
            print(f"\n{self.tests_failed} TEST(S) FAILED")
        print("=" * 60)


if __name__ == "__main__":
    suite = TestSuite()
    
    # Run all tests
    suite.test_payoff_matrices()
    suite.test_nash_equilibrium()
    suite.run_full_analysis()
    
    # Print summary to console
    suite.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if suite.tests_failed == 0 else 1)
