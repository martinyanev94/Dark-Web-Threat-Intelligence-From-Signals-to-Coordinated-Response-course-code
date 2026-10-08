import unittest

from src.charter import Actor, Requirement, SystemCharter, validate_requirements


class CharterTests(unittest.TestCase):
    def make_charter(self) -> SystemCharter:
        return SystemCharter(
            system_name="test charter",
            problem="coordinate synthetic reports for human review",
            goals=("support authorized coordination",),
            actors=(Actor.COMMUNITY, Actor.HUB_OPERATOR),
            inputs=("report", "source reference"),
            outputs=("review item",),
            constraints=("purpose limitation",),
            non_goals=("automated guilt determination",),
        )

    def test_valid_charter_has_no_errors(self) -> None:
        errors = validate_requirements(
            (Requirement("R-01", "intake", "accept reports", "reject missing source"),),
            self.make_charter(),
        )
        self.assertEqual(errors, ())

    def test_empty_problem_is_rejected(self) -> None:
        charter = self.make_charter()
        invalid = SystemCharter(
            charter.system_name,
            "",
            charter.goals,
            charter.actors,
            charter.inputs,
            charter.outputs,
            charter.constraints,
            charter.non_goals,
        )
        self.assertIn("problem must not be empty", invalid.validate())

    def test_missing_adjudication_boundary_is_rejected(self) -> None:
        charter = self.make_charter()
        invalid = SystemCharter(
            charter.system_name,
            charter.problem,
            charter.goals,
            charter.actors,
            charter.inputs,
            charter.outputs,
            charter.constraints,
            ("unrestricted sharing",),
        )
        self.assertIn(
            "adjudication must be an explicit non-goal", invalid.validate()
        )

    def test_duplicate_requirement_ids_are_rejected(self) -> None:
        requirements = (
            Requirement("R-01", "intake", "accept reports", "check input"),
            Requirement("R-01", "routing", "route reports", "check output"),
        )
        errors = validate_requirements(requirements, self.make_charter())
        self.assertIn("duplicate requirement id: R-01", errors)


if __name__ == "__main__":
    unittest.main()
