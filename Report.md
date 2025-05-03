# Pac-Man Game Code Analysis Report

## 1. Introduction

### a. What is your application?

**Application Description:**

This application is a clone of the classic arcade game Pac-Man, developed using the Pygame library in Python. The goal of the coursework was to recreate the core gameplay mechanics of Pac-Man, including player movement, pellet collection, ghost AI, scoring, levels, and lives system. The application utilizes sprite-based graphics loaded from external asset files for the game board, characters, UI elements, and sound effects/music to provide an experience reminiscent of the original game.

### b. How to run the program?

**Prerequisites:**

1.  **Python:** Ensure Python 3.x is installed on your system.
2.  **Pygame:** Install the Pygame library. You can typically do this using pip:
    ```bash
    pip install pygame
    ```
3.  **Assets Folder:** The game requires an `Assets` folder containing subfolders (`BoardImages`, `ElementImages`, `TextImages`, `Data`, `Music`) with the necessary image and sound files, structured as referenced in the code (e.g., `Assets/BoardImages/tile000.png`). Place this `Assets` folder in the same directory as the Python script.

**Execution:**

1.  Navigate to the directory containing the `pacman_game.py` script and the `Assets` folder in your terminal or command prompt.
2.  Run the script using Python:
    ```bash
    python pacman_game.py
    ```

### c. How to use the program?

1.  **Launch Screen:** Upon running the script, a launch screen will appear displaying the game title, character introductions, and basic instructions.
2.  **Start Game:** Press the `SPACE` bar to start the game. The initial game music will play, and the game will begin after it finishes.
3.  **Gameplay:**
    * Control Pac-Man using the `W`, `A`, `S`, `D` keys or the Arrow keys (`UP`, `LEFT`, `DOWN`, `RIGHT`).
    * Navigate the maze, eating all the small dots (pellets) and large flashing dots (power pellets).
    * Avoid colliding with the ghosts (Blinky, Pinky, Inky, Clyde).
    * Eating a power pellet makes the ghosts vulnerable (turn blue) for a short period, allowing you to eat them for bonus points.
    * Occasionally, a fruit (berry) will appear near the center; eat it for extra points.
4.  **Scoring:** Points are awarded for eating pellets, power pellets, vulnerable ghosts, and fruit. The current score and high score are displayed at the top.
5.  **Lives:** You start with 3 lives. Losing a life occurs when a non-vulnerable ghost catches Pac-Man. An extra life is awarded at 10,000 points. The game ends when all lives are lost.
6.  **Levels:** Clearing all pellets advances Pac-Man to the next level, which increases difficulty (e.g., ghosts may move faster or scatter less).
7.  **Quit:** Press `Q` or `ESC` at any time (during the launch screen or gameplay) to quit the application. The high score will be saved automatically upon quitting or game over.

## 2. Body/Analysis

This section details how the Python code implements the core functional requirements of the Pac-Man game.

### a. Game Initialization and Structure

* **Pygame Setup:** The program initializes Pygame and its mixer for sound. It dynamically calculates the screen size based on the monitor resolution and the fixed board dimensions to ensure the game scales reasonably well.
    ```python
    # Pygame initialization
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16) # Allocate sound channels

    # Screen size calculation based on monitor and board
    display_info = pygame.display.Info()
    monitor_width = display_info.current_w
    monitor_height = display_info.current_h
    board_rows = len(originalGameBoard)
    board_cols = len(originalGameBoard[0])
    max_sq_w = int((monitor_width * 0.95) / board_cols)
    max_sq_h = int((monitor_height * 0.95) / board_rows)
    square = min(max_sq_w, max_sq_h) # Tile size
    width = board_cols * square
    height = board_rows * square
    screen = pygame.display.set_mode((width, height))
    ```
* **Game Board:** The maze layout is defined by a 2D list (`originalGameBoard`), where different numbers represent walls (3), empty paths (1), pellets (2), power pellets (6 - initially, flips to 5), and the ghost house area (4).
    ```python
    originalGameBoard = [
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        # ... (rest of the board definition) ...
        [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
        # ...
    ]
    ```
