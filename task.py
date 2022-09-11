import argparse
import csv
from typing import List, Dict
from src.ranking import Ranking, MatchResult, Match


def get_match_from_input_row(input_row: List[str]) -> Match:
    """
    Parse csv input row and map to team name and score attributes
    Provided to reduce coupling between `Match` and csv input format

    Args:
        input_row: csv input row as List of strs

    Returns: None
    """
    team_a_split = input_row[0].split()
    team_b_split = input_row[1].split()

    return Match(
        team_name_a=" ".join(team_a_split[:-1]),
        score_a=int(team_a_split[-1]),
        team_name_b=" ".join(team_b_split[:-1]),
        score_b=int(team_b_split[-1])
    )


def generate_all_rankings(input_file: str) -> Dict[str, Ranking]:
    """
    Given a csv input file,  create dictionary of all rankings for each team in the file
    Args:
        input_file: csv file path

    Returns: Dict of { <team_name>: Ranking object }
    """
    all_rankings = dict()

    def add_to_all_rankings(team_name: str, match_results: Dict[str, MatchResult]):
        if not all_rankings.get(team_name):
            all_rankings[team_name] = Ranking(team_name)

        all_rankings[team_name].add_score(match_results[team_name])

    with open(input_file) as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            if file_reader.line_num > 1:  # Skip header
                match = get_match_from_input_row(row)
                match_results = match.get_match_result()
                for team_name in [match.team_name_a, match.team_name_b]:
                    add_to_all_rankings(team_name, match_results)

    return all_rankings


def write_output(output_file: str, all_rankings: Dict[str, Ranking]) -> None:
    """
    Write all given rankings to given csv output_file using
    Standard Competition ranking ("1224" ranking)
    https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking)

    Args:
        output_file: csv file which may or may not exist
        all_rankings: Dictionary of { <team_name>: Ranking object }

    Returns: None
    """
    def get_header_row() -> List[str]:
        return ["Place", "Team", "Score"]

    def format_ranking_score(ranking_score: int):
        ranking_score_unit = "pts"
        if ranking.score == 1:
            ranking_score_unit = "pt"
        return f"{ranking_score} {ranking_score_unit}"

    with open(output_file, 'w') as file:
        file_writer = csv.writer(file)

        # Write headers
        file_writer.writerow(get_header_row())

        current_rank = 1
        prev_ranking = None
        for ranking in sorted(list(all_rankings.values()), reverse=True):
            if prev_ranking and prev_ranking.score == ranking.score:
                ranking.rank = prev_ranking.rank
            else:
                ranking.rank = current_rank

            file_writer.writerow([ranking.rank, ranking.team_name, format_ranking_score(ranking.score)])
            prev_ranking = ranking
            current_rank += 1


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

    # Generate rankings and write output to file
    all_rankings = generate_all_rankings(input_file)
    write_output(output_file, all_rankings)


if __name__ == "__main__":
    entrypoint()
