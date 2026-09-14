import unittest

from verification_arguments import verification_arguments


class VerificationArgumentsTest(unittest.TestCase):
    def test_merges_patterns_without_applying_them_to_other_tasks(self):
        self.assertEqual(
            [":ui:test", "--tests", "A", "--tests", "B", ":ui:compile", ":other:test", "--tests", "C"],
            verification_arguments([
                [":ui:test", "--tests", "A"],
                [":ui:compile"],
                [":ui:test", "--tests", "B", "--tests", "A"],
                [":other:test", "--tests", "C"],
                [":ui:compile"],
            ]),
        )

    def test_unfiltered_task_preserves_full_coverage_in_either_order(self):
        for commands in (
            [[":ui:test"], [":ui:test", "--tests", "A"]],
            [[":ui:test", "--tests", "A"], [":ui:test"]],
        ):
            with self.subTest(commands=commands):
                self.assertEqual([":ui:test"], verification_arguments(commands))

    def test_rejects_options_that_cannot_be_merged_safely(self):
        for commands in (
            [],
            [[":ui:test", "--tests"]],
            [[":ui:test", "--exclude-task", ":other:test"]],
            [[":ui:test", ":other:test", ":ui:compile"]],
        ):
            with self.subTest(commands=commands):
                with self.assertRaises(ValueError):
                    verification_arguments(commands)


if __name__ == "__main__":
    unittest.main()
