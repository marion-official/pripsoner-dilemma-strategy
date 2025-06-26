import unittest

from es import (
    Banker,
    Tournament,
    AlwaysCooperate,
    AlwaysDefect,
    Scores,
    Moves,
    TitForTat,
    Random,
)


class TestBanker(unittest.TestCase):
    def test_play_round(self):
        banker = Banker(AlwaysCooperate("Player 1"), AlwaysDefect("Player 2"))
        result = banker.play_round()
        self.assertEqual(result.p1_score, Scores.PLAYER1_LOSE)
        self.assertEqual(result.p2_score, Scores.PLAYER2_WIN)

    def test_run_game(self):
        banker = Banker(AlwaysCooperate("Player 1"), AlwaysDefect("Player 2"))
        banker.run_game()
        self.assertEqual(banker.player1.score, 0)
        self.assertEqual(banker.player2.score, 15)


class TestStrategy(unittest.TestCase):

    def test_always_cooperate(self):
        player = AlwaysCooperate("Player 1")
        for _ in range(5):
            self.assertEqual(player.choose([]), Moves.COOPERATE)

    def test_always_defect(self):
        player = AlwaysDefect("Player 1")
        for _ in range(5):
            self.assertEqual(player.choose([]), Moves.DEFECT)

    def test_tit_for_tat(self):
        player = TitForTat("Player 1")
        self.assertEqual(player.choose([]), Moves.COOPERATE)
        self.assertEqual(player.choose([Moves.COOPERATE]), Moves.COOPERATE)
        self.assertEqual(player.choose([Moves.COOPERATE, Moves.DEFECT]), Moves.DEFECT)
        self.assertEqual(
            player.choose([Moves.COOPERATE, Moves.DEFECT, Moves.DEFECT]), Moves.DEFECT
        )

    def test_random(self):
        player = Random("Player 1")
        for _ in range(5):
            self.assertIn(player.choose([]), [Moves.COOPERATE, Moves.DEFECT])


class TestTournament(unittest.TestCase):
    def test_run_tournament(self):
        players = [AlwaysCooperate("Player 1"), AlwaysDefect("Player 2")]
        tournament = Tournament(players)
        tournament.run_tournament()
        self.assertEqual(tournament.results, {"Player 1": 0, "Player 2": 1})


if __name__ == "__main__":
    unittest.main()