* **Game Class:** The `Game` class encapsulates the main game state and logic, including the board, score, level, lives, Pac-Man instance, ghost instances, game timers, and state flags (paused, gameOver, etc.).
    ```python
    class Game:
        """ Manages the overall game state, entities, and logic. """
        def __init__(self, level, score):
            # Game state variables
            self.paused = True
            self.highScore = self._getHighScore()
            self.score = score
            self.level = level
            self.lives = 3
            # ...
            self.board = copy.deepcopy(originalGameBoard)
            # Create game objects
            self.ghosts = [ # Ghost instances with initial positions and colors
                Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 12.0, "blue", 1),
                Ghost(16.0, 14.0, "pink", 2), Ghost(17.0, 15.0, "orange", 3)
            ]
            self.pacman = Pacman(26.0, 13.5) # Pacman instance
            # ... other initializations (timers, sounds, caches)
    ```
* **GameObject Base Class:** An abstract base class `GameObject` defines the common interface (`update`, `draw`) for movable entities like Pac-Man and Ghosts.
    ```python
    from abc import ABC, abstractmethod

    class GameObject(ABC):
        """ Abstract Base Class for all movable game entities. """
        def __init__(self, row, col):
            self.row = row
            self.col = col
            self.direction_vectors = [(-1, 0), (0, 1), (1, 0), (0, -1)] # N, E, S, W

        @abstractmethod
        def update(self): pass
        @abstractmethod
        def draw(self): pass
    ```

### b. Game Loop and State Management

* **Main Loop:** The primary game loop resides in the `if __name__ == "__main__":` block. It handles game initialization, the launch screen loop, and the main gameplay loop.
* **Update Cycle:** The `Game.update()` method is called each frame. It manages game states (paused, game over, waiting for music/intermission), updates Pac-Man and ghosts based on timers, checks for collisions, handles pellet eating, and determines if the level or game session should end.
    ```python
    # Simplified structure of Game.update()
    def update(self):
        # Handle game over state
        if self.gameOver:
            if self.gameOverFunc(): return True # End session
            else: return False # Continue animation

        # Handle waiting states (start music, intermission)
        if self.waiting_for_start_music: # ... handle music end ...
        if self.waiting_for_intermission: # ... handle intermission end ...

        # Handle paused state
        if self.paused or not self.started: # ... draw READY! ...
            return False

        # --- Main Gameplay Update ---
        # Increment timers
        self.levelTimer += 1
        # ... other timers ...

        # Check for extra life
        if self.score >= 10000 and not self.extraLifeGiven: # ... give life ...

        # Manage background music
        # ... start/stop siren ...

        # Update game elements
        self.clearBoard() # Clear previous positions
        self._updateGhostStates() # Update ghost chase/scatter modes
        # ... check if ghosts leave house ...
        self.checkSurroundings() # Check collisions

        # Update Pacman and Ghosts based on delays
        if self.ghostUpdateCount >= self.ghostUpdateDelay: # ... update ghosts ...
        if self.pacmanUpdateCount >= self.pacmanUpdateDelay: # ... update pacman ...
            self._handlePacmanTileInteraction() # Check pellet eating

        # Update power pellet flashing
        if self.tictakChangeCount >= self.tictakChangeDelay: self.flipColor()

        # Check for level clear
        if self.collected == self.total: # ... start intermission ...
            return False

        # Render the frame
        self.softRender()
        return False # Continue session
    ```
* **Event Handling:** The main loop also processes Pygame events for quitting (`pygame.QUIT`), starting the game (`pygame.K_SPACE`), pausing/unpausing, and player input (`pygame.KEYDOWN` for WASD/Arrows).
    ```python
    # Inside the main game loop (while game_active and running:)
    for event in pygame.event.get():
         if event.type == pygame.QUIT: # Handle window close
            # ... quit logic ...
         elif event.type == pygame.KEYDOWN:
            # Handle unpausing (any key except Q/ESC)
            if game.paused and not game.waiting_for_intermission and not game.waiting_for_start_music and event.key not in [pygame.K_q, pygame.K_ESCAPE]:
                 game.paused = False
                 # ...
            # Handle Pacman movement input
            if not game.paused and ... and event.key in KEY_TO_DIRECTION_MAP:
                 direction = KEY_TO_DIRECTION_MAP[event.key]
                 game.pacman.newDir = direction
            # Handle quitting
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                 # ... quit logic ...
    ```

### c. Pac-Man Implementation

