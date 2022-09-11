from task import entrypoint
from unittest import mock
import os
import csv


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


class TestTask:
    def test_task_should_generate_expected_output_for_standard_file(self):
        """
        Given a standard input file 'tests/test_fixtures/input/league-sample-games.csv'
        When we call the entrypoint function from task.py
        Then we should get the exact output from 'tests/test_fixtures/output/league-results.csv'
        """
        # Setup
        input_file_path = os.path.join(PROJECT_ROOT, "tests/test_fixtures/input/league-sample-games.csv")
        output_file_path = os.path.join(PROJECT_ROOT, "tests/tmp/test.csv")
        expected_output_file_path = os.path.join(PROJECT_ROOT, "tests/test_fixtures/output/league-results.csv")

        with mock.patch(
                "sys.argv", [
                    "main",
                    input_file_path,
                    output_file_path
                ]
        ):
            entrypoint()

        # Test
        with open(output_file_path) as output_file:
            with open(expected_output_file_path) as expected_file:
                output_file_reader = csv.reader(output_file)
                expected_file_reader = csv.reader(expected_file)

                assert list(output_file_reader) == list(expected_file_reader), \
                    "Output should match expected output exactly"

        # Cleanup
        os.remove(output_file_path)

    def test_all_teams_should_have_same_rank_with_same_score(self):
        """
        Given a standard input file 'tests/test_fixtures/input/all-same-rank-input.csv'
        When we call the entrypoint function from task.py
        Then we should get the same ranking for all teams as in 'tests/test_fixtures/output/all-same-rank-output.csv'
        """
        # Setup
        input_file_path = os.path.join(PROJECT_ROOT, "tests/test_fixtures/input/all-same-rank-input.csv")
        output_file_path = os.path.join(PROJECT_ROOT, "tests/tmp/test.csv")
        expected_output_file_path = os.path.join(PROJECT_ROOT, "tests/test_fixtures/output/all-same-rank-output.csv")

        with mock.patch(
                "sys.argv", [
                    "main",
                    input_file_path,
                    output_file_path
                ]
        ):
            entrypoint()

        # Test
        with open(output_file_path) as output_file:
            with open(expected_output_file_path) as expected_file:
                output_file_reader = csv.reader(output_file)
                expected_file_reader = csv.reader(expected_file)

                assert list(output_file_reader) == list(expected_file_reader), \
                    "Output should match expected output exactly"

        # Cleanup
        os.remove(output_file_path)

    def test_large_input_file_should_generate_output_without_error(self):
        """
        Given a large input file 'tests/test_fixtures/input/large-input-file.csv'
        When we call the entrypoint function from task.py
        Then we should get the exact output from 'tests/test_fixtures/output/large-input-output.csv'
        """
        # Setup
        input_file_path = os.path.join(PROJECT_ROOT, "tests/test_fixtures/input/large-input-file.csv")
        output_file_path = os.path.join(PROJECT_ROOT, "tests/tmp/test.csv")
        expected_output_file_path = os.path.join(PROJECT_ROOT, "tests/test_fixtures/output/large-input-output.csv")

        with mock.patch(
                "sys.argv", [
                    "main",
                    input_file_path,
                    output_file_path
                ]
        ):
            entrypoint()

        # Test
        with open(output_file_path) as output_file:
            with open(expected_output_file_path) as expected_file:
                output_file_reader = csv.reader(output_file)
                expected_file_reader = csv.reader(expected_file)

                assert list(output_file_reader) == list(expected_file_reader), \
                    "Output should match expected output exactly"

        # Cleanup
        os.remove(output_file_path)