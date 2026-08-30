from pathlib import Path
import sys
import unittest

PYTHON_DIR = Path(__file__).resolve().parents[1] / "python"
sys.path.insert(0, str(PYTHON_DIR))

from alr_mpp import AssuranceState, ReasonCode, base_receipts, evaluate, mutation_receipts


class ALRKernelTests(unittest.TestCase):
    def test_complete_base_space_is_fail_closed(self) -> None:
        receipts = list(base_receipts())
        self.assertEqual(len(receipts), 729)
        decisions = [evaluate(receipt) for receipt in receipts]
        self.assertEqual(sum(decision.eligible for decision in decisions), 1)
        self.assertTrue(decisions[0].eligible)
        self.assertEqual(decisions[0].reason, ReasonCode.ELIGIBLE)

    def test_unknown_never_activates(self) -> None:
        for receipt in base_receipts():
            if AssuranceState.UNKNOWN in receipt.states():
                self.assertFalse(evaluate(receipt).eligible)

    def test_all_prespecified_mutations_reject(self) -> None:
        mutations = list(mutation_receipts())
        self.assertEqual(len(mutations), 7)
        for name, receipt, expected in mutations:
            with self.subTest(name=name):
                decision = evaluate(receipt)
                self.assertFalse(decision.eligible)
                self.assertEqual(decision.reason, expected)


if __name__ == "__main__":
    unittest.main()
