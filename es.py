from collections import namedtuple
from enum import Enum
from random import choice


class Moves(Enum):
    COOPERATE = "C"
    DEFECT = "D"


class Scores(Enum):
    BOTH_COOPERATE = 3
    PLAYER1_WIN = 5
    PLAYER1_LOSE = 0
    PLAYER2_WIN = 5
    PLAYER2_LOSE = 0
    BOTH_DEFECT = 1


class Outcomes(Enum):
    BOTH_COOPERATE = "BC"
    PLAYER1_WIN = "1W"
    PLAYER2_WIN = "2W"
    BOTH_DEFECT = "BD"


RoundResult = namedtuple(
    "RoundResult", ["p1_choice", "p2_choice", "p1_score", "p2_score", "outcome"]
)

PAYOFF = {
    (Moves.COOPERATE, Moves.COOPERATE): RoundResult(
        p1_choice=Moves.COOPERATE,
        p2_choice=Moves.COOPERATE,
        p1_score=Scores.BOTH_COOPERATE,
        p2_score=Scores.BOTH_COOPERATE,
        outcome=Outcomes.BOTH_COOPERATE,
    ),
    (Moves.COOPERATE, Moves.DEFECT): RoundResult(
        p1_choice=Moves.COOPERATE,
        p2_choice=Moves.DEFECT,
        p1_score=Scores.PLAYER1_LOSE,
        p2_score=Scores.PLAYER2_WIN,
        outcome=Outcomes.PLAYER2_WIN,
    ),
    (Moves.DEFECT, Moves.COOPERATE): RoundResult(
        p1_choice=Moves.DEFECT,
        p2_choice=Moves.COOPERATE,
        p1_score=Scores.PLAYER1_WIN,
        p2_score=Scores.PLAYER2_LOSE,
        outcome=Outcomes.PLAYER1_WIN,
    ),
    (Moves.DEFECT, Moves.DEFECT): RoundResult(
        p1_choice=Moves.DEFECT,
        p2_choice=Moves.DEFECT,
        p1_score=Scores.BOTH_DEFECT,
        p2_score=Scores.BOTH_DEFECT,
        outcome=Outcomes.BOTH_DEFECT,
    ),
}


class Player:
    def __init__(self, name):
        self.name = name
        self.history = []
        self.score = 0

    def choose(self, opponent_history):
        raise NotImplementedError("Override in subclass")


class HumanPlayer(Player):
    def choose(self, opponent_history):
        while True:
            response = (
                input(f"{self.name}, cooperate (C) or defect (D)? ").strip().upper()
            )
            if response in [m.value for m in Moves]:
                return Moves(response)


class AlwaysCooperate(Player):
    def choose(self, opponent_history):
        return Moves.COOPERATE


class AlwaysDefect(Player):
    def choose(self, opponent_history):
        return Moves.DEFECT


class TitForTat(Player):
    def choose(self, opponent_history):
        if not opponent_history:
            return Moves.COOPERATE
        return opponent_history[-1]


class Random(Player):
    def choose(self, opponent_history):
        return choice(list(Moves))


class Banker:
    def __init__(self, player1, player2, rounds=3):
        self.player1 = player1
        self.player2 = player2

        self.rounds = rounds

        self.score_history = []

    def play_round(self):
        c1 = self.player1.choose(self.player2.history)
        c2 = self.player2.choose(self.player1.history)

        self.player1.history.append(c1)
        self.player2.history.append(c2)

        result = PAYOFF[(c1, c2)]
        print(
            f"{self.player1.name} chose {c1}, {self.player2.name} chose {c2} => "
            f"{result.p1_score.value}: {result.p2_score.value} ({result.outcome.value})"
        )
        self.player1.score += result.p1_score.value
        self.player2.score += result.p2_score.value
        return result

    def run_game(self):
        for i in range(self.rounds):
            print(f"Playing round: {i + 1}")
            self.score_history.append(self.play_round())

        self.show_result()

    def show_result(self):
        c = 0
        for score in self.score_history:
            print(f" {score.outcome.value} ", end="")
            c += 1
            if c == 30:
                print()
                c = 0
        print()

        print(f"Player1 {self.player1.name} has {self.player1.score} coins")
        print(f"Player2 {self.player2.name} has {self.player2.score} coins")

        if self.player1.score == self.player2.score:
            print("Draw!")
        elif self.player1.score > self.player2.score:
            print(f"Player 1 {self.player1.name} WINS")
        else:
            print(f"Player 2 {self.player2.name} WINS")


class Tournament:
    def __init__(self, players, rounds=3):
        self.players = players
        self.rounds = rounds
        self.results = {}

    def run_tournament(self):
        self.results = {player.name: 0 for player in self.players}

        for i, p1 in enumerate(self.players):
            for j in range(i + 1, len(self.players)):
                p2 = self.players[j]
                print(f"Playing match between {p1.name} and {p2.name}")
                game = Banker(p1, p2, rounds=self.rounds)
                game.run_game()

                if p1.score > p2.score:
                    self.results[p1.name] += 1
                elif p2.score > p1.score:
                    self.results[p2.name] += 1

        print("\nTournament Results:")
        for player_name, score in self.results.items():
            print(f"{player_name}: {score} wins")


if __name__ == "__main__":
    players_in_tournament = [
        AlwaysCooperate("Cooperator"),
        AlwaysDefect("Defector"),
        TitForTat("TitForTat"),
        Random("RandomPlayer"),
    ]
    rounds = 3
    tournament = Tournament(players_in_tournament, rounds=rounds)
    tournament.run_tournament()
