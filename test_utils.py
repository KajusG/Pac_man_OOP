import unittest
import math
from unittest.mock import MagicMock, patch

try:
    from pacman_game import canMove, Ghost, originalGameBoard
    pygame_mock = MagicMock()
    with patch.dict('sys.modules', {'pygame': pygame_mock}):
        from pacman_game import Game 
except ImportError as e:
    print(f"Error importing from pacman_game.py: {e}")
    print("Make sure pacman_game.py is in the same directory.")
    def canMove(row, col, game_instance): return True
    class Ghost:
        def calcDistance(self, pos_a, pos_b):
             if pos_a is None or pos_b is None or pos_a == [-1,-1] or pos_b == [-1,-1]: return float('inf')
             dR = pos_a[0] - pos_b[0]; dC = pos_a[1] - pos_b[1]; return math.sqrt(dR*dR + dC*dC)
    class Game: pass
    originalGameBoard = [[1]*5 for _ in range(5)]


class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        """Set up a mock game instance for functions that need it."""
        self.mock_game = MagicMock(spec=Game)
        self.mock_game.board = originalGameBoard 
        self.mock_game.board_rows = len(originalGameBoard)
        self.mock_game.board_cols = len(originalGameBoard[0])
        self.mock_game.pacman = MagicMock()
        self.mock_game.ghosts = []


    def test_canMove_open_space(self):
        """Test canMove for an open space (tile type 1, 2, 4, 5, 6)."""
        self.assertTrue(canMove(4, 1, self.mock_game))
        self.assertTrue(canMove(14, 10, self.mock_game))
        self.assertTrue(canMove(16, 14, self.mock_game))

    def test_canMove_wall(self):
        """Test canMove for a wall (tile type 3)."""
        self.assertFalse(canMove(0, 0, self.mock_game))
        self.assertFalse(canMove(5, 3, self.mock_game))

    def test_canMove_out_of_bounds(self):
        """Test canMove for coordinates outside the board."""
        self.assertFalse(canMove(-1, 5, self.mock_game))
        self.assertFalse(canMove(100, 5, self.mock_game))
        self.assertFalse(canMove(10, -5, self.mock_game))
        self.assertFalse(canMove(10, 100, self.mock_game))

    def test_canMove_tunnel(self):
        """Test canMove for the tunnel area (row 17)."""
        self.assertTrue(canMove(17, -1, self.mock_game))
        self.assertTrue(canMove(17, self.mock_game.board_cols + 1, self.mock_game))
        self.assertTrue(canMove(17, 1, self.mock_game))

    def test_calcDistance_simple(self):
        """Test basic distance calculation."""
        g = Ghost(0,0,"red",0)
        self.assertAlmostEqual(g.calcDistance([0, 0], [3, 4]), 5.0)
        self.assertAlmostEqual(g.calcDistance([1, 1], [1, 1]), 0.0)
        self.assertAlmostEqual(g.calcDistance([-1, 0], [1, 0]), 2.0)

    def test_calcDistance_invalid_input(self):
        """Test distance calculation with invalid inputs."""
        g = Ghost(0,0,"red",0)
        self.assertEqual(g.calcDistance([-1, -1], [3, 4]), float('inf'))
        self.assertEqual(g.calcDistance([0, 0], [-1, -1]), float('inf'))
        self.assertEqual(g.calcDistance(None, [3, 4]), float('inf'))
        self.assertEqual(g.calcDistance([0, 0], None), float('inf'))


if __name__ == '__main__':
    with patch.dict('sys.modules', {'pygame': MagicMock()}):
        unittest.main(argv=['first-arg-is-ignored'], exit=False)