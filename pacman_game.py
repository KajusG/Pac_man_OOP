import pygame
import math
from random import randrange
import random
import copy
import os
from abc import ABC, abstractmethod 

BoardPath = "Assets/BoardImages/"
ElementPath = "Assets/ElementImages/"
TextPath = "Assets/TextImages/"
DataPath = "Assets/Data/"
MusicPath = "Assets/Music/"

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
print(f"Music Mixer Busy on Init: {pygame.mixer.music.get_busy()}")

originalGameBoard = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3], 
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3], 
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3], 
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3], 
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3], 
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3], 
    [3,6,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,6,3], 
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3], 
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3], 
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3], 
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3], 
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3], 
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3], 
    [1,1,1,1,1,1,2,1,1,1,3,4,4,4,4,4,4,3,1,1,1,2,1,1,1,1,1,1], 
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],  
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3], 
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3], 
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3], 
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3], 
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3], 
    [3,6,2,2,3,3,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,3,3,2,2,6,3], 
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3], 
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3], 
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3], 
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3], 
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3], 
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3], 
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3], 
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3], 
]

display_info = pygame.display.Info()
monitor_width = display_info.current_w
monitor_height = display_info.current_h
print(f"Detected Monitor Size: {monitor_width}x{monitor_height}")
board_rows = len(originalGameBoard) 
board_cols = len(originalGameBoard[0])
max_sq_w = int((monitor_width * 0.95) / board_cols)
max_sq_h = int((monitor_height * 0.95) / board_rows)
square = min(max_sq_w, max_sq_h)
print(f"Calculated Square Size: {square}")
width = board_cols * square
height = board_rows * square
print(f"Final Screen Size: {width}x{height}")
screen = pygame.display.set_mode((width, height))
spriteRatio = 3/2
spriteOffset = square * (1 - spriteRatio) * (1/2)
pygame.display.set_caption("Pac-Man Clone")
pygame.display.flip()

musicPlaying = 0
pelletColor = (222, 161, 133)
ghostsafeArea = [15, 13]
ghostGate = [[14, 13], [14, 14]]
PACMAN_DIRS = {"UP": 0, "RIGHT": 1, "DOWN": 2, "LEFT": 3}
ORIGINAL_PLAYING_KEYS_STRUCTURE = {
    "up":[pygame.K_w, pygame.K_UP], "down":[pygame.K_s, pygame.K_DOWN],
    "right":[pygame.K_d, pygame.K_RIGHT], "left":[pygame.K_a, pygame.K_LEFT]
}
KEY_TO_DIRECTION_MAP = {
    **{key: PACMAN_DIRS["UP"]    for key in ORIGINAL_PLAYING_KEYS_STRUCTURE["up"]},
    **{key: PACMAN_DIRS["DOWN"]  for key in ORIGINAL_PLAYING_KEYS_STRUCTURE["down"]},
    **{key: PACMAN_DIRS["RIGHT"] for key in ORIGINAL_PLAYING_KEYS_STRUCTURE["right"]},
    **{key: PACMAN_DIRS["LEFT"]  for key in ORIGINAL_PLAYING_KEYS_STRUCTURE["left"]},
}

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

