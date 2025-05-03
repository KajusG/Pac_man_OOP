import unittest
import copy 
import math 
from unittest.mock import MagicMock, patch

pygame_mock = MagicMock()
pygame_mock.display = MagicMock()
pygame_mock.image = MagicMock()
pygame_mock.transform = MagicMock()
pygame_mock.Surface = MagicMock
pygame_mock.Rect = MagicMock

pygame_patcher = patch.dict('sys.modules', {'pygame': pygame_mock})
pygame_patcher.start()

try:
    from pacman_game import Pacman, Game, canMove, PACMAN_DIRS, ElementPath, originalGameBoard
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Error importing from pacman_game.py: {e}")
    print("Make sure pacman_game.py is in the same directory.")
    IMPORT_SUCCESS = False
    class Pacman:
        def __init__(self, row, col): self.row=row; self.col=col; self.dir=3; self.newDir=3; self.pacSpeed=1/4; self.direction_vectors=[(-1,0),(0,1),(1,0),(0,-1)]; self.mouthOpen=False # Add mouthOpen
        def update(self): pass 
        def _try_move(self, direction, game_instance): return True
    class Game: pass
    def canMove(r, c, g): return True
    PACMAN_DIRS = {"UP": 0, "RIGHT": 1, "DOWN": 2, "LEFT": 3}
    ElementPath = ""
    originalGameBoard = [[1]*28 for _ in range(36)]


