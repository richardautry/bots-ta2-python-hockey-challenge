from enum import Enum
from typing import Dict
from dataclasses import dataclass


class MatchResult(Enum):
    """
    Possible outcome labels for a match
    """
    WIN = 1
    TIE = 2
    LOSS = 3


# Default score map for assigning scores to match results
SCORE_MAP = {
    MatchResult.WIN: 3,
    MatchResult.TIE: 1,
    MatchResult.LOSS: 0
}


@dataclass
class Match:
    team_name_a: str
    score_a: int
    team_name_b: str
    score_b: int

    def get_match_result(self) -> Dict[str, MatchResult]:
        """
        Given two teams and corresponding scores, return the match results
        as dict of { team_name: MatchResult }

        Returns: Results Dict { team_name: MatchResult }

        """
        if self.score_a > self.score_b:  # Team A won
            result = {
                self.team_name_a: MatchResult.WIN,
                self.team_name_b: MatchResult.LOSS
            }
        elif self.score_b > self.score_a:  # Team B won
            result = {
                self.team_name_a: MatchResult.LOSS,
                self.team_name_b: MatchResult.WIN
            }
        else:  # Tie
            result = {
                self.team_name_a: MatchResult.TIE,
                self.team_name_b: MatchResult.TIE
            }
        return result


def get_score(match_result: MatchResult, score_map: Dict[MatchResult, int] = None) -> int:
    """
    Get a score for ranking teams per MatchResult
    Uses default score_map if none given

    Args:
        match_result: MatchResult
        score_map: Dict of { MatchResult: int } to assign scores

    Returns: Assigned score as int
    """
    if not score_map:
        score_map = SCORE_MAP
    return score_map[match_result]


class Ranking:
    """
    A basic data class to track a team's overall score and assign rank
    """
    def __init__(self, team_name: str):
        self.team_name = team_name
        self._score = 0
        self.rank = 1

    @property
    def score(self):
        return self._score

    def add_score(self, match_result: MatchResult) -> None:
        """
        Given a MatchResult, calculate and add score

        Args:
            match_result: MatchResult

        Returns: None

        """
        self._score += get_score(match_result)

    def __str__(self):
        return f"{self.team_name}: {self.score}"

    def __lt__(self, other: "Ranking") -> bool:
        """
        Used to sort by score, then team name

        Args:
            other: Ranking

        Returns: bool
        """
        if self.score == other.score:
            # If same score, should be sorted by team_name DESCENDING
            return self.team_name > other.team_name
        return self.score < other.score  # Sort by score
