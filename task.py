import argparse
import csv
from typing import List, Dict, Union

from src.ranking import Ranking, get_match_result


def parse_input_row(input_row: List[str]) -> Dict[str, Union[str, int]]:
    """
    Parse csv input row according to required arguments in `ranking.get_match_result`

    Args:
        input_row: csv input row as List of strs

    Returns: Keyword arguments for ranking.get_match_result as dict
    """
    team_a_split = input_row[0].split()
    team_b_split = input_row[1].split()
    return {
        "team_name_a": " ".join(team_a_split[:-1]),
        "score_a": int(team_a_split[-1]),
        "team_name_b": " ".join(team_b_split[:-1]),
        "score_b": int(team_b_split[-1])
    }


def entrypoint() -> None:
    """Main entry point for the hockey ranker CLI.

    Raises:
        FileNotFoundError: If the input_file argument points to a file that does not exist.
        TypeError: If the input_file argument points to a non-file (eg, a directory).
    """
    parser = argparse.ArgumentParser(
        description="CLI to rank teams from a list of game results"
    )
    parser.add_argument("input_file", help="Location of input CSV")
    parser.add_argument("output_file", help="Location to write output CSV")

    # Parse out the input file
    args = parser.parse_args()

    # Here are your two arguments: the input CSV and the output CSV
    input_file = args.input_file
    output_file = args.output_file

    # TODO: Add your code here
    all_rankings = dict()
    with open(input_file) as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            if file_reader.line_num > 1:  # Skip header
                parsed_args = parse_input_row(row)
                team_name_a = parsed_args["team_name_a"]
                team_name_b = parsed_args["team_name_b"]
                if not all_rankings.get(team_name_a):
                    all_rankings[team_name_a] = Ranking(team_name_a)

                if not all_rankings.get(team_name_b):
                    all_rankings[team_name_b] = Ranking(team_name_b)

                match_results = get_match_result(**parsed_args)

                all_rankings[team_name_a].add_score(match_results[team_name_a])
                all_rankings[team_name_b].add_score(match_results[team_name_b])

    with open(output_file, 'w') as file:
        file_writer = csv.writer(file)
        # Write headers
        file_writer.writerow(["Place", "Team", "Score"])

        current_rank = 1
        prev_ranking = None
        for ranking in sorted(list(all_rankings.values()), reverse=True):
            if prev_ranking and prev_ranking.score == ranking.score:
                ranking.rank = prev_ranking.rank
            else:
                ranking.rank = current_rank

            ranking_score_unit = "pts"
            if ranking.score == 1:
                ranking_score_unit = "pt"

            file_writer.writerow([ranking.rank, ranking.team_name, f"{ranking.score} {ranking_score_unit}"])
            prev_ranking = ranking
            current_rank += 1

if __name__ == "__main__":
    entrypoint()