class Game:
    """ Manages the overall game state, entities, and logic. """
    def __init__(self, level, score):

        self.paused = True
        self.ghostUpdateDelay = 2
        self.pacmanUpdateDelay = 2
        self.ghostUpdateCount = 0
        self.pacmanUpdateCount = 0
        self.tictakChangeDelay = 10
        self.tictakChangeCount = 0
        self.ghostsAttacked = False
        self.highScore = self._getHighScore()
        self.score = score
        self.level = level
        self.lives = 3
        self.ghost_aggro_radius = 10.0
        self.ghost_aggro_duration = 300
        self.waiting_for_intermission = False
        self.waiting_for_start_music = False


        self.board = copy.deepcopy(originalGameBoard)
        self.board_rows = len(self.board)
        self.board_cols = len(self.board[0])


        self.ghosts = [
            Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 12.0, "blue", 1),
            Ghost(16.0, 14.0, "pink", 2), Ghost(17.0, 15.0, "orange", 3)
        ]
        self.pacman = Pacman(26.0, 13.5)


        self.total = self.getCount() 
        self.ghostScore = 200
        self.levels = [[150, 500], [50, 700], [50, 700], [0, 900]]
        random.shuffle(self.levels)
        self.ghostStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            max_initial_time = self.levels[index][state[0]]
            state[1] = randrange(max_initial_time + 1) if max_initial_time >= 0 else 0
            index += 1
        self.collected = 0
        self.started = False
        self.gameOver = False
        self.gameOverCounter = 0
        self.points = []
        self.pointsTimer = 10
        self.berryState = [200, 400, False]
        self.berryLocation = [20.0, 13.5]
        self.berries = [f"tile0{80+i}.png" for i in range(8)]
        self.berriesCollected = []
        self.levelTimer = 0
        self.berryScore = 100
        self.lockedInTimer = 100
        self.lockedIn = True
        self.extraLifeGiven = False
        self.musicPlaying = 0
        self.sirenPlaying = False


        self.sounds = {}
        try:
            self.sounds["munch"] = pygame.mixer.Sound(os.path.join(MusicPath, "munch_1.wav"))
        except pygame.error as e:
            print(f"Warning: Could not load sound effect - {e}")


        self.tile_actions = {
            2: {"score": 10, "sound": "munch", "powerup": False},
            5: {"score": 50, "sound": "power_pellet.wav", "powerup": True},
            6: {"score": 50, "sound": "power_pellet.wav", "powerup": True}
        }
        self.music_map = {
             "siren_1.wav": 2, "power_pellet.wav": 1, "pacman_extrapac.wav": 1,
             "pacman_death.wav": 1, "death_1.wav": 1, "eat_ghost.wav": 1,
             "eat_fruit.wav": 1, "intermission.wav": 1, "pacman_beginning.wav": 1
        }

        self.tile_cache = {}
        self.text_cache = {}
        self.element_cache = {}


    def update(self):
        """ Main update logic called each frame. Returns True if game session should end. """
        global running 


        if self.gameOver:
            if self.gameOverFunc():
                return True 
            else:
                return False 


        if self.waiting_for_start_music:
            if not pygame.mixer.music.get_busy():
                print("Start music finished.")
                self.waiting_for_start_music = False

                self.paused = False
                self.started = True
                self.start_background_music()
            else:

                self.displayScore(); self.displayLives(); self.displayBerries()
                pygame.display.update()
                return False 


        if self.waiting_for_intermission:
            if not pygame.mixer.music.get_busy():
                print("Intermission finished, starting next level.")
                self.waiting_for_intermission = False
                self.level += 1
                if self.level > 8:
                    print(f"You win! Final Score: {self.score}")
                    self._recordHighScore()
                    return True 
                else:
                    self.newLevel() 
            else:

                self.displayScore(); self.displayLives(); self.displayBerries()
                pygame.display.update()
                return False 


        if self.paused or not self.started:
            self.drawTilesAround(20, 10); self.drawTilesAround(20, 11)
            self.drawTilesAround(20, 12); self.drawTilesAround(20, 13)
            self.drawTilesAround(20, 14)
            self.drawReady()
            self.displayScore(); self.displayLives(); self.displayBerries()
            pygame.display.update()
            return False 


        self.levelTimer += 1
        self.ghostUpdateCount += 1
        self.pacmanUpdateCount += 1
        self.tictakChangeCount += 1
        self.ghostsAttacked = any(ghost.attacked for ghost in self.ghosts if not ghost.dead)


        if self.score >= 10000 and not self.extraLifeGiven:
            self.lives += 1
            self.extraLifeGiven = True
            self.forcePlayMusic("pacman_extrapac.wav")

      
        should_siren_be_playing = self.started and not self.paused and not self.gameOver and not self.ghostsAttacked and not self.waiting_for_intermission and not self.waiting_for_start_music
        if should_siren_be_playing and not pygame.mixer.music.get_busy():
            self.start_background_music()
        elif not should_siren_be_playing and pygame.mixer.music.get_busy() and self.sirenPlaying:

             if self.paused or self.gameOver or self.ghostsAttacked or self.waiting_for_intermission or self.waiting_for_start_music:
                pygame.mixer.music.stop()
                self.sirenPlaying = False


        self.clearBoard()
        self._updateGhostStates()
        if self.lockedIn and self.levelTimer >= self.lockedInTimer:
            self.lockedIn = False
        self.checkSurroundings()

        if self.gameOver:
             self.gameOverFunc() 
             return False 

        if self.paused: return False 


        if self.ghostUpdateCount >= self.ghostUpdateDelay:
            for ghost in self.ghosts: ghost.update()
            self.ghostUpdateCount = 0
        if self.pacmanUpdateCount >= self.pacmanUpdateDelay:
            self.pacmanUpdateCount = 0
            self.pacman.update()
            self._handlePacmanTileInteraction() 


        if self.tictakChangeCount >= self.tictakChangeDelay:
            self.flipColor() 
            self.tictakChangeCount = 0
        self.highScore = max(self.score, self.highScore)


        if self.collected == self.total: 
            print("Level Cleared! Playing intermission...")
            self.forcePlayMusic("intermission.wav") 
            self.waiting_for_intermission = True   
            return False


        self.softRender()
        return False 

    def _updateGhostStates(self):
        """ Updates the chase/scatter state for each ghost based on timers. """
        for i, state in enumerate(self.ghostStates):
            state[1] += 1
            if i < len(self.levels) and state[0] < len(self.levels[i]):
                duration = self.levels[i][state[0]]
                if duration > 0 and state[1] >= duration:
                    state[1] = 0
                    state[0] = (state[0] + 1) % 2
                elif duration <= 0:
                    state[0] = 0
                    state[1] = 0
            else:
                print(f"Warning: Index out of bounds accessing self.levels[{i}][{state[0]}]")

    def _handlePacmanTileInteraction(self):
        """ Handles Pacman eating pellets or powerups when landing on a tile center. """
        tolerance = 0.1
        if abs(self.pacman.row - round(self.pacman.row)) < tolerance and \
           abs(self.pacman.col - round(self.pacman.col)) < tolerance:
            pac_row, pac_col = int(round(self.pacman.row)), int(round(self.pacman.col))
            if 0 <= pac_row < self.board_rows and 0 <= pac_col < self.board_cols: 
                try:
                    tile_type = self.board[pac_row][pac_col] 
                    if tile_type in self.tile_actions:
                        action = self.tile_actions[tile_type]
                        sound_key_or_file = action.get("sound")
                        if sound_key_or_file in self.sounds:
                            self.playSoundEffect(sound_key_or_file)
                        elif sound_key_or_file:
                            self.forcePlayMusic(sound_key_or_file)
                        self.board[pac_row][pac_col] = 1 
                        self.score += action.get("score", 0)
                        self.collected += 1
                        pygame.draw.rect(screen, (0, 0, 0), (pac_col * square, pac_row * square, square, square))
                        if action.get("powerup"):
                            self.ghostScore = 200
                            self.ghostsAttacked = True
                            for ghost in self.ghosts:
                                if not ghost.dead:
                                    ghost.attackedCount = 0
                                    ghost.setAttacked(True)
                except IndexError:
                    print(f"Warning: IndexError accessing self.board[{pac_row}][{pac_col}] in _handlePacmanTileInteraction")


    def render(self):
        """ Full render of the game state (used for initial draw and level start). """
        screen.fill((0, 0, 0))
        self.displayScore()
        self.displayLives()
        self.displayBerries()
        tile_draw_map = {
            2: lambda r, c: pygame.draw.circle(screen, pelletColor, (c * square + square//2, r * square + square//2), square//4),
            5: lambda r, c: pygame.draw.circle(screen, (0, 0, 0), (c * square + square//2, r * square + square//2), square//2),
            6: lambda r, c: pygame.draw.circle(screen, pelletColor, (c * square + square//2, r * square + square//2), square//2)
        }
        for i in range(3, self.board_rows - 2): 
            for j in range(self.board_cols): 
                try:
                    tile_type = self.board[i][j]
                    if tile_type == 3:
                        wall_tile_index = ((i - 3) * self.board_cols) + j 
                        imageName = f"tile{wall_tile_index:03d}.png"
                        try:
                            if imageName not in self.tile_cache:
                                loaded_tile = pygame.image.load(BoardPath + imageName).convert()
                                self.tile_cache[imageName] = pygame.transform.scale(loaded_tile, (square, square))
                            tileImage = self.tile_cache[imageName]
                            screen.blit(tileImage, (j * square, i * square))
                        except pygame.error:
                            pygame.draw.rect(screen, (0, 0, 100), (j * square, i * square, square, square))
                    elif tile_type in tile_draw_map:
                        tile_draw_map[tile_type](i, j)
                except IndexError:
                   print(f"Warning: IndexError accessing self.board[{i}][{j}] in render")
        for ghost in self.ghosts: ghost.draw()
        self.pacman.draw()
        self.drawBerry()
        pygame.display.update()

    def softRender(self):
        """ More efficient render, only updating areas around moving objects and UI elements. """
        pointsToDraw = []
        for i in range(len(self.points) - 1, -1, -1):
            point = self.points[i]
            if point[3] < self.pointsTimer:
                pointsToDraw.append([point[2], point[0], point[1]])
                point[3] += 1
            else:
                self.drawTilesAround(point[0], point[1]) 
                self.points.pop(i)
        for point_data in pointsToDraw:
            self.drawPoints(point_data[0], point_data[1], point_data[2])
        for ghost in self.ghosts: ghost.draw()
        self.pacman.draw()
        self.drawBerry()
        self.displayScore()
        self.displayBerries()
        self.displayLives()
        pygame.display.update()


    def playSoundEffect(self, sound_key):
        """ Plays a pre-loaded sound effect on an available channel. """
        if sound_key in self.sounds:
            try:
                channel = pygame.mixer.find_channel(True)
                if channel:
                    channel.play(self.sounds[sound_key])
            except pygame.error as e:
                print(f"Error playing sound effect {sound_key}: {e}")
        else:
            print(f"Warning: Sound effect key '{sound_key}' not found in self.sounds")

    def forcePlayMusic(self, music_file, loops=0):
        """ Stops current music and plays the new one immediately. """
        global musicPlaying
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join(MusicPath, music_file))
            pygame.mixer.music.play(loops)
            musicPlaying = self.music_map.get(music_file, 1)
            self.sirenPlaying = (music_file == "siren_1.wav")
        except pygame.error as e:
            print(f"Error force playing music {MusicPath + music_file}: {e}")

    def start_background_music(self):
        """Starts the background siren music on loop."""
        global musicPlaying
        try:

            if not self.waiting_for_intermission and not self.waiting_for_start_music:
                if not pygame.mixer.music.get_busy() or not self.sirenPlaying:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(os.path.join(MusicPath, "siren_1.wav"))
                    pygame.mixer.music.play(-1)
                    self.sirenPlaying = True
                    musicPlaying = self.music_map.get("siren_1.wav", 2)
        except pygame.error as e:
            print(f"Error starting background music: {e}")

    def clearBoard(self):
        """ Redraws tiles around moving objects to clear their previous frame image. """
        locations_to_clear = [(g.row, g.col) for g in self.ghosts] + [(self.pacman.row, self.pacman.col)]
        locations_to_clear.append((self.berryLocation[0], self.berryLocation[1]))
        if self.started and self.levelTimer < 5:
            locations_to_clear.extend([(20, c) for c in range(10, 15)])
        tiles_to_redraw = set()
        for r, c in locations_to_clear:
            cr, cc = math.floor(r), math.floor(c)
            for ro in range(-2, 3):
                for co in range(-2, 3):
                    tiles_to_redraw.add((cr + ro, cc + co))
        for r, c in tiles_to_redraw:
            self._redraw_single_tile(r, c) 

    def _redraw_single_tile(self, i, j):
        """ Helper function to redraw a single tile at board coordinates (i, j). """

        if 3 <= i < self.board_rows - 2 and 0 <= j < self.board_cols:
            try:
                tile_type = self.board[i][j]
                pygame.draw.rect(screen, (0, 0, 0), (j * square, i * square, square, square))
                if tile_type == 3:
                    wall_tile_index = ((i - 3) * self.board_cols) + j 
                    imageName = f"tile{wall_tile_index:03d}.png"
                    try:
                        if imageName not in self.tile_cache:
                             loaded_tile = pygame.image.load(BoardPath + imageName).convert()
                             self.tile_cache[imageName] = pygame.transform.scale(loaded_tile, (square, square))
                        tileImage = self.tile_cache[imageName]
                        screen.blit(tileImage, (j * square, i * square))
                    except pygame.error:
                        pygame.draw.rect(screen, (0, 0, 100), (j * square, i * square, square, square))
                elif tile_type == 2:
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//4)
                elif tile_type == 5:
                    pygame.draw.circle(screen, (0,0,0),(j * square + square//2, i * square + square//2), square//2)
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//4)
                elif tile_type == 6:
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)
            except IndexError:
                print(f"Warning: IndexError accessing self.board[{i}][{j}] in _redraw_single_tile")

    def checkSurroundings(self):
        """ Checks for collisions between Pacman and Ghosts/Berries. """
        for ghost in self.ghosts:
            if self.touchingPacman(ghost.row, ghost.col):
                collision_actions = {
                    (False, False): self.handlePacmanDeath,
                    (True, False): lambda g=ghost: self.handleGhostEaten(g),
                }
                action = collision_actions.get((ghost.isAttacked(), ghost.isDead()))
                if action:
                    action()

                    if self.paused: return 

        is_berry_active = self.levelTimer in range(self.berryState[0], self.berryState[1])
        berry_not_collected = not self.berryState[2]
        touching_berry = self.touchingPacman(self.berryLocation[0], self.berryLocation[1])
        if is_berry_active and berry_not_collected and touching_berry:
            self.handleBerryEaten()

    def handlePacmanDeath(self):
        """ Handles the logic when Pacman is caught by a non-vulnerable ghost. """
        global game 
        self.lives -= 1
        self.forcePlayMusic("pacman_death.wav")

        if self.lives == 0:
            print("Game Over - Triggering Sequence")
            self.gameOver = True 

            for g in self.ghosts: self.drawTilesAround(g.row, g.col)
            self.drawTilesAround(self.pacman.row, self.pacman.col)
            self.pacman.draw()
            pygame.display.update()
        else:
            self.started = False
            self.paused = True
            pygame.time.wait(2000) 
            reset_game_state() 


    def handleGhostEaten(self, ghost):
        """ Handles the logic when Pacman eats a vulnerable ghost. """
        ghost_row_display, ghost_col_display = math.floor(ghost.row), math.floor(ghost.col)
        self.points.append([ghost_row_display, ghost_col_display, self.ghostScore, 0])
        self.score += self.ghostScore
        self.ghostScore *= 2
        self.forcePlayMusic("eat_ghost.wav")
        ghost.dead = True
        ghost.attacked = False
        ghost.aggro_timer = 0
        ghost.row, ghost.col = ghost.ghost_house_target
        ghost.is_in_box = True
        ghost.started_death_timer = True
        ghost.deathCount = 0
        self.paused = True
        self.softRender()
        pygame.time.wait(500)
        self.paused = False

    def handleBerryEaten(self):
        """ Handles the logic when Pacman eats a berry. """
        self.berryState[2] = True
        self.score += self.berryScore
        self.points.append([math.floor(self.berryLocation[0]), math.floor(self.berryLocation[1]), self.berryScore, 0])
        berry_index = (self.level - 1) % len(self.berries)
        self.berriesCollected.append(self.berries[berry_index])
        self.forcePlayMusic("eat_fruit.wav")
        self.drawTilesAround(self.berryLocation[0], self.berryLocation[1])

    def displayScore(self):
        """ Draws the current score and high score text/numbers at the top. """
        text_defs = {
            "1up": ["tile033.png", "tile021.png", "tile016.png"],
            "high_score": ["tile007.png", "tile008.png", "tile006.png", "tile007.png", "tile015.png", "tile019.png", "tile002.png", "tile014.png", "tile018.png", "tile004.png"],
            "digits": [f"tile0{32 + i}.png" for i in range(10)]
        }
        pos = {"text_row": 0, "score_row": 1, "1up_col": 5, "hs_col": 11}
        pygame.draw.rect(screen, (0,0,0), (pos["1up_col"]*square, pos["text_row"]*square, 6*square, 2*square))
        pygame.draw.rect(screen, (0,0,0), (pos["hs_col"]*square, pos["text_row"]*square, 12*square, 2*square))
        for i, img in enumerate(text_defs["1up"]):
            self._drawTextImage(img, (pos["1up_col"] + i) * square, pos["text_row"] * square + 4)
        scoreStr = str(self.score) if self.score > 0 else "00"
        score_start_col = pos["1up_col"] + (len(text_defs["1up"]) // 2) - (len(scoreStr) // 2) + 1
        for i, digit in enumerate(scoreStr):
            try:
                self._drawTextImage(text_defs["digits"][int(digit)], (score_start_col + i) * square, pos["score_row"] * square + 4)
            except (ValueError, IndexError):
                print(f"Warning: Invalid digit '{digit}' in score {self.score}")
        for i, img in enumerate(text_defs["high_score"]):
             self._drawTextImage(img, (pos["hs_col"] + i) * square, pos["text_row"] * square + 4)
        highScoreStr = str(self.highScore) if self.highScore > 0 else "00"
        hs_digit_start_col = pos["hs_col"] + (len(text_defs["high_score"]) // 2) - (len(highScoreStr) // 2) + 1
        for i, digit in enumerate(highScoreStr):
            try:
                self._drawTextImage(text_defs["digits"][int(digit)], (hs_digit_start_col + i) * square, pos["score_row"] * square + 4)
            except (ValueError, IndexError):
                print(f"Warning: Invalid digit '{digit}' in high score {self.highScore}")

    def _drawTextImage(self, img_filename, x, y):
        """ Helper function to load, scale, and blit a text image tile using cache. """
        try:
            if img_filename not in self.text_cache:
                loaded_img = pygame.image.load(TextPath + img_filename).convert_alpha()
                self.text_cache[img_filename] = pygame.transform.scale(loaded_img, (square, square))
            tileImage = self.text_cache[img_filename]
            screen.blit(tileImage, (x, y))
        except pygame.error as e:
            print(f"Error loading text image {TextPath + img_filename}: {e}")

    def drawBerry(self):
        """ Draws the active berry on the screen using cache. """
        is_berry_active = self.levelTimer in range(self.berryState[0], self.berryState[1])
        if is_berry_active and not self.berryState[2]:
            berry_index = (self.level - 1) % len(self.berries)
            berry_img_name = self.berries[berry_index]
            try:
                if berry_img_name not in self.element_cache:
                    loaded_img = pygame.image.load(ElementPath + berry_img_name).convert_alpha()
                    self.element_cache[berry_img_name] = pygame.transform.scale(loaded_img, (int(square * spriteRatio), int(square * spriteRatio)))
                berryImage = self.element_cache[berry_img_name]
                screen.blit(berryImage, (self.berryLocation[1] * square + spriteOffset, self.berryLocation[0] * square + spriteOffset))
            except pygame.error as e:
                print(f"Error loading berry image {ElementPath + berry_img_name}: {e}")

    def drawPoints(self, points_value, row, col):
        """ Draws the score value popup using cache. """
        pointStr = str(points_value)
        digit_width = square // 2
        total_width = len(pointStr) * digit_width
        start_x = col * square + (square - total_width) // 2
        start_y = row * square - square // 2
        digit_img_base = 224
        for i, digit in enumerate(pointStr):
            try:
                digit_value = int(digit)
                if 0 <= digit_value <= 9:
                    img_name = f"tile{digit_img_base + digit_value}.png"
                    cache_key = f"{img_name}_points" 
                    if cache_key not in self.text_cache:
                        loaded_img = pygame.image.load(TextPath + img_name).convert_alpha()
                        self.text_cache[cache_key] = pygame.transform.scale(loaded_img, (digit_width, digit_width))
                    tileImage = self.text_cache[cache_key]
                    screen.blit(tileImage, (start_x + (digit_width * i), start_y))
                else:
                    print(f"Warning: Invalid digit '{digit}' in points value {points_value}")
            except (pygame.error, ValueError) as e:
                print(f"Error processing points image {img_name}: {e}")

    def drawReady(self):
        """ Draws the "READY!" text using cache. """

        if self.paused and not self.started and not self.waiting_for_start_music:
            ready_images = ["tile274.png", "tile260.png", "tile256.png", "tile259.png", "tile281.png", "tile283.png"]
            start_col, start_row = 11, 20
            for i, img_name in enumerate(ready_images):
                 self._drawTextImage(img_name, (start_col + i) * square, start_row * square)

    def gameOverFunc(self):
        """ Handles the Pacman death animation sequence and returns True when done. """

        if self.gameOverCounter >= 11: 
            self._recordHighScore() 
            pygame.time.wait(1000) 
            print("Game Over Animation Complete. Returning to menu.")
            return True 


        self.drawTilesAround(self.pacman.row, self.pacman.col)
        try:
            anim_frame_index = 116 + self.gameOverCounter
            img_name = f"tile{anim_frame_index}.png"
            if img_name not in self.element_cache:
                loaded_img = pygame.image.load(ElementPath + img_name).convert_alpha()
                self.element_cache[img_name] = pygame.transform.scale(loaded_img, (int(square * spriteRatio), int(square * spriteRatio)))
            pacmanImage = self.element_cache[img_name]
            screen.blit(pacmanImage, (self.pacman.col * square + spriteOffset, self.pacman.row * square + spriteOffset))
            pygame.display.update()
            pygame.time.wait(100) 
            self.gameOverCounter += 1
        except pygame.error as e:
            print(f"Error loading death animation frame {ElementPath + img_name}: {e}")

            self._recordHighScore()
            self.gameOverCounter = 11

        return False 

    def displayLives(self):
        """ Draws the remaining lives icons using cache. """
        livesRow, startCol = 34, 1
        life_img_name = "tile054.png"
        max_lives_icons = 5
        clear_width = (max_lives_icons * 2) * square
        icon_height = int(square * spriteRatio)
        clear_y = livesRow * square + spriteOffset
        clear_height = icon_height + 2
        clear_x = startCol * square
        pygame.draw.rect(screen, (0,0,0), (clear_x, clear_y, clear_width, clear_height))
        try:
            if life_img_name not in self.element_cache:
                loaded_img = pygame.image.load(ElementPath + life_img_name).convert_alpha()
                self.element_cache[life_img_name] = pygame.transform.scale(loaded_img, (int(square * spriteRatio), int(square * spriteRatio)))
            lifeImage = self.element_cache[life_img_name]
            for i in range(self.lives - 1):
                screen.blit(lifeImage, ((startCol + 2 * i) * square, livesRow * square + spriteOffset))
        except pygame.error as e:
            print(f"Error loading life image {ElementPath + life_img_name}: {e}")

    def displayBerries(self):
        """ Draws the collected berry icons using cache. """
        berriesRow, endCol = 34, 26
        max_berry_icons = len(self.berries)
        icon_width_with_spacing = 2 * square
        clear_width = max_berry_icons * icon_width_with_spacing
        clear_x = (endCol + 1) * square - clear_width
        icon_height = int(square * spriteRatio)
        clear_y = berriesRow * square + spriteOffset
        clear_height = icon_height + 2
        pygame.draw.rect(screen, (0,0,0), (clear_x, clear_y, clear_width, clear_height))
        for i, berry_img_name in enumerate(self.berriesCollected):
            try:
                if berry_img_name not in self.element_cache:
                     loaded_img = pygame.image.load(ElementPath + berry_img_name).convert_alpha()
                     self.element_cache[berry_img_name] = pygame.transform.scale(loaded_img, (int(square * spriteRatio), int(square * spriteRatio)))
                berrieImage = self.element_cache[berry_img_name]
                screen.blit(berrieImage, ((endCol - (2*i)) * square, berriesRow * square + spriteOffset))
            except pygame.error as e:
                print(f"Error loading collected berry image {ElementPath + berry_img_name}: {e}")

    def touchingPacman(self, row, col):
        """ Checks if the given (row, col) is close enough to Pacman's center. """
        tolerance = 0.6
        pac_row, pac_col = self.pacman.row, self.pacman.col
        return abs(row - pac_row) < tolerance and abs(col - pac_col) < tolerance

    def newLevel(self):
        """ Sets up the game state for the start of a new level (NO start music). """
        global game 
        reset_game_state() 
        self.collected = 0
        self.started = False
        self.paused = True
        self.berryState = [200, 400, False]
        self.levelTimer = 0
        self.lockedIn = True
        self.ghostScore = 200
        for level_timers in self.levels:
            level_timers[0] = max(30, level_timers[0] - 75)
            level_timers[1] = max(300, level_timers[1] + 75)
        random.shuffle(self.levels)
        for i, state in enumerate(self.ghostStates):
            state[0] = randrange(2)
            max_initial_time = self.levels[i][state[0]]
            state[1] = randrange(max_initial_time + 1) if max_initial_time >= 0 else 0

        self.board = copy.deepcopy(originalGameBoard)
        self.total = self.getCount() 
        self.render()


    def drawTilesAround(self, row, col):
        """ Redraws a 5x5 area of tiles centered at (row, col). """
        center_row, center_col = math.floor(row), math.floor(col)
        for r_offset in range(-2, 3):
            for c_offset in range(-2, 3):
                self._redraw_single_tile(center_row + r_offset, center_col + c_offset) 

    def flipColor(self):
        """ Flips the color/state of the special flashing power pellets. """

        for i in range(3, self.board_rows - 2):
            for j in range(self.board_cols):
                try:
                    tile_type = self.board[i][j] 
                    new_type = -1
                    draw_func = None
                    if tile_type == 5:
                        new_type = 6
                        draw_func = lambda r=i, c=j: pygame.draw.circle(screen, pelletColor,(c * square + square//2, r * square + square//2), square//2)
                    elif tile_type == 6:
                        new_type = 5
                        draw_func = lambda r=i, c=j: [pygame.draw.circle(screen, (0, 0, 0),(c * square + square//2, r * square + square//2), square//2),
                                                   pygame.draw.circle(screen, pelletColor,(c * square + square//2, r * square + square//2), square//4)]
                    if new_type != -1:
                        self.board[i][j] = new_type 
                        if draw_func: draw_func()
                except IndexError:
                    print(f"Warning: IndexError accessing self.board[{i}][{j}] in flipColor")

    def getCount(self):
        """ Counts the total number of pellets and power pellets. """
        total = 0
        for row in self.board: 
            for tile in row:
                if tile in [2, 5, 6]: total += 1
        return total

    def _getHighScore(self):
        """ Reads the high score from file. """
        file_path = os.path.join(DataPath, "HighScore.txt")
        highScore = 0
        try:
            os.makedirs(DataPath, exist_ok=True)
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content: highScore = int(content)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error reading high score file ({e}), creating/resetting.")
            try:
                with open(file_path, "w") as file: file.write("0")
            except Exception as write_e: print(f"Failed to write initial high score: {write_e}")
            highScore = 0
        except Exception as e:
            print(f"Unexpected error reading high score: {e}")
            highScore = 0
        return highScore

    def _recordHighScore(self):
        """ Writes the current high score to file. """
        file_path = os.path.join(DataPath, "HighScore.txt")
        try:

            self.highScore = max(self.score, self.highScore)
            os.makedirs(DataPath, exist_ok=True)
            with open(file_path, "w") as file:
                file.write(str(self.highScore))
            print(f"High score {self.highScore} saved.")
        except Exception as e:
            print(f"Error writing high score to file {file_path}: {e}")


class Pacman(GameObject):
    """ Pacman player class. """
    def __init__(self, row, col):
        super().__init__(row, col)
        self.mouthOpen = False; self.pacSpeed = 1/4; self.mouthChangeDelay = 5
        self.mouthChangeCount = 0; self.dir = PACMAN_DIRS["LEFT"]; self.newDir = PACMAN_DIRS["LEFT"]
        self.anim_frames = { PACMAN_DIRS["UP"]: ("tile049.png", "tile051.png"), PACMAN_DIRS["RIGHT"]: ("tile052.png", "tile054.png"), PACMAN_DIRS["DOWN"]: ("tile053.png", "tile055.png"), PACMAN_DIRS["LEFT"]: ("tile048.png", "tile050.png") }

    def update(self):
        global game 
        moved = self._try_move(self.newDir, game) 
        if not moved: self._try_move(self.dir, game) 
        if int(round(self.row)) == 17: self.col = (self.col + game.board_cols) % game.board_cols 

    def _try_move(self, direction, game_instance): 
        """ Attempts to move Pacman in the given direction, returns True if successful. """
        dr, dc = self.direction_vectors[direction]; move_speed = self.pacSpeed
        next_row, next_col = self.row + dr * move_speed, self.col + dc * move_speed
        tolerance = 0.1; on_col_int = abs(self.col - round(self.col)) < tolerance; on_row_int = abs(self.row - round(self.row)) < tolerance
        can_move_horiz = (direction in [PACMAN_DIRS["RIGHT"], PACMAN_DIRS["LEFT"]] and on_row_int)
        can_move_vert = (direction in [PACMAN_DIRS["UP"], PACMAN_DIRS["DOWN"]] and on_col_int)
        check_row, check_col = self.row, self.col
        if dr < 0: check_row = math.floor(next_row)
        elif dr > 0: check_row = math.ceil(next_row)
        if dc < 0: check_col = math.floor(next_col)
        elif dc > 0: check_col = math.ceil(next_col)

        if (can_move_horiz or can_move_vert) and canMove(check_row, check_col, game_instance):
            if direction != self.dir:
                if can_move_horiz: self.row = round(self.row)
                if can_move_vert: self.col = round(self.col)
                next_row, next_col = self.row + dr * move_speed, self.col + dc * move_speed
            self.row = next_row; self.col = next_col
            if direction == self.newDir: self.dir = self.newDir
            return True
        return False

    def draw(self):
        global game; img_name = ""
        if game.paused or not game.started: img_name = "tile112.png"
        else:
            self.mouthChangeCount = (self.mouthChangeCount + 1) % self.mouthChangeDelay
            if self.mouthChangeCount == 0: self.mouthOpen = not self.mouthOpen
            img_pair = self.anim_frames.get(self.dir, self.anim_frames[PACMAN_DIRS["RIGHT"]])
            img_name = img_pair[0] if self.mouthOpen else img_pair[1]
        try:
            if img_name not in game.element_cache:
                loaded_img = pygame.image.load(ElementPath + img_name).convert_alpha()
                game.element_cache[img_name] = pygame.transform.scale(loaded_img, (int(square * spriteRatio), int(square * spriteRatio)))
            pacmanImage = game.element_cache[img_name]
            screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset))
        except pygame.error as e:
            print(f"Error loading Pacman image {ElementPath + img_name}: {e}")
            pygame.draw.rect(screen, (255, 255, 0), (self.col * square, self.row * square, square, square))

class Ghost(GameObject):
    """ Ghost enemy class. """
    def __init__(self, row, col, color, changeFeetCount):
        super().__init__(row, col); self.attacked = False; self.color = color; self.dir = PACMAN_DIRS["UP"]; self.dead = False
        self.changeFeetCount = changeFeetCount; self.changeFeetDelay = 5; self.target = [-1, -1]; self.ghostSpeed = 1/4
        self.lastLoc = [-1, -1]; self.attackedTimer = 240; self.attackedCount = 0; self.deathTimer = 120; self.deathCount = 0
        self.is_in_box = True if color != "red" else False; self.started_death_timer = False; self.aggro_timer = 0; self.intersection_random_chance = 0.30
        self.dir_sprite_map = { PACMAN_DIRS["UP"]: 4, PACMAN_DIRS["RIGHT"]: 0, PACMAN_DIRS["DOWN"]: 6, PACMAN_DIRS["LEFT"]: 2 }
        self.color_sprite_base = {"red": 96, "pink": 128, "blue": 136, "orange": 144}
        self.scatter_targets = { "red": [3.0, 26.0], "pink": [3.0, 1.0], "blue": [30.0, 26.0], "orange": [30.0, 1.0] }
        self.flee_targets = [[3.0, 1.0], [3.0, 26.0], [30.0, 1.0], [30.0, 26.0]]
        self.ghost_house_target = [17.0, 13.5]; self.ghost_house_exit = [14.0, 13.5]

    def update(self):
        global game
        if not self.dead:
            current_tile_type = -1; r_int, c_int = int(round(self.row)), int(round(self.col))
            if 0 <= r_int < game.board_rows and 0 <= c_int < game.board_cols:
                try: current_tile_type = game.board[r_int][c_int] 
                except IndexError: current_tile_type = -1
            self.is_in_box = (current_tile_type == 4)
        self._updateTimersAndStates()
        if not (self.dead and self.started_death_timer):
            self._updateTarget(); self.setDir(); self.move()

    def _updateTimersAndStates(self):
        if self.aggro_timer > 0: self.aggro_timer -= 1
        if self.attacked and not self.dead:
            self.ghostSpeed = 1/8; self.attackedCount += 1
            if self.attackedCount >= self.attackedTimer: self.setAttacked(False)
        if self.dead and self.started_death_timer:
            self.deathCount += 1
            if self.deathCount >= self.deathTimer:
                self.setDead(False); self.is_in_box = True; self.started_death_timer = False

    def _updateTarget(self):
        global game; pac_row, pac_col = game.pacman.row, game.pacman.col
        if self.dead: self.target = [-1, -1]; return
        if self.attacked:
            if self.target == [-1,-1] or self.calcDistance([self.row, self.col], self.target) < 1.0: self.target = random.choice(self.flee_targets)
            return
        distance_to_pac = self.calcDistance([self.row, self.col], [pac_row, pac_col])
        if distance_to_pac <= game.ghost_aggro_radius:
            self.target = [pac_row, pac_col]; self.aggro_timer = game.ghost_aggro_duration; return
        if self.aggro_timer > 0: self.target = [pac_row, pac_col]; return
        is_locked = game.lockedIn and self.color != "red"
        if is_locked and self.is_in_box: self.target = self.ghost_house_exit; return
        if self.is_in_box: self.target = self.ghost_house_exit; return
        try:
            ghost_index = [g.color for g in game.ghosts].index(self.color)
            current_mode = game.ghostStates[ghost_index][0] if 0 <= ghost_index < len(game.ghostStates) else 0
        except ValueError: current_mode = 0
        if current_mode == 0: self._setChaseTarget()
        else: self.target = self.scatter_targets.get(self.color, self.scatter_targets["red"])

    def _setChaseTarget(self):
        global game; pac_row, pac_col = game.pacman.row, game.pacman.col; pac_dir = game.pacman.dir; pac_dr, pac_dc = self.direction_vectors[pac_dir]
        if self.color == "red": self.target = [pac_row, pac_col]
        elif self.color == "pink":
            self.target = [pac_row + pac_dr * 4, pac_col + pac_dc * 4]
            if pac_dir == PACMAN_DIRS["UP"]: self.target[1] -= 4
        elif self.color == "blue": self.target = self._calculateInkyTarget()
        elif self.color == "orange":
            distance_to_pac = self.calcDistance([self.row, self.col], [pac_row, pac_col])
            self.target = [pac_row, pac_col] if distance_to_pac > 8 else self.scatter_targets["orange"]
        else: self.target = [pac_row, pac_col]

    def _calculateInkyTarget(self):
        global game; pac_row, pac_col = game.pacman.row, game.pacman.col; pac_dir = game.pacman.dir; pac_dr, pac_dc = self.direction_vectors[pac_dir]
        blinky = next((g for g in game.ghosts if g.color == "red"), None)
        if not blinky: return [pac_row, pac_col]
        blinky_row, blinky_col = blinky.row, blinky.col
        ref_row = pac_row + pac_dr * 2; ref_col = pac_col + pac_dc * 2
        if pac_dir == PACMAN_DIRS["UP"]: ref_col -= 2
        vec_row = ref_row - blinky_row; vec_col = ref_col - blinky_col
        return [blinky_row + vec_row, blinky_col + vec_col]

    def draw(self):
        global game; self.changeFeetCount = (self.changeFeetCount + 1) % self.changeFeetDelay; frame_offset = 1 if self.changeFeetCount < self.changeFeetDelay // 2 else 0
        base_index_offset = self.dir_sprite_map.get(self.dir, 0); current_anim_index = base_index_offset + frame_offset
        img_name = ""; tileNum = 0
        if self.dead:
            dead_sprite_map = { PACMAN_DIRS["RIGHT"]: 152, PACMAN_DIRS["LEFT"]: 154, PACMAN_DIRS["UP"]: 156, PACMAN_DIRS["DOWN"]: 158 }
            tileNum = dead_sprite_map.get(self.dir, 152); img_name = f"tile{tileNum}.png"
        elif self.attacked:
            flash_threshold = self.attackedTimer // 4; is_ending = (self.attackedTimer - self.attackedCount) < flash_threshold
            is_flashing_frame = (self.attackedCount // (self.changeFeetDelay)) % 2 == 0
            base_vulnerable_index = 70 if (is_ending and is_flashing_frame) else 72
            tileNum = base_vulnerable_index + frame_offset; img_name = f"tile0{tileNum}.png"
        else:
            base_color_index = self.color_sprite_base.get(self.color, 96); tileNum = base_color_index + current_anim_index
            img_name = f"tile0{tileNum}.png" if tileNum < 100 and self.color == "red" else f"tile{tileNum}.png"
        try:
            if img_name not in game.element_cache:
                loaded_img = pygame.image.load(ElementPath + img_name).convert_alpha()
                game.element_cache[img_name] = pygame.transform.scale(loaded_img, (int(square * spriteRatio), int(square * spriteRatio)))
            ghostImage = game.element_cache[img_name]
            screen.blit(ghostImage, (self.col * square + spriteOffset, self.row * square + spriteOffset))
        except pygame.error as e:
            print(f"Error loading Ghost image {ElementPath + img_name}: {e}")
            colors = {"red": (255,0,0), "pink": (255,184,255), "blue": (0,255,255), "orange": (255,184,82)}
            fallback_color = colors.get(self.color, (255,255,255))
            if self.dead: fallback_color = (100, 100, 255)
            elif self.attacked: fallback_color = (0, 0, 200)
            pygame.draw.rect(screen, fallback_color, (self.col * square, self.row * square, square, square))

    def isValid(self, target_row, target_col):
        global game; current_r, current_c = self.row, self.col; r_int, c_int = int(round(target_row)), int(round(target_col))
        dr = target_row - current_r; dc = target_col - current_c; next_r_int, next_c_int = r_int, c_int
        move_threshold = 0.01
        if abs(dr) > move_threshold: next_r_int = math.ceil(target_row) if dr > 0 else math.floor(target_row)
        if abs(dc) > move_threshold: next_c_int = math.ceil(target_col) if dc > 0 else math.floor(target_col)
        r_int, c_int = next_r_int, next_c_int
        num_cols = game.board_cols 
        if c_int < 0 or c_int >= num_cols: return abs(target_row - 17) < 0.5
        if r_int < 0 or r_int >= game.board_rows: return False
        try: tile_type = game.board[r_int][c_int] 
        except IndexError: return False
        is_moving_up = target_row < current_r; is_gate_wall_below_exit = (r_int == 15 and c_int in [13, 14])
        can_exit_through_gate_wall = not self.dead and is_moving_up and is_gate_wall_below_exit and not game.lockedIn
        if tile_type == 3 and not can_exit_through_gate_wall: return False
        if self.dead: return True
        else:
            current_r_int, current_c_int = int(round(current_r)), int(round(current_c)); is_currently_in_box_tile = False
            if 0 <= current_r_int < game.board_rows and 0 <= current_c_int < game.board_cols:
                try: is_currently_in_box_tile = game.board[current_r_int][current_c_int] == 4 
                except IndexError: pass
            no_up_tiles = [(13, 13), (13, 14)]
            if is_moving_up and (r_int, c_int) in no_up_tiles: return False
            is_moving_down = target_row > current_r
            if tile_type == 4 and is_moving_down: return False
            is_exit_path_tile = (r_int == 14 and c_int in [13, 14])
            if game.lockedIn and self.color != "red" and is_moving_up and is_exit_path_tile: return False
            if tile_type == 4 and is_currently_in_box_tile: return True
            if tile_type == 4 and not is_currently_in_box_tile: return False
            return True

    def setDir(self):
        global game; moves = [[i, dr, dc] for i, (dr, dc) in enumerate(self.direction_vectors)]; best_dist = float('inf'); best_dir = -1
        allowed_dirs_data = []; reversal_dir = (self.dir + 2) % 4; reversal_move_valid = False
        tolerance = 0.1; on_col_int = abs(self.col - round(self.col)) < tolerance; on_row_int = abs(self.row - round(self.row)) < tolerance; is_aligned = on_col_int or on_row_int
        for move in moves:
            new_dir_code, d_row, d_col = move; next_row, next_col = self.row + d_row * self.ghostSpeed, self.col + d_col * self.ghostSpeed
            if not self.isValid(next_row, next_col): continue
            is_reversal = (new_dir_code == reversal_dir)
            if is_reversal:
                reversal_move_valid = True
                if is_aligned: continue
            if not is_reversal:
                is_turn = (new_dir_code != self.dir)
                can_turn_now = (new_dir_code in [PACMAN_DIRS["UP"], PACMAN_DIRS["DOWN"]] and on_col_int) or (new_dir_code in [PACMAN_DIRS["RIGHT"], PACMAN_DIRS["LEFT"]] and on_row_int)
                if is_turn and not can_turn_now: continue
            next_tile_center_row = round(self.row + d_row); next_tile_center_col = round(self.col + d_col)
            dist = self.calcDistance(self.target, [next_tile_center_row, next_tile_center_col])
            if not (is_aligned and is_reversal):
                 allowed_dirs_data.append([new_dir_code, dist])
                 if dist < best_dist: best_dist = dist; best_dir = new_dir_code
        chosen_dir = -1
        if allowed_dirs_data:
            is_intersection = is_aligned and len(allowed_dirs_data) > 1
            if is_intersection and random.random() < self.intersection_random_chance: chosen_dir = random.choice([d[0] for d in allowed_dirs_data])
            else: allowed_dirs_data.sort(key=lambda x: x[1]); chosen_dir = allowed_dirs_data[0][0]
        elif reversal_move_valid: chosen_dir = reversal_dir
        if chosen_dir != -1: self.dir = chosen_dir

    def calcDistance(self, pos_a, pos_b):
        if pos_a is None or pos_b is None or pos_a == [-1,-1] or pos_b == [-1,-1]: return float('inf')
        dR = pos_a[0] - pos_b[0]; dC = pos_a[1] - pos_b[1]; return math.sqrt(dR*dR + dC*dC)

    def move(self):
        self.lastLoc = [self.row, self.col]; dr, dc = self.direction_vectors[self.dir]
        next_row = self.row + dr * self.ghostSpeed; next_col = self.col + dc * self.ghostSpeed
        if self.isValid(next_row, next_col):
            self.row = next_row; self.col = next_col
        if int(round(self.row)) == 17: self.col = (self.col + game.board_cols) % game.board_cols

    def setAttacked(self, isAttacked):
        if isAttacked and not self.dead: self.attacked = True; self.attackedCount = 0; self.ghostSpeed = 1/8; self.aggro_timer = 0
        elif not isAttacked and self.attacked: self.attacked = False; self.ghostSpeed = 1/4
    def isAttacked(self): return self.attacked
    def setDead(self, isDead):
        if isDead and not self.dead: self.dead = True; self.attacked = False; self.started_death_timer = False; self.aggro_timer = 0
        elif not isDead and self.dead: self.dead = False; self.deathCount = 0; self.ghostSpeed = 1/4
    def isDead(self): return self.dead

def canMove(row, col, game_instance): 
    """ Basic check if a tile at given coordinates is passable (not a wall). """
    row_int, col_int = math.floor(row), math.floor(col)
    num_cols = game_instance.board_cols 
    if row_int == 17 and (col_int < 0 or col_int >= num_cols): return True
    if not (0 <= row_int < game_instance.board_rows and 0 <= col_int < num_cols): return False
    try: return game_instance.board[row_int][col_int] != 3 
    except IndexError: return False

def reset_game_state():
    """ Resets Pacman and Ghost positions and states. """
    global game
    if game:
        game.ghosts = [ Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 12.0, "blue", 1), Ghost(16.0, 14.0, "pink", 2), Ghost(17.0, 15.0, "orange", 3) ]
        game.pacman = Pacman(26.0, 13.5); game.pacman.dir = PACMAN_DIRS["LEFT"]; game.pacman.newDir = PACMAN_DIRS["LEFT"]

def displayLaunchScreen(game_instance):
    """ Draws the initial launch/splash screen. """
    screen.fill((0,0,0))
    def draw_text_line(img_list, start_x, start_y, scale=1):
        current_x = start_x
        for img_name in img_list:
            try:
                cache_key = f"{img_name}_{scale}"
                if cache_key not in game_instance.text_cache:
                     loaded_img = pygame.image.load(TextPath + img_name).convert_alpha()
                     game_instance.text_cache[cache_key] = pygame.transform.scale(loaded_img, (int(square * scale), int(square * scale)))
                img = game_instance.text_cache[cache_key]
                screen.blit(img, (current_x, start_y))
                current_x += square * scale
            except pygame.error as e: print(f"Error loading launch image {img_name}: {e}")
    pacmanTitle = ["tile016.png", "tile000.png", "tile448.png", "tile012.png", "tile000.png", "tile013.png"]
    title_scale = 3; title_width = len(pacmanTitle) * square * title_scale
    draw_text_line(pacmanTitle, (width - title_width) // 2, 2 * square, title_scale)
    characters = [
         ["tile449.png", "tile015.png", "tile107.png", "tile015.png", "tile083.png", "tile071.png", "tile064.png", "tile067.png", "tile078.png", "tile087.png", "tile015.png", "tile015.png", "tile015.png", "tile015.png", "tile108.png", "tile065.png", "tile075.png", "tile072.png", "tile077.png", "tile074.png", "tile089.png", "tile108.png"],
         ["tile450.png", "tile015.png", "tile363.png", "tile015.png", "tile339.png", "tile336.png", "tile324.png", "tile324.png", "tile323.png", "tile345.png", "tile015.png", "tile015.png", "tile015.png", "tile015.png", "tile364.png", "tile336.png", "tile328.png", "tile333.png", "tile330.png", "tile345.png", "tile364.png"],
         ["tile452.png", "tile015.png", "tile363.png", "tile015.png", "tile193.png", "tile192.png", "tile211.png", "tile199.png", "tile197.png", "tile213.png", "tile203.png", "tile015.png", "tile015.png", "tile015.png", "tile236.png", "tile200.png", "tile205.png", "tile202.png", "tile217.png", "tile236.png"],
         ["tile451.png", "tile015.png", "tile363.png", "tile015.png", "tile272.png", "tile270.png", "tile266.png", "tile260.png", "tile281.png", "tile015.png", "tile015.png", "tile015.png", "tile015.png", "tile015.png", "tile300.png", "tile258.png", "tile267.png", "tile281.png", "tile259.png", "tile260.png", "tile300.png"]
    ]
    char_start_y_base = 12 * square; char_row_height = 2 * square; char_start_x = 2 * square
    for i, char_line in enumerate(characters):
        current_x = char_start_x; current_y = char_start_y_base + i * char_row_height
        for j, img_name in enumerate(char_line):
            try:
                scale = spriteRatio if j == 0 else 1; offset_x = -square//3 if j == 0 else 0; offset_y = -square//3 if j == 0 else 0
                cache_key = f"{img_name}_{scale}"
                if cache_key not in game_instance.text_cache:
                     loaded_img = pygame.image.load(TextPath + img_name).convert_alpha()
                     game_instance.text_cache[cache_key] = pygame.transform.scale(loaded_img, (int(square * scale), int(square * scale)))
                item = game_instance.text_cache[cache_key]
                screen.blit(item, (current_x + offset_x, current_y + offset_y))
                current_x += square * scale
            except pygame.error as e: print(f"Error loading char intro image {img_name}: {e}")
    event = ["tile449.png", "tile015.png", "tile452.png", "tile015.png", "tile015.png", "tile448.png", "tile453.png", "tile015.png", "tile015.png", "tile015.png", "tile453.png"]
    draw_text_line(event, 4 * square, 24 * square, 2)
    wall = ["tile454.png"] * 14
    draw_text_line(wall, 0, 26 * square, 2)
    credit = ["tile015.png"]*4 + ["tile015.png", "tile015.png", "tile015.png", "tile010.png", "tile006.png"]
    draw_text_line(credit, 6 * square, 30 * square)
    instructions = ["tile016.png", "tile018.png", "tile004.png", "tile019.png", "tile019.png", "tile015.png", "tile019.png", "tile016.png", "tile000.png", "tile002.png", "tile004.png", "tile015.png", "tile020.png", "tile014.png", "tile015.png", "tile016.png", "tile011.png", "tile000.png", "tile025.png"]
    draw_text_line(instructions, 4.5 * square, 34 * square)
    pygame.display.update()

if __name__ == "__main__":
    for path in [BoardPath, ElementPath, TextPath, DataPath, MusicPath]:
        if not os.path.exists(path): print(f"Warning: Asset path '{path}' not found.")

    running = True 
    clock = pygame.time.Clock()
    game = None 

    while running: 

        game = Game(1, 0)
        game.tile_cache = {}
        game.text_cache = {}
        game.element_cache = {}
        displayLaunchScreen(game) 

        launch_screen_active = True
        while launch_screen_active and running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False; launch_screen_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        launch_screen_active = False 
                        game.forcePlayMusic("pacman_beginning.wav")
                        game.waiting_for_start_music = True
                        game.paused = True
                        game.started = False
                        game.render()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False; launch_screen_active = False
            clock.tick(60)

        game_active = True 
        while game_active and running: 
            clock.tick(60)
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    running = False; game_active = False
                    if game: game._recordHighScore() 
                 elif event.type == pygame.KEYDOWN:
                    if game.paused and not game.waiting_for_intermission and not game.waiting_for_start_music and event.key not in [pygame.K_q, pygame.K_ESCAPE]:
                         game.paused = False
                         game.started = True
                         game.start_background_music() 
                    if not game.paused and not game.waiting_for_intermission and not game.waiting_for_start_music and event.key in KEY_TO_DIRECTION_MAP:
                         direction = KEY_TO_DIRECTION_MAP[event.key]
                         game.pacman.newDir = direction
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                         running = False; game_active = False
                         if game: game._recordHighScore() 

            if game:
                 session_over = game.update()
                 if session_over:
                     game_active = False 


    pygame.quit()
    print("Game Exited.")