* **Pacman Class:** Inherits from `GameObject`. Manages Pac-Man's position, current direction (`dir`), desired direction (`newDir`), speed, and animation state (mouth open/closed).
* **Movement Logic:** `Pacman.update()` attempts to move in the `newDir` first. If that move is invalid (e.g., into a wall, requires turning but not aligned), it tries to continue in the current `dir`. The `_try_move()` method checks alignment and wall collisions using `canMove()`.
    ```python
    class Pacman(GameObject):
        # ... __init__ ...

        def update(self):
            global game
            # Try moving in the new direction requested by player
            moved = self._try_move(self.newDir, game)
            # If new direction failed, try continuing in the current direction
            if not moved:
                self._try_move(self.dir, game)
            # Handle tunnel wrapping
            if int(round(self.row)) == 17: # Tunnel row
                 self.col = (self.col + game.board_cols) % game.board_cols

        def _try_move(self, direction, game_instance):
            dr, dc = self.direction_vectors[direction]
            next_row, next_col = self.row + dr * self.pacSpeed, self.col + dc * self.pacSpeed

            # Check alignment for turning
            on_col_int = abs(self.col - round(self.col)) < tolerance
            on_row_int = abs(self.row - round(self.row)) < tolerance
            can_move_horiz = (direction in [PACMAN_DIRS["RIGHT"], PACMAN_DIRS["LEFT"]] and on_row_int)
            can_move_vert = (direction in [PACMAN_DIRS["UP"], PACMAN_DIRS["DOWN"]] and on_col_int)

            # Determine the tile to check for collision
            check_row, check_col = self.row, self.col
            # ... logic to find the next tile based on direction ...

            # Check if the move is valid (alignment and not a wall)
            if (can_move_horiz or can_move_vert) and canMove(check_row, check_col, game_instance):
                # Snap to grid if changing direction
                if direction != self.dir:
                    if can_move_horiz: self.row = round(self.row)
                    if can_move_vert: self.col = round(self.col)
                    # Recalculate next position after snapping
                    next_row, next_col = self.row + dr * self.pacSpeed, self.col + dc * self.pacSpeed

                # Update position
                self.row = next_row
                self.col = next_col
                # Update current direction if moving in the new direction
                if direction == self.newDir:
                    self.dir = self.newDir
                return True # Move successful
            return False # Move failed
    ```
* **Pellet Eating:** Handled in `Game._handlePacmanTileInteraction()` when Pac-Man is near the center of a tile containing a pellet (2) or power pellet (5/6).
    ```python
    def _handlePacmanTileInteraction(self):
        tolerance = 0.1
        # Check if Pacman is close to the center of a tile
        if abs(self.pacman.row - round(self.pacman.row)) < tolerance and \
           abs(self.pacman.col - round(self.pacman.col)) < tolerance:
            pac_row, pac_col = int(round(self.pacman.row)), int(round(self.pacman.col))
            # ... bounds check ...
            tile_type = self.board[pac_row][pac_col]
            if tile_type in self.tile_actions: # Check if it's a pellet/power pellet
                action = self.tile_actions[tile_type]
                # ... play sound ...
                self.board[pac_row][pac_col] = 1 # Clear the pellet
                self.score += action.get("score", 0)
                self.collected += 1
                # ... redraw tile ...
                if action.get("powerup"): # Handle power pellet effect
                    self.ghostScore = 200 # Reset ghost eat score
                    self.ghostsAttacked = True # Flag for game state
                    for ghost in self.ghosts:
                        if not ghost.dead:
                            ghost.setAttacked(True) # Make ghosts vulnerable
    ```

### d. Ghost Implementation

* **Ghost Class:** Inherits from `GameObject`. Manages ghost-specific state: color, current direction, target tile (`target`), speed, state (normal, attacked/vulnerable, dead), timers (attacked, death), and whether it's inside the ghost house (`is_in_box`).
* **AI States (Chase/Scatter):** The `Game` class manages timers (`ghostStates`, `levels`) that dictate whether each ghost should be in "chase" mode (mode 0) or "scatter" mode (mode 1). This is updated in `Game._updateGhostStates()`.
    ```python
    # In Game._updateGhostStates()
    for i, state in enumerate(self.ghostStates):
        state[1] += 1 # Increment timer for current mode
        # Check if duration for current mode is exceeded
        duration = self.levels[i][state[0]]
        if duration > 0 and state[1] >= duration:
            state[1] = 0 # Reset timer
            state[0] = (state[0] + 1) % 2 # Flip mode (0 -> 1, 1 -> 0)
    ```
