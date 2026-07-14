import unittest

from unlock_driven import UnlockDrivenSelector


class UnlockDrivenSelectorTests(unittest.TestCase):
    def test_prefers_reachable_high_unlock_skill(self):
        selector = UnlockDrivenSelector(["a", "b", "c"])
        selector.add_inferred_unlock("a", "b", confidence=0.9)
        selector.add_inferred_unlock("a", "c", confidence=0.8)
        selector.add_inferred_unlock("b", "c", confidence=0.4)
        selector.record_attempt("a", success=True)
        selector.record_attempt("b", success=False)
        self.assertEqual(selector.select_next().name, "a")

    def test_acquired_skill_leaves_frontier(self):
        selector = UnlockDrivenSelector(["a", "b"])
        selector.add_inferred_unlock("a", "b", confidence=1.0)
        selector.mark_acquired("a")
        self.assertEqual(selector.select_next().name, "b")

    def test_untried_skill_has_smoothed_feasibility(self):
        selector = UnlockDrivenSelector(["a"])
        self.assertEqual(selector.records["a"].feasibility, 0.5)

    def test_rejects_invalid_self_edge(self):
        selector = UnlockDrivenSelector(["a"])
        with self.assertRaises(ValueError):
            selector.add_inferred_unlock("a", "a", confidence=0.5)

    def test_rejects_invalid_confidence(self):
        selector = UnlockDrivenSelector(["a", "b"])
        with self.assertRaises(ValueError):
            selector.add_inferred_unlock("a", "b", confidence=1.1)


if __name__ == "__main__":
    unittest.main()
