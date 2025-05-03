import unittest
from unittest.mock import MagicMock, patch

pygame_mock = MagicMock(name="PygameMock")
pygame_mock.display = MagicMock()
pygame_mock.mixer = MagicMock()
pygame_mock.init = MagicMock()
pygame_mock.mixer.init = MagicMock()
mock_display_info = MagicMock()
mock_display_info.current_w = 800
mock_display_info.current_h = 600
pygame_mock.display.Info.return_value = mock_display_info
pygame_mock.K_UP = 1
pygame_mock.K_DOWN = 2
pygame_mock.K_LEFT = 3
pygame_mock.K_RIGHT = 4
pygame_mock.K_w = 119
pygame_mock.K_s = 115
pygame_mock.K_a = 97
pygame_mock.K_d = 100

pygame_patcher = patch.dict('sys.modules', {'pygame': pygame_mock})
pygame_patcher.start()

IMPORT_SUCCESS = False
PACMAN_DIRS = {}
originalGameBoard = None

try:
    from pacman_game import PACMAN_DIRS, originalGameBoard
    IMPORT_SUCCESS = True
    print("Successfully imported constants from pacman_game.py")
except ImportError as e:
    print(f"Error importing from pacman_game.py: {e}")
    print("Make sure pacman_game.py is in the same directory")
    PACMAN_DIRS = {"UP": -1, "RIGHT": -1, "DOWN": -1, "LEFT": -1}
    originalGameBoard = []
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
    PACMAN_DIRS = {"UP": -1, "RIGHT": -1, "DOWN": -1, "LEFT": -1}
    originalGameBoard = []


@unittest.skipUnless(IMPORT_SUCCESS, "Skipping tests due to failed import from pacman_game.py")
class TestMainConstants(unittest.TestCase):
    """
    A simple test suite to check basic constants and definitions
    imported from the main pacman_game.py file.
    """

    def test_pacman_dirs_up_value(self):
        """Checks if the constant PACMAN_DIRS['UP'] has the expected value (0)."""
        expected_value = 0
        actual_value = PACMAN_DIRS.get("UP", None)
        self.assertEqual(actual_value, expected_value,
                         f"Expected PACMAN_DIRS['UP'] to be {expected_value}, but got {actual_value}")

    def test_pacman_dirs_down_value(self):
        """Checks if the constant PACMAN_DIRS['DOWN'] has the expected value (2)."""
        expected_value = 2
        actual_value = PACMAN_DIRS.get("DOWN", None)
        self.assertEqual(actual_value, expected_value,
                         f"Expected PACMAN_DIRS['DOWN'] to be {expected_value}, but got {actual_value}")

    def test_pacman_dirs_left_value(self):
        """Checks if the constant PACMAN_DIRS['LEFT'] has the expected value (3)."""
        expected_value = 3
        actual_value = PACMAN_DIRS.get("LEFT", None)
        self.assertEqual(actual_value, expected_value,
                         f"Expected PACMAN_DIRS['LEFT'] to be {expected_value}, but got {actual_value}")

    def test_pacman_dirs_right_value(self):
        """Checks if the constant PACMAN_DIRS['RIGHT'] has the expected value (1)."""
        expected_value = 1
        actual_value = PACMAN_DIRS.get("RIGHT", None)
        self.assertEqual(actual_value, expected_value,
                         f"Expected PACMAN_DIRS['RIGHT'] to be {expected_value}, but got {actual_value}")

    def test_original_game_board_type(self):
        """Checks if originalGameBoard exists and is a list."""
        self.assertIsNotNone(originalGameBoard, "originalGameBoard was not imported or defined")
        self.assertIsInstance(originalGameBoard, list,
                              f"Expected originalGameBoard to be a list, but got {type(originalGameBoard)}")
        if isinstance(originalGameBoard, list) and len(originalGameBoard) > 0:
            self.assertIsInstance(originalGameBoard[0], list, "Expected originalGameBoard to be a list of lists")


pygame_patcher.stop()

if __name__ == '__main__':
    if IMPORT_SUCCESS:
        print("\nRunning simple main tests...")
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        print("\nSkipping test execution due to import errors")