* **Targeting Logic:** `Ghost._updateTarget()` determines the ghost's target tile based on its current state (dead, attacked, locked in box, chase, scatter) and color-specific AI rules.
    ```python
    def _updateTarget(self):
        # ... handle dead/attacked/in_box states first ...

        # Determine current mode (chase/scatter) from Game state
        ghost_index = [g.color for g in game.ghosts].index(self.color)
        current_mode = game.ghostStates[ghost_index][0]

        if current_mode == 0: # Chase Mode
            self._setChaseTarget()
        else: # Scatter Mode
            self.target = self.scatter_targets.get(self.color, ...) # Go to corner
    ```
* **Chase AI:** `Ghost._setChaseTarget()` implements the unique targeting for each ghost during chase mode:
    * **Blinky (Red):** Targets Pac-Man's current tile directly.
    * **Pinky (Pink):** Targets 4 tiles ahead of Pac-Man (with an offset bug emulation for UP).
    * **Inky (Blue):** Targets based on a vector from Blinky to a point 2 tiles ahead of Pac-Man.
    * **Clyde (Orange):** Targets Pac-Man directly if far away, but switches to its scatter target if too close (within 8 tiles).
    ```python
    def _setChaseTarget(self):
        pac_row, pac_col = game.pacman.row, game.pacman.col
        pac_dir = game.pacman.dir
        pac_dr, pac_dc = self.direction_vectors[pac_dir]

        if self.color == "red":
            self.target = [pac_row, pac_col]
        elif self.color == "pink":
            self.target = [pac_row + pac_dr * 4, pac_col + pac_dc * 4]
            # Original arcade bug emulation for UP direction
            if pac_dir == PACMAN_DIRS["UP"]: self.target[1] -= 4
        elif self.color == "blue":
            self.target = self._calculateInkyTarget() # Complex calculation
        elif self.color == "orange":
            distance_to_pac = self.calcDistance([self.row, self.col], [pac_row, pac_col])
            self.target = [pac_row, pac_col] if distance_to_pac > 8 else self.scatter_targets["orange"]
    ```
* **Movement Logic:** `Ghost.setDir()` determines the best direction to move towards the `target`. It checks valid moves (using `Ghost.isValid`), calculates the distance to the target for each valid direction, and chooses the direction minimizing distance. It avoids reversing direction unless necessary (dead ends). `Ghost.move()` updates the ghost's position based on the chosen direction and speed.
    ```python
    def setDir(self):
        # ... setup moves, check alignment ...
        allowed_dirs_data = []
        best_dist = float('inf')
        reversal_dir = (self.dir + 2) % 4

        for move in moves: # Iterate through UP, RIGHT, DOWN, LEFT
            new_dir_code, d_row, d_col = move
            next_row, next_col = self.row + d_row * self.ghostSpeed, self.col + d_col * self.ghostSpeed

            # Check if the potential move is valid (not into wall, respects ghost house rules)
            if not self.isValid(next_row, next_col): continue

            # Don't allow reversal unless it's the only option or not at an intersection
            is_reversal = (new_dir_code == reversal_dir)
            if is_aligned and is_reversal: continue # Skip reversal at intersections

            # Check if turning is allowed based on grid alignment
            # ... alignment check ...
            if is_turn and not can_turn_now: continue

            # Calculate distance from the potential next tile center to the target
            next_tile_center_row = round(self.row + d_row)
            next_tile_center_col = round(self.col + d_col)
            dist = self.calcDistance(self.target, [next_tile_center_row, next_tile_center_col])

            allowed_dirs_data.append([new_dir_code, dist])
            # ... update best_dist and best_dir ...

        # Choose the direction with the minimum distance
        if allowed_dirs_data:
            allowed_dirs_data.sort(key=lambda x: x[1])
            chosen_dir = allowed_dirs_data[0][0]
        elif reversal_move_valid: # Only reverse if no other option
            chosen_dir = reversal_dir
        # ... update self.dir ...

    def move(self):
        # ... get direction vector ...
        next_row = self.row + dr * self.ghostSpeed
        next_col = self.col + dc * self.ghostSpeed
        if self.isValid(next_row, next_col): # Double check validity before moving
            self.row = next_row
            self.col = next_col
        # Handle tunnel wrapping
        if int(round(self.row)) == 17: self.col = (self.col + game.board_cols) % game.board_cols
    ```
