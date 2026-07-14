import unittest

from developmental_leverage import DevelopmentalLeverageSelector


class DevelopmentalLeverageSelectorTests(unittest.TestCase):
    def test_prefers_transfer_to_unresolved_competence(self):
        selector = DevelopmentalLeverageSelector(["a", "b", "c"])
        selector.record_attempt("a", True)
        selector.record_attempt("b", True)
        selector.set_competence("c", 0.1)
        selector.set_transfer("a", "c", 0.8)
        selector.set_transfer("b", "c", 0.2)
        self.assertEqual(selector.select_next().name, "a")

    def test_transfer_to_mastered_target_has_little_value(self):
        selector = DevelopmentalLeverageSelector(["a", "b", "c"])
        selector.record_attempt("a", True)
        selector.record_attempt("b", True)
        selector.set_competence("c", 1.0)
        selector.set_transfer("a", "c", 1.0)
        selector.set_transfer("b", "a", 0.5)
        self.assertEqual(selector.select_next().name, "b")

    def test_negative_transfer_is_not_counted_as_positive_leverage(self):
        selector = DevelopmentalLeverageSelector(["a", "b"])
        selector.set_transfer("a", "b", -0.9)
        self.assertEqual(selector.developmental_leverage("a"), 0.0)

    def test_mastered_skill_leaves_frontier(self):
        selector = DevelopmentalLeverageSelector(["a", "b"])
        selector.set_competence("a", 1.0)
        self.assertEqual(selector.select_next().name, "b")

    def test_linear_calibration_is_bounded(self):
        selector = DevelopmentalLeverageSelector(["a", "b"])
        selector.set_transfer("a", "b", 0.8)
        selector.calibrate_transfers(alpha=2.0, beta=0.2)
        self.assertEqual(selector.skills["a"].transfer_to["b"], 1.0)

    def test_rejects_self_transfer(self):
        selector = DevelopmentalLeverageSelector(["a"])
        with self.assertRaises(ValueError):
            selector.set_transfer("a", "a", 0.5)


if __name__ == "__main__":
    unittest.main()
