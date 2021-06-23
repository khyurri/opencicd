import pathlib
from unittest import TestCase
from opencicd import exec_plan


class TestCreateGraph(TestCase):

    def test_create_simple_graph(self):
        spec_file = pathlib.Path("tests/spec_files/simple.yaml")
        graph = exec_plan.create_graph(spec_file)
        expected_steps = ["main", "step_1", "step_2",]
        for step in graph:
            self.assertTrue(step in expected_steps)
            expected_steps.remove(step)

        self.assertEqual(bool(expected_steps), False)