* **Ghost States (Vulnerable/Dead):** `setAttacked()` and `setDead()` methods manage the boolean flags and associated properties (speed changes, timers). Vulnerable ghosts flash when the timer is about to expire. Dead ghosts (eyes only) target the ghost house.

### e. Collision Detection

* **Pacman-Ghost:** `Game.checkSurroundings()` iterates through ghosts and calls `Game.touchingPacman()`. This function checks if the distance between Pac-Man's center and the ghost's center is below a tolerance threshold (0.6 tiles). Based on the ghost's state (attacked/dead), it triggers either Pac-Man's death (`handlePacmanDeath`) or the ghost being eaten (`handleGhostEaten`).
    ```python
    def checkSurroundings(self):
        for ghost in self.ghosts:
            if self.touchingPacman(ghost.row, ghost.col):
                # Determine action based on ghost state
                action = collision_actions.get((ghost.isAttacked(), ghost.isDead()))
                if action: action() # Execute death or ghost eaten logic
        # ... berry collision check ...

    def touchingPacman(self, row, col):
        """ Checks if the given (row, col) is close enough to Pacman's center. """
        tolerance = 0.6
        pac_row, pac_col = self.pacman.row, self.pacman.col
        # Simple distance check (Manhattan distance approximation used here)
        return abs(row - pac_row) < tolerance and abs(col - pac_col) < tolerance
    ```
* **Pacman-Wall/Ghost-Wall:** Movement validity checks within `Pacman._try_move()` and `Ghost.isValid()` prevent characters from moving into wall tiles (type 3). `canMove()` is a helper for basic wall checks.

### f. Rendering and Visuals

* **Full Render:** `Game.render()` draws the entire game state, used for the initial screen draw and at the start of a new level. It iterates through the board, drawing walls from cached tile images and pellets/power pellets using Pygame's drawing functions. It then draws ghosts, Pac-Man, and UI elements.
* **Optimized Render:** `Game.softRender()` is used during gameplay for efficiency. It only redraws areas around moving objects (Pac-Man, ghosts, berry) and updates UI elements (score, lives, berries). It uses `clearBoard()` which redraws tiles in a 5x5 area around each moving entity's previous position, and then draws the entities in their new positions.
    ```python
    def clearBoard(self):
        # Get locations of moving objects
        locations_to_clear = [(g.row, g.col) for g in self.ghosts] + [...]
        tiles_to_redraw = set()
        # Calculate a 5x5 grid around each location
        for r, c in locations_to_clear:
            cr, cc = math.floor(r), math.floor(c)
            for ro in range(-2, 3):
                for co in range(-2, 3):
                    tiles_to_redraw.add((cr + ro, cc + co))
        # Redraw only the necessary tiles
        for r, c in tiles_to_redraw:
            self._redraw_single_tile(r, c)

    def softRender(self):
        # ... handle drawing score popups ...
        # Redraw tiles around previous locations (done by clearBoard before this)
        # Draw entities in new locations
        for ghost in self.ghosts: ghost.draw()
        self.pacman.draw()
        self.drawBerry()
        # Update UI elements
        self.displayScore()
        # ... display lives/berries ...
        pygame.display.update() # Update the screen
    ```
* **Caching:** The game uses dictionaries (`tile_cache`, `text_cache`, `element_cache`) to store loaded and scaled images (board tiles, text characters, sprites) to avoid reloading them every frame, improving performance.
* **Sprites:** Pac-Man and ghost appearances are handled by their respective `draw()` methods, selecting the appropriate sprite image file based on direction and state (e.g., Pac-Man mouth open/closed, ghost color/vulnerable/eyes).

### g. Sound and Music

* **Mixer Setup:** Pygame's mixer is initialized with multiple channels.
* **Sound Effects:** Short sounds (like munching) are loaded into `Game.sounds` as `pygame.mixer.Sound` objects and played on available channels using `Game.playSoundEffect()`.
* **Music:** Longer tracks (siren, intro, death, intermission) are loaded and played using `pygame.mixer.music`. `Game.forcePlayMusic()` stops any current music and plays a new track. A specific method `start_background_music()` handles looping the siren sound during gameplay.

### h. High Score Persistence