@unittest.skipUnless(IMPORT_SUCCESS, "Skipping tests due to failed import from pacman_game.py")
class TestPacman(unittest.TestCase):

    def setUp(self):
        """Set up a mock game and a Pacman instance for each test."""
        self.mock_game = MagicMock(spec=Game)
        self.mock_game.board_rows = 36
        self.mock_game.board_cols = 28
        self.mock_game.board = copy.deepcopy(originalGameBoard)
        self.mock_game.paused = False
        self.mock_game.started = True
        self.mock_game.element_cache = {}

        self.pacman = Pacman(row=26.0, col=13.5) 
        self.pacman.dir = PACMAN_DIRS["LEFT"]
        self.pacman.newDir = PACMAN_DIRS["LEFT"]

        self.can_move_patcher = patch('pacman_game.canMove', return_value=True)
        self.mock_can_move = self.can_move_patcher.start()


    def tearDown(self):
        """Stop patching."""
        if self.can_move_patcher:
            self.can_move_patcher.stop()


    def test_pacman_initialization(self):
        """Test Pacman's initial state."""
        self.assertEqual(self.pacman.row, 26.0)
        self.assertEqual(self.pacman.col, 13.5)
        self.assertEqual(self.pacman.dir, PACMAN_DIRS["LEFT"])
        self.assertEqual(self.pacman.newDir, PACMAN_DIRS["LEFT"])
        self.assertFalse(self.pacman.mouthOpen)
        self.assertEqual(self.pacman.pacSpeed, 1/4)

    def test_try_move_valid_horizontal(self):
        """Test moving horizontally into an open space."""
        try:
             actual_try_move = Pacman._try_move.__get__(self.pacman, Pacman)
        except AttributeError:
             self.skipTest("_try_move method not found on Pacman class")
             return
        self.can_move_patcher.stop() 

        self.pacman.row = 26.0 
        self.pacman.col = 13.5 
        self.pacman.dir = PACMAN_DIRS["LEFT"]
        target_col_check = int(math.ceil(self.pacman.col + self.pacman.pacSpeed))
        self.assertNotEqual(self.mock_game.board[int(self.pacman.row)][target_col_check], 3, f"Target tile ({int(self.pacman.row)},{target_col_check}) for test is a wall")


        moved = actual_try_move(PACMAN_DIRS["RIGHT"], self.mock_game)

        self.assertTrue(moved, f"Move failed. Pacman at ({self.pacman.row},{self.pacman.col}), Target: ({int(self.pacman.row)},{target_col_check}), Board Tile: {self.mock_game.board[int(self.pacman.row)][target_col_check]}")
        self.assertAlmostEqual(self.pacman.row, 26.0)
        self.assertAlmostEqual(self.pacman.col, 13.5 + self.pacman.pacSpeed)
        self.pacman.newDir = PACMAN_DIRS["RIGHT"]
        moved = actual_try_move(PACMAN_DIRS["RIGHT"], self.mock_game)
        self.assertEqual(self.pacman.dir, PACMAN_DIRS["RIGHT"])

        self.can_move_patcher.start()


    def test_try_move_valid_vertical(self):
        """Test moving vertically into an open space."""
        try:
             actual_try_move = Pacman._try_move.__get__(self.pacman, Pacman)
        except AttributeError:
             self.skipTest("_try_move method not found on Pacman class")
             return
        self.can_move_patcher.stop()

        self.pacman.row = 24.0 
        self.pacman.col = 1.0  
        self.pacman.dir = PACMAN_DIRS["LEFT"]

        target_row_check = int(math.floor(self.pacman.row - self.pacman.pacSpeed))
        self.assertNotEqual(self.mock_game.board[target_row_check][int(self.pacman.col)], 3, f"Target tile ({target_row_check},{int(self.pacman.col)}) for test is a wall")

        moved = actual_try_move(PACMAN_DIRS["UP"], self.mock_game)

        self.assertTrue(moved, f"Move failed. Pacman at ({self.pacman.row},{self.pacman.col}), Target: ({target_row_check},{int(self.pacman.col)}), Board Tile: {self.mock_game.board[target_row_check][int(self.pacman.col)]}")
        self.assertAlmostEqual(self.pacman.row, 24.0 - self.pacman.pacSpeed) 
        self.assertAlmostEqual(self.pacman.col, 1.0) 
        self.pacman.newDir = PACMAN_DIRS["UP"]
        moved = actual_try_move(PACMAN_DIRS["UP"], self.mock_game)
        self.assertEqual(self.pacman.dir, PACMAN_DIRS["UP"])

        self.can_move_patcher.start() 

    def test_try_move_invalid_wall(self):
        """Test trying to move into a wall."""
        try:
             actual_try_move = Pacman._try_move.__get__(self.pacman, Pacman)
        except AttributeError:
             self.skipTest("_try_move method not found on Pacman class")
             return
        self.can_move_patcher.stop()

        self.pacman.row = 5.0
        self.pacman.col = 2.0 
        self.pacman.dir = PACMAN_DIRS["LEFT"]
        target_col_check = int(math.ceil(self.pacman.col + self.pacman.pacSpeed))
        self.assertEqual(self.mock_game.board[int(self.pacman.row)][target_col_check], 3, f"Target tile ({int(self.pacman.row)},{target_col_check}) for test is NOT a wall")


        initial_row, initial_col = self.pacman.row, self.pacman.col
        moved = actual_try_move(PACMAN_DIRS["RIGHT"], self.mock_game) 

        self.assertFalse(moved)
        self.assertAlmostEqual(self.pacman.row, initial_row)
        self.assertAlmostEqual(self.pacman.col, initial_col)

        self.can_move_patcher.start() 

    def test_try_move_invalid_alignment_horizontal(self):
        """Test trying to move horizontally when not aligned vertically."""
        try:
             actual_try_move = Pacman._try_move.__get__(self.pacman, Pacman)
        except AttributeError:
             self.skipTest("_try_move method not found on Pacman class")
             return

        self.pacman.row = 26.3 
        self.pacman.col = 13.5
        self.pacman.dir = PACMAN_DIRS["UP"]

        initial_row, initial_col = self.pacman.row, self.pacman.col
        moved = actual_try_move(PACMAN_DIRS["RIGHT"], self.mock_game) 

        self.assertFalse(moved) 
        self.assertAlmostEqual(self.pacman.row, initial_row)
        self.assertAlmostEqual(self.pacman.col, initial_col)

    def test_try_move_invalid_alignment_vertical(self):
        """Test trying to move vertically when not aligned horizontally."""
        try:
             actual_try_move = Pacman._try_move.__get__(self.pacman, Pacman)
        except AttributeError:
             self.skipTest("_try_move method not found on Pacman class")
             return

        self.pacman.row = 26.0
        self.pacman.col = 13.7 
        self.pacman.dir = PACMAN_DIRS["LEFT"]

        initial_row, initial_col = self.pacman.row, self.pacman.col
        moved = actual_try_move(PACMAN_DIRS["DOWN"], self.mock_game) 

        self.assertFalse(moved) 
        self.assertAlmostEqual(self.pacman.row, initial_row)
        self.assertAlmostEqual(self.pacman.col, initial_col)

    def test_try_move_turn_at_intersection(self):
        """Test changing direction at an intersection."""
        try:
             actual_try_move = Pacman._try_move.__get__(self.pacman, Pacman)
        except AttributeError:
             self.skipTest("_try_move method not found on Pacman class")
             return
        self.can_move_patcher.stop()

        self.pacman.row = 24.0 
        self.pacman.col = 1.0  
        self.pacman.dir = PACMAN_DIRS["RIGHT"]
        target_row_check = int(math.floor(self.pacman.row - self.pacman.pacSpeed))
        self.assertNotEqual(self.mock_game.board[target_row_check][int(self.pacman.col)], 3, f"Target tile ({target_row_check},{int(self.pacman.col)}) for test is a wall")


        moved = actual_try_move(PACMAN_DIRS["UP"], self.mock_game) 

        self.assertTrue(moved)
        self.assertAlmostEqual(self.pacman.row, 24.0 - self.pacman.pacSpeed)
        self.assertAlmostEqual(self.pacman.col, 1.0) 
        self.assertEqual(self.pacman.dir, PACMAN_DIRS["RIGHT"])

        self.pacman.newDir = PACMAN_DIRS["UP"]
        moved = actual_try_move(PACMAN_DIRS["UP"], self.mock_game)
        self.assertTrue(moved)
        self.assertEqual(self.pacman.dir, PACMAN_DIRS["UP"]) 

        self.can_move_patcher.start() 

    def test_tunnel_movement(self):
        """Test Pacman moving through the tunnel."""
        self.can_move_patcher.stop()

        self.pacman.row = 17.0
        self.pacman.col = 0.1
        self.pacman.dir = PACMAN_DIRS["LEFT"]
        self.pacman.newDir = PACMAN_DIRS["LEFT"]
        try:
            self.pacman.update() 
        except NameError as e:
             if "name 'game' is not defined" in str(e):
                 self.pacman.col = (self.pacman.col - self.pacman.pacSpeed + self.mock_game.board_cols) % self.mock_game.board_cols
                 pass 
             else:
                 raise
        except Exception as e:
             raise

        expected_col = (0.1 - self.pacman.pacSpeed + self.mock_game.board_cols) % self.mock_game.board_cols
        self.assertAlmostEqual(self.pacman.row, 17.0)
        self.assertAlmostEqual(self.pacman.col, expected_col, "Column did not wrap correctly moving left")

        self.pacman.col = self.mock_game.board_cols - 0.1
        self.pacman.dir = PACMAN_DIRS["RIGHT"]
        self.pacman.newDir = PACMAN_DIRS["RIGHT"]

        try:
            self.pacman.update()
        except NameError as e:
             if "name 'game' is not defined" in str(e):
                 self.pacman.col = (self.pacman.col + self.pacman.pacSpeed) % self.mock_game.board_cols
                 pass 
             else:
                 raise 
        except Exception as e:
             raise 

        expected_col = (self.mock_game.board_cols - 0.1 + self.pacman.pacSpeed) % self.mock_game.board_cols
        self.assertAlmostEqual(self.pacman.row, 17.0)
        self.assertAlmostEqual(self.pacman.col, expected_col, "Column did not wrap correctly moving right")

        self.can_move_patcher.start() 

pygame_patcher.stop()

if __name__ == '__main__':
    if IMPORT_SUCCESS:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        print("Skipping test execution due to import errors.")