* **Loading:** `Game._getHighScore()` reads the high score from `Assets/Data/HighScore.txt` during initialization. It includes error handling for file not found or invalid content, creating the file with 0 if necessary.
* **Saving:** `Game._recordHighScore()` is called at game over or when quitting. It updates the `highScore` attribute if the current `score` is higher and writes the result back to the file.
    ```python
    def _getHighScore(self):
        file_path = os.path.join(DataPath, "HighScore.txt")
        highScore = 0
        try:
            # Ensure directory exists
            os.makedirs(DataPath, exist_ok=True)
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content: highScore = int(content)
        except (FileNotFoundError, ValueError) as e:
            # Handle file not found or bad data -> create/reset file
            # ... error handling ...
            highScore = 0
        # ... other error handling ...
        return highScore

    def _recordHighScore(self):
        file_path = os.path.join(DataPath, "HighScore.txt")
        try:
            # Update internal high score if current score is higher
            self.highScore = max(self.score, self.highScore)
            os.makedirs(DataPath, exist_ok=True)
            with open(file_path, "w") as file:
                file.write(str(self.highScore)) # Write score to file
            print(f"High score {self.highScore} saved.")
        except Exception as e:
            print(f"Error writing high score to file {file_path}: {e}")
    ```

## 3. Results and Summary

### a. Results (including Challenges)

* **Functional Clone:** The program successfully implements the core gameplay loop and features of Pac-Man, including movement, pellet collection, distinct ghost behaviors, power-ups, scoring, and level progression.
* **Asset Dependency:** The game heavily relies on external asset files (images, sounds) being correctly named and placed in the specified `Assets` directory structure. Missing or incorrectly named assets will cause errors or lead to visual/audio inconsistencies (though some basic error handling prints warnings).
* **Ghost AI Complexity:** Implementing the distinct targeting logic for each ghost (especially Inky and Clyde) requires careful translation of the original arcade rules into code, which can be prone to subtle bugs affecting behavior. The pathfinding relies on choosing the shortest distance at intersections, which is characteristic of the original game but not a sophisticated pathfinding algorithm.
* **Collision and Movement Precision:** Using floating-point numbers for position and checking against tolerances (`touchingPacman`, `_try_move` alignment checks) is necessary for smooth movement but requires careful tuning to feel right and avoid getting stuck or passing through walls/ghosts unexpectedly.
* **Performance Optimization:** The use of image caching and a `softRender` function (updating only changed parts of the screen) are crucial optimizations for maintaining a smooth frame rate, especially given the reliance on blitting many small images.

### b. Conclusions

* **Achievement:** This coursework successfully achieved the goal of creating a playable Pac-Man clone in Python using Pygame. It demonstrates understanding of game loop structure, state management, sprite handling, basic AI implementation, collision detection, and asset management.
* **Result:** The result is a functional program (`pacman_game.py`) that, when run with the necessary assets, provides a recognizable Pac-Man gameplay experience. It includes key elements like the four unique ghosts, power pellets, fruit bonuses, levels, and high score tracking.
* **Key Findings:** The implementation highlights the importance of modular design (e.g., `Game`, `Pacman`, `Ghost` classes), the need for careful state management in games, the challenges of replicating specific AI behaviors accurately, and the performance benefits of techniques like caching and dirty rect rendering (approximated by `softRender`).

### c. How it would be possible to extend your application?

* **Improved AI:** Implement more sophisticated pathfinding algorithms (like A*) for ghosts, potentially as an alternative difficulty mode. Add more complex scatter behaviors or reactions to Pac-Man's movements.
* **More Levels/Mazes:** Add functionality to load different maze layouts (`originalGameBoard`) for subsequent levels or allow maze selection.
* **Cutscenes:** Implement the intermission cutscenes from the original arcade game between certain levels.
* **UI Enhancements:** Add a more interactive menu system (e.g., selecting difficulty, viewing controls) instead of just a launch screen. Improve the visual feedback for game events.
* **Refactoring:** Further refactor the code for clarity, potentially separating rendering logic more distinctly from game logic, or using more constants instead of magic numbers for tile types within logic checks.
* **Testing:** Expand the unit tests (`test_*.py` files) to cover more edge cases, ghost AI logic, and game state transitions.

## 4. Optional: Resources, References List

* **Pygame Documentation:** [https://www.pygame.org/docs/](https://www.pygame.org/docs/)
* **Python Documentation:** [https://docs.python.org/3/](https://docs.python.org/3/)