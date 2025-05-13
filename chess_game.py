import pygame
import sys
import chess
import chess.engine
import os
from pathlib import Path
import subprocess
import time
import math
import random
import numpy

# Initialize Pygame
pygame.init()

# Get screen info for responsiveness
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Calculate responsive sizes
BOARD_WIDTH = int(SCREEN_WIDTH * 0.6)  # 60% of screen width
BOARD_SIZE = 8
SQUARE_SIZE = BOARD_WIDTH // BOARD_SIZE
SIDE_PANEL_WIDTH = SCREEN_WIDTH - BOARD_WIDTH  # 40% of screen width

# Set up the display with hardware acceleration and double buffering
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Chess Capture Challenge")

# Layout constants
PADDING = 20
ELEMENT_SPACING = 15

# Input box properties
input_box = pygame.Rect(
    BOARD_WIDTH + PADDING,
    PADDING,
    SIDE_PANEL_WIDTH - 2 * PADDING,
    40
)

# Side toggle properties
toggle_width = SIDE_PANEL_WIDTH - 2 * PADDING
toggle_height = 40
side_toggle_rect = pygame.Rect(
    BOARD_WIDTH + PADDING,
    input_box.bottom + ELEMENT_SPACING,
    toggle_width,
    toggle_height
)

# Game info panel
info_panel = pygame.Rect(
    BOARD_WIDTH + PADDING,
    side_toggle_rect.bottom + ELEMENT_SPACING,
    toggle_width,
    SCREEN_HEIGHT - side_toggle_rect.bottom - 2 * PADDING
)

# Font sizes (improved scaling)
TITLE_FONT_SIZE = int(SIDE_PANEL_WIDTH * 0.04)
INFO_FONT_SIZE = int(SIDE_PANEL_WIDTH * 0.035)
SCORE_FONT_SIZE = int(SIDE_PANEL_WIDTH * 0.04)
COORD_FONT_SIZE = int(SIDE_PANEL_WIDTH * 0.025)

# Create fonts with better typography
title_font = pygame.font.SysFont('Helvetica', TITLE_FONT_SIZE, bold=True)
info_font = pygame.font.SysFont('Helvetica', INFO_FONT_SIZE)
score_font = pygame.font.SysFont('Helvetica', SCORE_FONT_SIZE, bold=True)
coord_font = pygame.font.SysFont('Helvetica', COORD_FONT_SIZE)

# Update color scheme with Material Design 3 colors
BACKGROUND = (255, 255, 255)  # White background
BOARD_WHITE = (238, 238, 238)  # Slightly off-white for better contrast
BOARD_BLACK = (118, 150, 86)  # Modern green for dark squares
HIGHLIGHT = (0, 0, 0, 40)  # Subtle black highlight
MOVE_HIGHLIGHT = (76, 175, 80, 160)  # Material green
CHECK_HIGHLIGHT = (244, 67, 54, 160)  # Material red
BEST_MOVE_HIGHLIGHT = (33, 150, 243, 160)  # Material blue
INPUT_BOX_COLOR = (245, 245, 245)  # Light input box
INPUT_BOX_BORDER = (224, 224, 224)  # Light border
TEXT_COLOR = (33, 33, 33)  # Dark text
ACCENT_COLOR = (33, 150, 243)  # Material blue
SCORE_COLOR = (76, 175, 80)  # Material green
PANEL_COLOR = (250, 250, 250)  # Light panel
PANEL_BORDER = (224, 224, 224)  # Light panel border
SIDE_PANEL_COLOR = (245, 245, 245)  # Light side panel
SIDE_PANEL_BORDER = (224, 224, 224)  # Light side panel border

# Modern toggle colors
TOGGLE_ON = (76, 175, 80)  # Material green
TOGGLE_OFF = (158, 158, 158)  # Material gray
TOGGLE_BG = (245, 245, 245)
TOGGLE_SLIDER = (224, 224, 224)
TOGGLE_WHITE = (255, 255, 255)
TOGGLE_BLACK = (50, 50, 50)
TOGGLE_ACTIVE = (76, 175, 80)  # Green for active
TOGGLE_BORDER = (224, 224, 224)

# Side toggle colors
SIDE_TOGGLE_ON = (76, 175, 80)  # Material green
SIDE_TOGGLE_OFF = (158, 158, 158)  # Material gray
SIDE_TOGGLE_BG = (66, 66, 66)  # Dark gray

# Suggestion box colors
SUGGESTION_BOX_COLOR = (40, 40, 40)  # Dark background for suggestions
SUGGESTION_BOX_BORDER = (60, 60, 60)     # Border color for suggestions
SUGGESTION_HIGHLIGHT = (76, 175, 80, 40)  # Highlight color for best moves
SUGGESTION_TEXT = (255, 255, 255)  # White text for suggestions

# Arrow and move indicator colors
ARROW_COLOR = (76, 175, 80, 180)  # Semi-transparent green
ARROW_WIDTH = 3
ARROW_HEAD_SIZE = 10
SUGGESTED_MOVE_HIGHLIGHT = (33, 150, 243, 160)  # Material blue
SUGGESTED_CAPTURE_HIGHLIGHT = (244, 67, 54, 160)  # Material red

# Button colors
RESTART_BUTTON_COLOR = (33, 150, 243)  # Material blue
RESTART_BUTTON_HOVER = (30, 136, 229)  # Darker blue for hover
RESTART_BUTTON_TEXT = (255, 255, 255)  # White text

# Limit toggle colors
LIMIT_TOGGLE_ON = (76, 175, 80)  # Material green
LIMIT_TOGGLE_OFF = (244, 67, 54)  # Material red
LIMIT_TOGGLE_BG = (40, 40, 40)

# Loading overlay colors
LOADING_OVERLAY_COLOR = (0, 0, 0, 220)  # More opaque black
LOADING_SPINNER_COLOR = (33, 150, 243)  # Material blue
LOADING_TEXT_COLOR = (255, 255, 255)    # White

# Prediction box colors
PREDICTION_BOX_COLOR = (40, 40, 40)     # Dark background for predictions
PREDICTION_BORDER = (60, 60, 60)        # Border color
PREDICTION_HIGHLIGHT = (76, 175, 80, 40) # Green highlight
PREDICTION_TEXT = (255, 255, 255)       # White text
PREDICTION_ACCENT = (33, 150, 243)      # Blue accent

# Promotion menu colors
PROMOTION_MENU_COLOR = (40, 40, 40)
PROMOTION_MENU_BORDER = (60, 60, 60)
PROMOTION_HIGHLIGHT = (76, 175, 80, 40)
PROMOTION_TEXT = (255, 255, 255)
PROMOTION_MESSAGE = "Choose a piece to promote to:"

# Modal colors
MODAL_COLOR = (40, 40, 40)  # Dark background for modal
MODAL_BORDER = (60, 60, 60)  # Border color for modal
MODAL_TEXT = (255, 255, 255)  # Text color for modal
MODAL_TITLE = (33, 150, 243)  # Title color for modal
MODAL_ACCENT = (76, 175, 80)  # Accent color for modal
MODAL_BACKGROUND = (40, 40, 40)  # Dark background for modal

# Error message colors
ERROR_MESSAGE_COLOR = (244, 67, 54)  # Material red for error messages
ERROR_MESSAGE_DURATION = 2.0  # Show error message for 2 seconds

# Piece values
PIECE_VALUES = {
    'p': 1,  # pawn
    'n': 3,  # knight
    'b': 3,  # bishop
    'r': 5,  # rook
    'q': 9,  # queen
    'k': 0   # king (not counted in scoring)
}

# Add after pygame initialization
board = None  # Global board variable

# Add after other global variables
info_modal_active = False
info_button_rect = None
error_message = ""
error_message_time = 0

# Add these constants at the top with other color definitions
PROMOTION_ANIMATION_SPEED = 0.3  # seconds
PROMOTION_HOVER_SCALE = 1.1  # Scale factor for hover animation

# Add new modern color schemes
THEME = {
    'light': {
        'background': (255, 255, 255),
        'board_white': (238, 238, 238),
        'board_black': (118, 150, 86),
        'panel': (250, 250, 250),
        'text': (33, 33, 33),
        'accent': (33, 150, 243),
        'success': (76, 175, 80),
        'error': (244, 67, 54),
        'border': (224, 224, 224)
    },
    'dark': {
        'background': (18, 18, 18),
        'board_white': (238, 238, 238),
        'board_black': (118, 150, 86),
        'panel': (30, 30, 30),
        'text': (255, 255, 255),
        'accent': (33, 150, 243),
        'success': (76, 175, 80),
        'error': (244, 67, 54),
        'border': (45, 45, 45)
    }
}

# Animation constants
ANIMATION_SPEED = 0.3
HOVER_SCALE = 1.1
PIECE_MOVE_ANIMATION = 0.2
CAPTURE_ANIMATION = 0.3
CHECK_ANIMATION = 0.5

# Add new UI elements
class UIElement:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.hover = False
        self.animation_progress = 0
        self.visible = True

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.hover:
            self.animation_progress = min(1.0, self.animation_progress + 0.1)
        else:
            self.animation_progress = max(0.0, self.animation_progress - 0.1)

class Button(UIElement):
    def __init__(self, x, y, width, height, text, color, hover_color):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.on_click = None

    def draw(self, surface):
        if not self.visible:
            return

        # Animate button scale on hover
        scale = 1.0 + (HOVER_SCALE - 1.0) * self.animation_progress
        scaled_rect = self.rect.copy()
        scaled_rect.width = int(self.rect.width * scale)
        scaled_rect.height = int(self.rect.height * scale)
        scaled_rect.center = self.rect.center

        # Draw button with gradient
        color = self.color if not self.hover else self.hover_color
        draw_rounded_rect(surface, color, scaled_rect, 10, None, 0)

        # Draw text with shadow
        text_surface = info_font.render(self.text, True, (0, 0, 0, 50))
        shadow_rect = text_surface.get_rect(center=(scaled_rect.centerx + 2, scaled_rect.centery + 2))
        surface.blit(text_surface, shadow_rect)

        text_surface = info_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)

class Toggle(UIElement):
    def __init__(self, x, y, width, height, text, is_on=False):
        super().__init__(x, y, width, height)
        self.text = text
        self.is_on = is_on
        self.animation_progress = 1.0 if is_on else 0.0
        self.was_clicked = False

    def update(self, mouse_pos):
        was_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Only animate on hover, not on click
        if self.hover:
            self.animation_progress = min(1.0, self.animation_progress + 0.1)
        else:
            self.animation_progress = max(0.0, self.animation_progress - 0.1)
        
        # Reset click state when mouse is released
        if not pygame.mouse.get_pressed()[0]:
            self.was_clicked = False

    def toggle(self):
        if not self.was_clicked:  # Only toggle if not already clicked
            self.is_on = not self.is_on
            self.was_clicked = True
            return self.is_on
        return self.is_on

    def draw(self, surface):
        if not self.visible:
            return

        # Draw background
        draw_rounded_rect(surface, TOGGLE_BG, self.rect, 20, TOGGLE_BORDER, 1)
        
        # Draw toggle switch
        switch_width = 60
        switch_height = 30
        switch_x = self.rect.right - switch_width - 20
        switch_y = self.rect.y + (self.rect.height - switch_height) // 2
        
        # Draw switch background with gradient
        switch_rect = pygame.Rect(switch_x, switch_y, switch_width, switch_height)
        draw_rounded_rect(surface, TOGGLE_SLIDER, switch_rect, 15, None, 0)
        
        # Draw switch button with animation
        button_size = 26
        button_x = switch_x + (switch_width - button_size) * self.animation_progress
        button_y = switch_y + (switch_height - button_size) // 2
        button_color = TOGGLE_WHITE if self.is_on else TOGGLE_BLACK
        draw_rounded_rect(surface, button_color, 
                         pygame.Rect(button_x, button_y, button_size, button_size), 
                         13, None, 0)
        
        # Draw text with proper spacing
        text_surface = info_font.render(self.text, True, TEXT_COLOR)
        text_x = self.rect.x + 20
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        surface.blit(text_surface, (text_x, text_y))

# Add new animation functions
def animate_piece_move(surface, piece, start_pos, end_pos, progress):
    """Animate a piece moving from start_pos to end_pos"""
    if not piece:
        return

    # Calculate current position
    current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
    current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

    # Draw piece at current position with shadow
    draw_piece(surface, piece, current_x, current_y, SQUARE_SIZE)

def animate_capture(surface, square, progress):
    """Animate a piece being captured"""
    # Create flash effect
    alpha = int(255 * (1 - progress))
    flash = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    flash.fill((255, 0, 0, alpha))
    surface.blit(flash, (square[0] * SQUARE_SIZE, square[1] * SQUARE_SIZE))

def animate_check(surface, square, progress):
    """Animate check effect"""
    # Create pulsing effect
    alpha = int(128 * (1 + math.sin(progress * math.pi * 2)) / 2)
    pulse = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    pulse.fill((255, 0, 0, alpha))
    surface.blit(pulse, (square[0] * SQUARE_SIZE, square[1] * SQUARE_SIZE))

# Add new UI components
class GameStats:
    def __init__(self):
        self.moves_history = []
        self.captures_history = []
        self.evaluation_history = []
        self.max_history = 10

    def add_move(self, move, capture=None, evaluation=None):
        self.moves_history.append(move)
        if capture:
            self.captures_history.append(capture)
        if evaluation:
            self.evaluation_history.append(evaluation)

        # Keep history limited
        if len(self.moves_history) > self.max_history:
            self.moves_history.pop(0)
            if self.captures_history:
                self.captures_history.pop(0)
            if self.evaluation_history:
                self.evaluation_history.pop(0)

class GameUI:
    def __init__(self, layout):
        self.layout = layout
        self.theme = THEME['light']  # Use light theme by default
        self.stats = GameStats()
        self.buttons = []
        self.toggles = []
        self.sliders = []
        self.particle_system = ParticleSystem()
        self.tooltip = Tooltip()
        self.last_frame_time = time.time()
        self.initialize_ui()

    def initialize_ui(self):
        # Header Section
        self.buttons.extend([
            Button(self.layout.board_width + self.layout.padding, 
                  self.layout.header_y + self.layout.padding,
                  200, 40, "New Game", 
                  self.theme['accent'], self.theme['success']),
            Button(self.layout.board_width + self.layout.padding + 210,
                  self.layout.header_y + self.layout.padding,
                  200, 40, "Analysis",
                  self.theme['accent'], self.theme['success'])
        ])

        # Controls Section
        controls_x = self.layout.board_width + self.layout.padding
        controls_y = self.layout.controls_y + self.layout.padding
        toggle_width = 250  # Increased width for better text display
        toggle_height = 40
        toggle_spacing = 60  # Increased spacing between toggles
        
        # Side toggle
        self.toggles.append(
            Toggle(controls_x, controls_y, toggle_width, toggle_height, "Target Side: White")
        )
        
        # Move limit toggle
        self.toggles.append(
            Toggle(controls_x, controls_y + toggle_spacing, toggle_width, toggle_height, "12-Move Limit")
        )
        
        # Engine toggle
        self.toggles.append(
            Toggle(controls_x, controls_y + toggle_spacing * 2, toggle_width, toggle_height, "Engine Analysis")
        )
        
        # Sound toggle
        self.toggles.append(
            Toggle(controls_x, controls_y + toggle_spacing * 3, toggle_width, toggle_height, "Sound Effects")
        )
        
        # Theme toggle
        self.toggles.append(
            Toggle(controls_x, controls_y + toggle_spacing * 4, toggle_width, toggle_height, "Dark Mode")
        )

        # Initialize panels
        self.initialize_game_info()
        self.initialize_move_history()

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme = THEME['dark'] if self.theme == THEME['light'] else THEME['light']
        # Update global colors
        global BACKGROUND, TEXT_COLOR, PANEL_COLOR, PANEL_BORDER
        BACKGROUND = self.theme['background']
        TEXT_COLOR = self.theme['text']
        PANEL_COLOR = self.theme['panel']
        PANEL_BORDER = self.theme['border']

    def initialize_game_info(self):
        """Initialize the game info panel"""
        info_x = self.layout.board_width + self.layout.padding
        info_y = self.layout.game_info_y + self.layout.padding
        
        # Create info panel
        self.info_panel = pygame.Rect(
            info_x,
            info_y,
            self.layout.side_panel_width - 2 * self.layout.padding,
            self.layout.game_info_height - 2 * self.layout.padding
        )

    def initialize_move_history(self):
        """Initialize the move history panel"""
        history_x = self.layout.board_width + self.layout.padding
        history_y = self.layout.move_history_y + self.layout.padding
        
        # Create history panel
        self.history_panel = pygame.Rect(
            history_x,
            history_y,
            self.layout.side_panel_width - 2 * self.layout.padding,
            self.layout.move_history_height - 2 * self.layout.padding
        )

    def draw(self, surface):
        # Draw header section
        self.draw_header(surface)
        
        # Draw controls section
        self.draw_controls(surface)
        
        # Draw game info section
        self.draw_game_info(surface)
        
        # Draw move history section
        self.draw_move_history(surface)
        
        # Draw particle effects
        self.particle_system.draw(surface)
        
        # Draw tooltips
        self.tooltip.draw(surface)

    def draw_header(self, surface):
        # Draw header background
        header_rect = pygame.Rect(
            self.layout.board_width,
            self.layout.header_y,
            self.layout.side_panel_width,
            self.layout.header_height
        )
        draw_rounded_rect(surface, self.theme['panel'], header_rect, 0, 
                         self.theme['border'], 1)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def draw_controls(self, surface):
        # Draw controls background
        controls_rect = pygame.Rect(
            self.layout.board_width,
            self.layout.controls_y,
            self.layout.side_panel_width,
            self.layout.controls_height
        )
        draw_rounded_rect(surface, self.theme['panel'], controls_rect, 0,
                         self.theme['border'], 1)
        
        # Draw section title
        title = title_font.render("Game Controls", True, self.theme['text'])
        surface.blit(title, (controls_rect.x + self.layout.padding,
                            controls_rect.y + self.layout.padding))
        
        # Draw toggles
        for toggle in self.toggles:
            toggle.draw(surface)

    def draw_game_info(self, surface):
        # Draw game info background
        draw_rounded_rect(surface, self.theme['panel'], self.info_panel, 10,
                         self.theme['border'], 1)
        
        # Draw section title
        title = title_font.render("Game Status", True, self.theme['text'])
        surface.blit(title, (self.info_panel.x + self.layout.padding,
                            self.info_panel.y + self.layout.padding))
        
        # Draw game information
        y = self.info_panel.y + 50
        for text in [
            f"Turn: {'White' if board.board.turn else 'Black'}",
            f"Moves: {board.moves_made}/{board.max_moves if board.move_limit_enabled else '∞'}",
            f"White Score: {board.white_score}",
            f"Black Score: {board.black_score}",
            f"Last Capture: {board.last_capture[0] if board.last_capture else 'None'}"
        ]:
            text_surface = info_font.render(text, True, self.theme['text'])
            surface.blit(text_surface, (self.info_panel.x + self.layout.padding, y))
            y += text_surface.get_height() + self.layout.element_spacing

    def draw_move_history(self, surface):
        # Draw move history background
        draw_rounded_rect(surface, self.theme['panel'], self.history_panel, 10,
                         self.theme['border'], 1)
        
        # Draw section title
        title = title_font.render("Move History", True, self.theme['text'])
        surface.blit(title, (self.history_panel.x + self.layout.padding,
                            self.history_panel.y + self.layout.padding))
        
        # Draw moves
        y = self.history_panel.y + 50
        for i, move in enumerate(self.stats.moves_history):
            move_text = f"{i+1}. {move}"
            text_surface = info_font.render(move_text, True, self.theme['text'])
            surface.blit(text_surface, (self.history_panel.x + self.layout.padding, y))
            y += text_surface.get_height() + self.layout.element_spacing

    def update(self, mouse_pos):
        """Update UI elements and handle interactions"""
        # Update buttons
        for button in self.buttons:
            button.update(mouse_pos)
        
        # Update toggles
        for toggle in self.toggles:
            toggle.update(mouse_pos)
        
        # Update particle system
        current_time = time.time()
        dt = current_time - self.last_frame_time
        self.last_frame_time = current_time
        self.particle_system.update(dt)
        
        # Update tooltip
        self.tooltip.update(dt)
        
        # Show tooltips for buttons
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.tooltip.show(button.text, mouse_pos)
                break
        else:
            self.tooltip.hide()

    def emit_particles(self, x, y, color):
        """Emit particles at the specified position"""
        self.particle_system.emit(x, y, color)

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        self.engine = None
        self.engine_enabled = True  # Add engine enabled flag
        self.best_move = None
        self.evaluation = None
        self.is_analyzing = False
        self.analysis_start_time = 0
        self.analysis_depth = 0
        self.analysis_speed = 0
        self.initialize_engine()
        self.moves_made = 0
        self.max_moves = float('inf')  # No move limit by default
        self.move_limit_enabled = False  # Move limit disabled by default
        self.white_score = 0
        self.black_score = 0
        self.last_capture = None
        self.game_over = False
        self.winner = None
        self.suggested_moves = []
        self.future_moves = []
        self.target_side = 'white'
        self.last_analysis_time = 0
        self.analysis_cooldown = 1.0
        self.valid_moves_cache = {}
        self.promotion_pending = False
        self.promotion_square = None
        self.promotion_from_square = None
        self.promotion_start_time = 0
        self.update_suggested_moves()
    
    def initialize_engine(self):
        """Initialize chess engine with essential settings"""
        try:
            stockfish_path = "/opt/homebrew/bin/stockfish"
            if not os.path.exists(stockfish_path):
                stockfish_path = "stockfish"
            
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            # Use only supported options according to error message
            self.engine.configure({
                "Threads": 2,            # Reduced threads for faster analysis
                "Hash": 128,             # Reduced hash size
                "Skill Level": 20,       # Maximum skill level
                "Move Overhead": 10      # Lower move overhead for faster analysis
            })
            print("Stockfish engine initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Stockfish: {e}")
            self.engine = None
    
    def get_winning_side(self, score):
        """Determine the winning side based on the evaluation score object."""
        try:
            # Use centipawn score if available
            if self.board.turn:  # White to move
                val = score.white().score(mate_score=10000)
            else:
                val = score.black().score(mate_score=10000)
            if val is not None:
                if val > 0:
                    return chess.WHITE
                elif val < 0:
                    return chess.BLACK
        except Exception:
            pass
        return self.board.turn  # fallback
    
    def toggle_move_limit(self):
        """Toggle the move limit on/off"""
        self.move_limit_enabled = not self.move_limit_enabled
        if not self.move_limit_enabled:
            self.max_moves = float('inf')  # No move limit
        else:
            self.max_moves = 12
        self.update_suggested_moves()
    
    def toggle_engine(self):
        """Toggle the chess engine on/off"""
        self.engine_enabled = not self.engine_enabled
        if self.engine_enabled:
            self.initialize_engine()
        else:
            if self.engine:
                try:
                    self.engine.quit()
                except chess.engine.EngineTerminatedError:
                    pass
            self.engine = None
            self.suggested_moves = []
            self.future_moves = []
        return self.engine_enabled
    
    def update_suggested_moves(self):
        """Find the best moves based on current mode"""
        if not self.engine_enabled or not self.engine:
            self.suggested_moves = []
            self.future_moves = []
            return
        
        current_time = time.time()
        if current_time - self.last_analysis_time < self.analysis_cooldown:
            return
        
        self.last_analysis_time = current_time
        self.suggested_moves = []
        self.future_moves = []
        self.is_analyzing = True
        self.analysis_start_time = current_time
        self.analysis_depth = 0
        self.analysis_speed = 0
        
        try:
            # Adjust analysis depth based on mode
            depth = 8 if not self.move_limit_enabled else 5  # Reduced depth
            time_limit = 0.5 if not self.move_limit_enabled else 0.2  # Reduced time limit
            
            # Analyze position with MultiPV
            info_list = self.engine.analyse(self.board, chess.engine.Limit(depth=depth, time=time_limit), multipv=3)
            if not isinstance(info_list, list):
                info_list = [info_list]
            
            # Update analysis metrics
            elapsed_time = time.time() - self.analysis_start_time
            if elapsed_time > 0:
                self.analysis_speed = depth / elapsed_time  # nodes per second
            self.analysis_depth = depth
            
            # Get all legal moves
            legal_moves = list(self.board.legal_moves)
            
            # Collect moves
            capturing_moves = []
            future_moves = []
            for info in info_list:
                if "pv" in info and info["pv"]:
                    move = info["pv"][0]
                    if move in legal_moves:
                        # Verify the move is actually legal
                        try:
                            self.board.push(move)
                            self.board.pop()
                            
                            moving_piece = self.board.piece_at(move.from_square)
                            moving_piece_name = moving_piece.symbol().upper() if moving_piece else "?"
                            is_capture = self.board.is_capture(move)
                            points = 0
                            captured_piece_name = ""
                            if is_capture:
                                captured_piece = self.board.piece_at(move.to_square)
                                if captured_piece:
                                    points = PIECE_VALUES.get(captured_piece.symbol().lower(), 0)
                                    captured_piece_name = captured_piece.symbol().upper()
                            
                            # Evaluation
                            eval_text = "?"
                            score = info.get("score", None)
                            if score:
                                try:
                                    eval_pawns = score.relative.score(mate_score=10000) / 100.0
                                    eval_text = f"{eval_pawns:+.1f}"
                                except Exception:
                                    pass
                            
                            # Opponent response prediction
                            opponent_response = ""
                            if len(info["pv"]) > 1:
                                opp_move = info["pv"][1]
                                if opp_move in self.board.legal_moves:
                                    opp_from = chess.square_name(opp_move.from_square)
                                    opp_to = chess.square_name(opp_move.to_square)
                                    opponent_response = f"{opp_from}-{opp_to}"
                            
                            move_info = {
                                'move': move,
                                'from_piece': moving_piece_name,
                                'from_square': chess.square_name(move.from_square),
                                'to_square': chess.square_name(move.to_square),
                                'is_safe': True,
                                'evaluation': eval_text,
                                'opponent_response': opponent_response
                            }
                            
                            if is_capture:
                                move_info['to_piece'] = captured_piece_name
                                move_info['points'] = points
                                capturing_moves.append(move_info)
                            else:
                                future_moves.append(move_info)
                        except:
                            continue
            
            # Sort and assign
            capturing_moves.sort(key=lambda x: x.get('points', 0), reverse=True)
            self.suggested_moves = capturing_moves[:3]
            self.future_moves = future_moves[:3]
            
        except Exception as e:
            print(f"Error in move analysis: {e}")
        finally:
            self.is_analyzing = False
    
    def analyze_position(self):
        if not self.engine:
            return
        
        try:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
            self.best_move = info["pv"][0] if "pv" in info else None
            
            score = info.get("score", None)
            if score:
                try:
                    # Always show score from current player's perspective
                    if self.board.turn:  # White's turn
                        white_score = score.white()
                        if hasattr(white_score, 'score'):
                            eval_pawns = white_score.score() / 100.0
                            self.evaluation = f"{eval_pawns:+.1f}"
                        else:
                            self.evaluation = "?"
                    else:  # Black's turn
                        black_score = score.black()
                        if hasattr(black_score, 'score'):
                            eval_pawns = black_score.score() / 100.0
                            self.evaluation = f"{eval_pawns:+.1f}"
                        else:
                            self.evaluation = "?"
                except Exception as e:
                    self.evaluation = "?"
                    # Don't print the error to avoid console spam
            else:
                self.evaluation = "?"
        except Exception as e:
            print(f"Analysis error: {e}")
            self.best_move = None
            self.evaluation = None
    
    def set_from_fen(self, fen):
        try:
            new_board = chess.Board(fen)
            self.board = new_board
            self.moves_made = 0
            self.white_score = 0
            self.black_score = 0
            self.last_capture = None
            self.game_over = False
            self.winner = None
            self.analyze_position()
            self.update_suggested_moves()
            return True
        except:
            return False
    
    def get_valid_moves(self, square):
        """Get valid moves with proper chess move validation"""
        if self.game_over or self.moves_made >= self.max_moves:
            return []
        
        # Check cache first
        if square in self.valid_moves_cache:
            return self.valid_moves_cache[square]
        
        moves = []
        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:  # Only allow moves for current player's pieces
            for move in self.board.legal_moves:
                if move.from_square == square:
                    moves.append(move.to_square)
        
        # Cache the result
        self.valid_moves_cache[square] = moves
        return moves
    
    def make_move(self, from_square, to_square, promotion_piece=None):
        """Make a move with proper validation and promotion handling"""
        if self.game_over or self.moves_made >= self.max_moves:
            return False, "Game is over or maximum moves reached"
        
        try:
            # Get coordinates for validation
            from_rank = chess.square_rank(from_square)
            from_file = chess.square_file(from_square)
            to_rank = chess.square_rank(to_square)
            to_file = chess.square_file(to_square)
            
            # Get the piece being moved
            piece = self.board.piece_at(from_square)
            if not piece:
                return False, "No piece to move"
            
            # Create the move
            if promotion_piece:
                try:
                    promotion = chess.Piece.from_symbol(promotion_piece.upper())
                    move = chess.Move(from_square, to_square, promotion=promotion.piece_type)
                except Exception as e:
                    print(f"Error creating promotion move: {e}")
                    return False, "Invalid promotion piece"
            else:
                move = chess.Move(from_square, to_square)
            
            # Check if the move is legal
            if move in self.board.legal_moves:
                # Check if this is a pawn promotion
               # Modify this section:
                if piece.piece_type == chess.PAWN and \
                    ((piece.color == chess.WHITE and to_rank == 7) or 
                    (piece.color == chess.BLACK and to_rank == 0)):
                    
                    # Handle promotion with capture
                    if self.board.is_capture(move):
                        # Capture is valid, proceed with promotion
                        if promotion_piece:
                            move = chess.Move(from_square, to_square, 
                                            promotion=chess.Piece.from_symbol(promotion_piece.upper()).piece_type)
                            if move in self.board.legal_moves:
                                self.board.push(move)
                                self.moves_made += 1
                                self.valid_moves_cache.clear()
                                self.analyze_position()
                                self.update_suggested_moves()
                                self.check_game_over()
                                return True, None
                        else:
                            # Set promotion pending state even for captures
                            self.promotion_pending = True
                            self.promotion_square = to_square
                            self.promotion_from_square = from_square
                            self.promotion_start_time = time.time()
                            return True, "Promotion required"

                # Process captures if applicable
                if self.board.is_capture(move):
                    captured_piece = self.board.piece_at(to_square)
                    if captured_piece:
                        piece_value = PIECE_VALUES.get(captured_piece.symbol().lower(), 0)
                        if self.board.turn:  # White's turn
                            self.white_score += piece_value
                        else:
                            self.black_score += piece_value
                        self.last_capture = (captured_piece.symbol(), piece_value)
                
                # Make the move
                self.board.push(move)
                self.moves_made += 1
                # Clear move cache after making a move
                self.valid_moves_cache.clear()
                # Immediately analyze the new position
                self.analyze_position()
                # Force a suggestion update
                self.last_analysis_time = 0
                self.check_game_over()
                return True, None
            
            # If move is not legal, provide more specific error message
            elif piece.piece_type == chess.PAWN:
                # Allow diagonal moves for captures
                if from_file != to_file:
                    if not self.board.is_capture(move):
                        return False, "Pawns can only move diagonally to capture pieces"
                elif (piece.color == chess.WHITE and to_rank <= from_rank) or \
                     (piece.color == chess.BLACK and to_rank >= from_rank):
                    return False, "Pawns can only move forward"
                elif abs(to_rank - from_rank) > 2 or \
                     (abs(to_rank - from_rank) == 2 and from_rank != (1 if piece.color == chess.WHITE else 6)):
                    return False, "Pawns can only move one square, or two squares on their first move"
                elif ((piece.color == chess.WHITE and to_rank == 7) or \
                      (piece.color == chess.BLACK and to_rank == 0)):
                    return False, "Pawn must be promoted when reaching the last rank"
            elif piece.piece_type == chess.KING:
                if abs(to_file - from_file) > 1 or abs(to_rank - from_rank) > 1:
                    return False, "Kings can only move one square in any direction"
            elif piece.piece_type == chess.KNIGHT:
                if not ((abs(to_file - from_file) == 2 and abs(to_rank - from_rank) == 1) or \
                       (abs(to_file - from_file) == 1 and abs(to_rank - from_rank) == 2)):
                    return False, "Knights move in an L-shape: 2 squares in one direction, then 1 square perpendicular"
            elif piece.piece_type == chess.BISHOP:
                if abs(to_file - from_file) != abs(to_rank - from_rank):
                    return False, "Bishops can only move diagonally"
            elif piece.piece_type == chess.ROOK:
                if from_file != to_file and from_rank != to_rank:
                    return False, "Rooks can only move horizontally or vertically"
            elif piece.piece_type == chess.QUEEN:
                if not (from_file == to_file or from_rank == to_rank or \
                       abs(to_file - from_file) == abs(to_rank - from_rank)):
                    return False, "Queens can move horizontally, vertically, or diagonally"
            
            return False, "Invalid move"
        except Exception as e:
            print(f"Error making move: {e}")
            return False, f"Error making move: {str(e)}"
    
    def check_game_over(self):
        if self.moves_made >= self.max_moves:
            self.game_over = True
            if self.white_score > self.black_score:
                self.winner = "White"
            elif self.black_score > self.white_score:
                self.winner = "Black"
            else:
                self.winner = "Draw"
            return True
        return False
    
    def get_piece_at(self, square):
        piece = self.board.piece_at(square)
        if piece:
            color = 'white' if piece.color else 'black'
            piece_type = piece.symbol().lower()
            return f"{color}_{piece_type}"
        return None
    
    def __del__(self):
        if self.engine:
            self.engine.quit()

def square_to_coords(square):
    return (chess.square_file(square), chess.square_rank(square))

def coords_to_square(x, y):
    return chess.square(x, 7-y)

def draw_piece(surface, piece, x, y, square_size):
    if not piece:
        return
    
    color = (255, 255, 255) if piece.startswith('white') else (50, 50, 50)
    piece_type = piece.split('_')[1]
    
    # Draw piece with modern styling
    center_x = x + square_size//2
    center_y = y + square_size//2
    radius = int(square_size * 0.4)  # Slightly larger pieces
    
    # Draw piece shadow
    shadow_offset = 3
    pygame.draw.circle(surface, (0, 0, 0, 100), 
                      (center_x + shadow_offset, center_y + shadow_offset), 
                      radius)
    
    # Draw piece with gradient
    for i in range(radius, 0, -1):
        alpha = 255 - (i * 2)
        if alpha < 0:
            alpha = 0
        pygame.draw.circle(surface, (*color, alpha), (center_x, center_y), i)
    
    # Draw piece symbol with larger font
    font = pygame.font.SysFont('Helvetica', int(square_size * 0.6), bold=True)
    text = font.render(piece_type.upper(), True, 
                      (30, 30, 30) if color == (255, 255, 255) else (255, 255, 255))
    text_rect = text.get_rect(center=(center_x, center_y))
    surface.blit(text, text_rect)

def draw_rounded_rect(surface, color, rect, border_radius, border_color=None, border_width=0):
    """Draw a rounded rectangle with optional border"""
    # Draw the main rectangle
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    
    # Draw the border if specified
    if border_color and border_width > 0:
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=border_radius)

def get_clipboard_content():
    """Get clipboard content with better error handling"""
    try:
        if sys.platform == 'darwin':  # macOS
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        elif sys.platform == 'win32':  # Windows
            result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], capture_output=True, text=True)
        else:  # Linux
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Error getting clipboard content: {e}")
    return ""

def draw_toggle(surface, rect, is_white, text):
    """Draw a modern toggle switch with text"""
    # Draw background
    draw_rounded_rect(surface, TOGGLE_BG, rect, 20, TOGGLE_BORDER, 1)
    
    # Draw toggle switch
    switch_width = 60
    switch_height = 30
    switch_x = rect.right - switch_width - 20
    switch_y = rect.y + (rect.height - switch_height) // 2
    
    # Draw switch background with gradient
    switch_rect = pygame.Rect(switch_x, switch_y, switch_width, switch_height)
    draw_rounded_rect(surface, TOGGLE_SLIDER, switch_rect, 15, None, 0)
    
    # Draw switch button
    button_size = 26
    button_x = switch_x + (switch_width - button_size) if is_white else switch_x + 2
    button_y = switch_y + (switch_height - button_size) // 2
    button_color = TOGGLE_WHITE if is_white else TOGGLE_BLACK
    draw_rounded_rect(surface, button_color, 
                     pygame.Rect(button_x, button_y, button_size, button_size), 
                     13, None, 0)
    
    # Draw text
    text_surface = info_font.render(text, True, TEXT_COLOR)
    text_x = rect.x + 20
    text_y = rect.y + (rect.height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))

def analyze_move_explanation(board, move_info):
    """Generate user-friendly explanation for a suggested move"""
    try:
        move = move_info['move']
        from_square = move.from_square
        to_square = move.to_square
        piece = board.board.piece_at(from_square)
        piece_name = piece.symbol().upper() if piece else "?"
        
        explanation = []
        
        # Basic move description in user-friendly terms
        explanation.append(f"Move your {piece_name} from {chess.square_name(from_square)} to {chess.square_name(to_square)}")
        
        # Capture analysis with clear point value
        if board.board.is_capture(move):
            captured = board.board.piece_at(to_square)
            if captured:
                points = PIECE_VALUES.get(captured.symbol().lower(), 0)
                explanation.append(f"Capture opponent's {captured.symbol().upper()} for {points} points!")
        
        # Check if move creates threats
        board.push(move)
        if board.board.is_check():
            explanation.append("This move puts the opponent's king in check!")
        
        # Analyze tactical elements in user-friendly terms
        if board.board.is_attacked_by(not board.board.turn, to_square):
            explanation.append("⚠️ Warning: This square is under attack")
            if board.board.is_attacked_by(board.board.turn, to_square):
                explanation.append("✅ But your piece will be defended")
        
        # Analyze piece development and positioning
        if piece.piece_type == chess.PAWN:
            if to_square in [chess.E4, chess.E5, chess.D4, chess.D5]:
                explanation.append("Controls important center squares")
            if abs(chess.square_file(to_square) - chess.square_file(from_square)) > 0:
                explanation.append("Opens up the position for your other pieces")
        elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            if to_square in [chess.C3, chess.D3, chess.E3, chess.F3, chess.C6, chess.D6, chess.E6, chess.F6]:
                explanation.append("Develops your piece to a strong position")
        elif piece.piece_type == chess.ROOK:
            if chess.square_rank(to_square) in [0, 7]:
                explanation.append("Places your rook on an open file")
        
        # Analyze king safety
        if piece.piece_type == chess.KING:
            if abs(chess.square_file(to_square) - chess.square_file(from_square)) > 1:
                explanation.append("Castles to protect your king")
        
        # Analyze material and position in user-friendly terms
        eval_pawns = float(move_info.get('evaluation', '0').replace('+', ''))
        if eval_pawns > 1:
            explanation.append(f"🎯 Strong position! ({eval_pawns:+.1f} advantage)")
        elif eval_pawns < -1:
            explanation.append(f"⚠️ Be careful! Position is difficult ({eval_pawns:+.1f})")
        
        # Opponent's likely response in user-friendly terms
        if move_info.get('opponent_response'):
            opp_from, opp_to = move_info['opponent_response'].split('-')
            explanation.append(f"Opponent might respond: {opp_from} to {opp_to}")
        
        board.pop()  # Undo the move
        return explanation
    except Exception as e:
        return ["Move analysis unavailable"]

def draw_suggestion_box(surface, board, x, y, width, height):
    """Draw the suggestion box with proper scrolling and overflow handling"""
    # Draw box background
    box_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, SUGGESTION_BOX_COLOR, box_rect, 10, SUGGESTION_BOX_BORDER, 2)
    
    # Draw title
    title_surface = info_font.render("Suggested Moves", True, SUGGESTION_TEXT)
    surface.blit(title_surface, (x + 10, y + 10))
    
    # Calculate content area
    content_x = x + 10
    content_y = y + 40
    content_width = width - 20
    line_height = 25
    max_lines = (height - 50) // line_height  # Leave space for title and padding
    
    # Get and format suggestions
    suggestions = []
    if board.suggested_moves:
        for i, move_info in enumerate(board.suggested_moves[:3], 1):
            try:
                move = move_info['move']
                from_square = chess.square_name(move.from_square)
                to_square = chess.square_name(move.to_square)
                piece = board.board.piece_at(move.from_square)
                if piece:
                    piece_name = piece.symbol().upper()
                    eval_text = move_info.get('evaluation', '?')
                    suggestions.append(f"{i}. {piece_name} {from_square}-{to_square} ({eval_text})")
            except Exception as e:
                print(f"Error formatting suggestion: {e}")
                continue
    
    # Draw suggestions with proper clipping
    for i, suggestion in enumerate(suggestions[:max_lines]):
        if content_y + line_height <= y + height - 10:  # Check if we have space
            text_surface = info_font.render(suggestion, True, SUGGESTION_TEXT)
            surface.blit(text_surface, (content_x, content_y))
            content_y += line_height
    
    # Draw scroll indicator if there are more suggestions than can be shown
    if len(suggestions) > max_lines:
        scroll_text = info_font.render("↑↓", True, SUGGESTION_TEXT)
        surface.blit(scroll_text, (x + width - 30, y + height - 30))

def draw_arrow(surface, start_pos, end_pos, color, width, head_size):
    """Draw an arrow from start_pos to end_pos"""
    try:
        # Calculate arrow direction and length
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = (dx**2 + dy**2)**0.5
        
        # Normalize direction
        if length > 0:
            dx = dx / length
            dy = dy / length
        
        # Calculate arrow head points
        head_angle = 0.5  # Angle in radians
        head_length = head_size
        
        # Calculate perpendicular direction
        perp_dx = -dy
        perp_dy = dx
        
        # Calculate arrow head points
        end_x = end_pos[0] - dx * head_length
        end_y = end_pos[1] - dy * head_length
        
        head1_x = end_x + perp_dx * head_length * math.sin(head_angle)
        head1_y = end_y + perp_dy * head_length * math.sin(head_angle)
        
        head2_x = end_x - perp_dx * head_length * math.sin(head_angle)
        head2_y = end_y - perp_dy * head_length * math.sin(head_angle)
        
        # Draw arrow line
        pygame.draw.line(surface, color, start_pos, (end_x, end_y), width)
        
        # Draw arrow head
        pygame.draw.polygon(surface, color, [
            end_pos,
            (head1_x, head1_y),
            (head2_x, head2_y)
        ])
    except Exception as e:
        print(f"Error drawing arrow: {e}")

def draw_suggested_moves(surface, board, square_size):
    """Draw visual indicators for suggested moves"""
    try:
        # Draw capturing moves first
        for i, move_info in enumerate(board.suggested_moves[:3]):
            try:
                # Convert squares to coordinates
                from_square = chess.parse_square(move_info['from_square'])
                to_square = chess.parse_square(move_info['to_square'])
                
                from_x = chess.square_file(from_square) * square_size + square_size // 2
                from_y = (7 - chess.square_rank(from_square)) * square_size + square_size // 2
                to_x = chess.square_file(to_square) * square_size + square_size // 2
                to_y = (7 - chess.square_rank(to_square)) * square_size + square_size // 2
                
                # Draw highlight for the target square
                s = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_color = SUGGESTED_CAPTURE_HIGHLIGHT if move_info.get('is_safe', True) else (244, 67, 54, 100)  # Red for unsafe
                pygame.draw.rect(s, highlight_color, (0, 0, square_size, square_size), border_radius=5)
                surface.blit(s, (chess.square_file(to_square) * square_size, 
                               (7 - chess.square_rank(to_square)) * square_size))
                
                # Draw arrow with different color for unsafe moves
                arrow_color = ARROW_COLOR if move_info.get('is_safe', True) else (244, 67, 54, 180)  # Red for unsafe
                draw_arrow(surface, (from_x, from_y), (to_x, to_y), arrow_color, ARROW_WIDTH, ARROW_HEAD_SIZE)
                
            except Exception as e:
                continue
        
        # Draw non-capturing moves
        for move_info in board.future_moves:
            try:
                # Convert squares to coordinates
                from_square = chess.parse_square(move_info['from_square'])
                to_square = chess.parse_square(move_info['to_square'])
                
                from_x = chess.square_file(from_square) * square_size + square_size // 2
                from_y = (7 - chess.square_rank(from_square)) * square_size + square_size // 2
                to_x = chess.square_file(to_square) * square_size + square_size // 2
                to_y = (7 - chess.square_rank(to_square)) * square_size + square_size // 2
                
                # Draw highlight for the target square
                s = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_color = SUGGESTED_MOVE_HIGHLIGHT if move_info.get('is_safe', True) else (244, 67, 54, 100)  # Red for unsafe
                pygame.draw.rect(s, highlight_color, (0, 0, square_size, square_size), border_radius=5)
                surface.blit(s, (chess.square_file(to_square) * square_size, 
                               (7 - chess.square_rank(to_square)) * square_size))
                
                # Draw arrow with different color for unsafe moves
                arrow_color = ARROW_COLOR if move_info.get('is_safe', True) else (244, 67, 54, 180)  # Red for unsafe
                draw_arrow(surface, (from_x, from_y), (to_x, to_y), arrow_color, ARROW_WIDTH, ARROW_HEAD_SIZE)
                
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error drawing suggested moves: {e}")

def cleanup():
    """Cleanup function to properly close all resources"""
    try:
        global board
        if board and board.engine:
            try:
                board.engine.quit()
            except chess.engine.EngineTerminatedError:
                pass  # Engine already terminated
    except:
        pass
    try:
        pygame.quit()
    except:
        pass
    sys.exit()

def draw_restart_button(surface, rect, is_hovered):
    """Draw a modern restart button"""
    # Draw button background
    color = RESTART_BUTTON_HOVER if is_hovered else RESTART_BUTTON_COLOR
    draw_rounded_rect(surface, color, rect, 10, None, 0)
    
    # Draw button text
    text = "Restart Game"
    text_surface = info_font.render(text, True, RESTART_BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_limit_toggle(surface, rect, is_enabled):
    """Draw the move limit toggle button"""
    # Draw background
    draw_rounded_rect(surface, LIMIT_TOGGLE_BG, rect, 20, TOGGLE_BORDER, 1)
    
    # Draw toggle switch
    switch_width = 60
    switch_height = 30
    switch_x = rect.right - switch_width - 20
    switch_y = rect.y + (rect.height - switch_height) // 2
    
    # Draw switch background
    switch_rect = pygame.Rect(switch_x, switch_y, switch_width, switch_height)
    draw_rounded_rect(surface, TOGGLE_SLIDER, switch_rect, 15, None, 0)
    
    # Draw switch button
    button_size = 26
    button_x = switch_x + (switch_width - button_size) if is_enabled else switch_x + 2
    button_y = switch_y + (switch_height - button_size) // 2
    button_color = LIMIT_TOGGLE_ON if is_enabled else LIMIT_TOGGLE_OFF
    draw_rounded_rect(surface, button_color, 
                     pygame.Rect(button_x, button_y, button_size, button_size), 
                     13, None, 0)
    
    # Draw text
    text = "12-Move Limit: ON" if is_enabled else "12-Move Limit: OFF"
    text_surface = info_font.render(text, True, TEXT_COLOR)
    text_x = rect.x + 20
    text_y = rect.y + (rect.height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))

def draw_info_button(surface, rect):
    """Draw the info button"""
    # Draw button background
    draw_rounded_rect(surface, ACCENT_COLOR, rect, 10, None, 0)
    
    # Draw info icon (i)
    text = "i"
    text_surface = title_font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_info_modal(surface):
    """Draw the info modal with game instructions"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    surface.blit(overlay, (0, 0))
    
    # Calculate modal dimensions
    modal_width = min(SCREEN_WIDTH - 100, 600)
    modal_height = min(SCREEN_HEIGHT - 100, 500)
    modal_x = (SCREEN_WIDTH - modal_width) // 2
    modal_y = (SCREEN_HEIGHT - modal_height) // 2
    
    # Draw modal background
    modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
    draw_rounded_rect(surface, MODAL_BACKGROUND, modal_rect, 10, MODAL_BORDER, 2)
    
    # Draw close button
    close_button_size = 30
    close_button_rect = pygame.Rect(
        modal_x + modal_width - close_button_size - 10,
        modal_y + 10,
        close_button_size,
        close_button_size
    )
    pygame.draw.rect(surface, MODAL_BORDER, close_button_rect, border_radius=5)
    pygame.draw.line(surface, MODAL_TEXT, 
                    (close_button_rect.x + 5, close_button_rect.y + 5),
                    (close_button_rect.x + close_button_rect.width - 5, close_button_rect.y + close_button_rect.height - 5), 2)
    pygame.draw.line(surface, MODAL_TEXT,
                    (close_button_rect.x + close_button_rect.width - 5, close_button_rect.y + 5),
                    (close_button_rect.x + 5, close_button_rect.y + close_button_rect.height - 5), 2)
    
    # Draw title
    title_surface = title_font.render("How to Play", True, MODAL_TEXT)
    title_x = modal_x + (modal_width - title_surface.get_width()) // 2
    surface.blit(title_surface, (title_x, modal_y + 20))
    
    # Draw content with scrolling
    content_y = modal_y + 60
    line_height = 25
    padding = 20
    
    # Content text
    content = [
        "Game Rules:",
        "• Capture pieces to score points",
        "• Pawn: 1 point",
        "• Knight: 3 points",
        "• Bishop: 3 points",
        "• Rook: 5 points",
        "• Queen: 9 points",
        "",
        "Controls:",
        "• Click to select and move pieces",
        "• Press 'A' to auto-play best moves",
        "• Toggle move limit on/off",
        "• Switch target side (White/Black)",
        "",
        "Tips:",
        "• Focus on capturing high-value pieces",
        "• Watch for suggested moves",
        "• Plan your strategy within 12 moves",
        "• Use the side panel to track progress"
    ]
    
    # Draw each line of content
    for line in content:
        if content_y + line_height <= modal_y + modal_height - padding:
            text_surface = info_font.render(line, True, MODAL_TEXT)
            surface.blit(text_surface, (modal_x + padding, content_y))
            content_y += line_height
    
    return close_button_rect

def draw_side_panel(surface, board, current_y):
    """Draw the side panel with game information"""
    # Draw side panel background
    draw_rounded_rect(surface, SIDE_PANEL_COLOR, 
                     pygame.Rect(BOARD_WIDTH, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT),
                     0, SIDE_PANEL_BORDER, 1)
    
    # Draw input box
    draw_rounded_rect(surface, INPUT_BOX_COLOR, input_box, 10, 
                     ACCENT_COLOR if input_active else INPUT_BOX_BORDER, 2)
    
    if input_text:
        text_surface = info_font.render(input_text, True, TEXT_COLOR)
    else:
        text_surface = info_font.render("Paste FEN string here", True, (150, 150, 150))
    
    text_y = input_box.y + (input_box.height - text_surface.get_height()) // 2
    surface.blit(text_surface, (input_box.x + 15, text_y))
    
    # Draw side toggle
    draw_toggle(surface, side_toggle_rect, 
               board.target_side == 'white',
               f"Target Side: {board.target_side.capitalize()}")
    
    # Draw move limit toggle
    limit_toggle_rect = pygame.Rect(
        BOARD_WIDTH + PADDING,
        side_toggle_rect.bottom + ELEMENT_SPACING,
        toggle_width,
        toggle_height
    )
    draw_limit_toggle(surface, limit_toggle_rect, board.move_limit_enabled)
    
    # Draw game info panel
    info_panel = pygame.Rect(
        BOARD_WIDTH + PADDING,
        limit_toggle_rect.bottom + ELEMENT_SPACING,
        toggle_width,
        SCREEN_HEIGHT - limit_toggle_rect.bottom - 2 * PADDING
    )
    draw_rounded_rect(surface, PANEL_COLOR, info_panel, 10, PANEL_BORDER, 1)
    
    # Draw game status
    current_y = info_panel.y + PADDING
    
    # Show analysis status if analyzing
    if getattr(board, 'is_analyzing', False):
        elapsed = time.time() - board.analysis_start_time
        loading_text = f"Analyzing... Depth: {board.analysis_depth}"
        speed_text = f"Speed: {board.analysis_speed:.1f} nodes/sec"
        time_text = f"Time: {elapsed:.1f}s"
        
        loading_surface = title_font.render(loading_text, True, (200, 200, 0))
        speed_surface = info_font.render(speed_text, True, (200, 200, 0))
        time_surface = info_font.render(time_text, True, (200, 200, 0))
        
        surface.blit(loading_surface, (info_panel.x + PADDING, current_y))
        current_y += loading_surface.get_height() + 10
        surface.blit(speed_surface, (info_panel.x + PADDING, current_y))
        current_y += speed_surface.get_height() + 5
        surface.blit(time_surface, (info_panel.x + PADDING, current_y))
        current_y += time_surface.get_height() + 20
    
    if not board.game_over:
        turn_text = "Your Turn (White)" if board.board.turn else "Black's Turn"
        moves_text = f"Moves: {board.moves_made}/{board.max_moves if board.move_limit_enabled else '∞'}"
    else:
        if board.winner == "Draw":
            turn_text = "Game Over - It's a Draw!"
        else:
            turn_text = f"Game Over - {board.winner} Wins!"
        moves_text = "Final Score"
    
    # Draw scores
    white_score_text = f"Your Score: {board.white_score} points"
    black_score_text = f"Black's Score: {board.black_score} points"
    
    if board.last_capture:
        last_capture_text = f"Last Capture: {board.last_capture[0]} (+{board.last_capture[1]} pts)"
    else:
        last_capture_text = "No captures yet"
    
    if not board.game_over:
        remaining_text = f"Remaining: {board.max_moves - board.moves_made if board.move_limit_enabled else '∞'} moves"
    else:
        remaining_text = "Game Over!"
    
    # Draw all text elements
    turn_surface = title_font.render(turn_text, True, ACCENT_COLOR)
    moves_surface = info_font.render(moves_text, True, TEXT_COLOR)
    white_score_surface = score_font.render(white_score_text, True, SCORE_COLOR)
    black_score_surface = score_font.render(black_score_text, True, SCORE_COLOR)
    last_capture_surface = info_font.render(last_capture_text, True, TEXT_COLOR)
    remaining_surface = title_font.render(remaining_text, True, ACCENT_COLOR)
    
    surface.blit(turn_surface, (info_panel.x + PADDING, current_y))
    current_y += ELEMENT_SPACING + turn_surface.get_height()
    
    surface.blit(moves_surface, (info_panel.x + PADDING, current_y))
    current_y += ELEMENT_SPACING + moves_surface.get_height()
    
    surface.blit(white_score_surface, (info_panel.x + PADDING, current_y))
    current_y += ELEMENT_SPACING + white_score_surface.get_height()
    
    surface.blit(black_score_surface, (info_panel.x + PADDING, current_y))
    current_y += ELEMENT_SPACING + black_score_surface.get_height()
    
    surface.blit(last_capture_surface, (info_panel.x + PADDING, current_y))
    current_y += ELEMENT_SPACING + last_capture_surface.get_height()
    
    surface.blit(remaining_surface, (info_panel.x + PADDING, current_y))
    current_y += ELEMENT_SPACING + remaining_surface.get_height() + 20
    
    # Draw restart button
    restart_button_rect = pygame.Rect(
        info_panel.x + PADDING,
        current_y,
        info_panel.width - 2 * PADDING,
        50
    )
    draw_restart_button(surface, restart_button_rect, restart_button_rect.collidepoint(pygame.mouse.get_pos()))
    current_y += restart_button_rect.height + 20
    
    # Draw info button
    global info_button_rect
    info_button_rect = pygame.Rect(
        info_panel.x + info_panel.width - 50,
        info_panel.y + 20,
        40,
        40
    )
    draw_info_button(surface, info_button_rect)
    
    return current_y, restart_button_rect, limit_toggle_rect

def auto_play_best_moves(board, n=6):
    """Automatically play the best move (by points, or best engine suggestion) for n moves."""
    for _ in range(n):
        board.update_suggested_moves()
        # Prefer capturing moves
        move_info = None
        if board.suggested_moves:
            move_info = board.suggested_moves[0]
        elif board.future_moves:
            move_info = board.future_moves[0]
        if move_info:
            move = move_info['move']
            board.make_move(move.from_square, move.to_square)
        else:
            break  # No moves available

def draw_board(surface, board, selected_square, square_size):
    """Draw the chess board with pieces and highlights"""
    for rank in range(BOARD_SIZE):
        for file in range(BOARD_SIZE):
            square = coords_to_square(file, rank)
            color = BOARD_WHITE if (rank + file) % 2 == 0 else BOARD_BLACK
            rect = pygame.Rect(
                file * SQUARE_SIZE,
                rank * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            pygame.draw.rect(screen, color, rect)
            
            # Draw coordinates
            if rank == 7:
                file_text = coord_font.render(chr(file + 97), True, 
                                            (100, 100, 100) if color == BOARD_WHITE else (200, 200, 200))
                screen.blit(file_text, (file * SQUARE_SIZE + 5, rank * SQUARE_SIZE + SQUARE_SIZE - 25))
            if file == 0:
                rank_text = coord_font.render(str(8 - rank), True, 
                                            (100, 100, 100) if color == BOARD_WHITE else (200, 200, 200))
                screen.blit(rank_text, (5, rank * SQUARE_SIZE + 5))
            
            # Draw highlights
            if selected_square == square:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(s, HIGHLIGHT, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(s, (file * SQUARE_SIZE, rank * SQUARE_SIZE))
            
            # Show all possible moves for selected piece
            if selected_square:
                valid_moves = board.get_valid_moves(selected_square)
                if square in valid_moves:
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    # Draw a semi-transparent purple highlight for legal moves
                    pygame.draw.rect(s, (156, 39, 176, 160), (0, 0, SQUARE_SIZE, SQUARE_SIZE), border_radius=5)
                    screen.blit(s, (file * SQUARE_SIZE, rank * SQUARE_SIZE))
            
            # Draw check highlight
            if board.board.is_check():
                king_square = None
                for sq in chess.SQUARES:
                    piece = board.board.piece_at(sq)
                    if piece and piece.piece_type == chess.KING and piece.color == board.board.turn:
                        king_square = sq
                        break
                
                if king_square == square:
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(s, CHECK_HIGHLIGHT, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(s, (file * SQUARE_SIZE, rank * SQUARE_SIZE))
            
            piece = board.get_piece_at(square)
            if piece:
                draw_piece(screen, piece, file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE)

def draw_loading_overlay(surface, board):
    """Draw a loading overlay with spinner animation"""
    if not getattr(board, 'is_analyzing', False):
        return
        
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(LOADING_OVERLAY_COLOR)
    surface.blit(overlay, (0, 0))
    
    # Calculate center position
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    
    # Draw spinner
    spinner_radius = 50  # Increased size
    spinner_width = 10   # Increased width
    current_time = time.time()
    angle = (current_time * 360) % 360  # Rotate 360 degrees per second
    
    # Draw spinner segments
    for i in range(8):
        segment_angle = angle + (i * 45)
        start_angle = math.radians(segment_angle)
        end_angle = math.radians(segment_angle + 30)
        
        # Calculate points for spinner segment
        start_x = center_x + math.cos(start_angle) * spinner_radius
        start_y = center_y + math.sin(start_angle) * spinner_radius
        end_x = center_x + math.cos(end_angle) * spinner_radius
        end_y = center_y + math.sin(end_angle) * spinner_radius
        
        # Draw segment with fading opacity
        alpha = 255 - (i * 30)
        if alpha < 0:
            alpha = 0
        color = (*LOADING_SPINNER_COLOR[:3], alpha)
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), spinner_width)
    
    # Draw loading text with larger font
    elapsed = time.time() - board.analysis_start_time
    loading_text = f"Analyzing Position..."
    depth_text = f"Search Depth: {board.analysis_depth}"
    speed_text = f"Analysis Speed: {board.analysis_speed:.1f} nodes/sec"
    time_text = f"Time Elapsed: {elapsed:.1f}s"
    
    # Create text surfaces with larger font
    loading_surface = title_font.render(loading_text, True, LOADING_TEXT_COLOR)
    depth_surface = info_font.render(depth_text, True, LOADING_TEXT_COLOR)
    speed_surface = info_font.render(speed_text, True, LOADING_TEXT_COLOR)
    time_surface = info_font.render(time_text, True, LOADING_TEXT_COLOR)
    
    # Position text below spinner with more spacing
    text_y = center_y + spinner_radius + 30
    surface.blit(loading_surface, (center_x - loading_surface.get_width()//2, text_y))
    text_y += loading_surface.get_height() + 15
    surface.blit(depth_surface, (center_x - depth_surface.get_width()//2, text_y))
    text_y += depth_surface.get_height() + 10
    surface.blit(speed_surface, (center_x - speed_surface.get_width()//2, text_y))
    text_y += speed_surface.get_height() + 10
    surface.blit(time_surface, (center_x - time_surface.get_width()//2, text_y))

def draw_promotion_menu(surface, board, square_size):
    """Draw the pawn promotion menu with animations"""
    if not board.promotion_pending:
        return None
    
    # Calculate menu position
    file = chess.square_file(board.promotion_square)
    rank = chess.square_rank(board.promotion_square)
    is_white = board.board.turn == chess.WHITE
    
    # Menu dimensions
    menu_width = square_size * 4
    menu_height = square_size * 2
    menu_x = file * square_size - (menu_width - square_size) // 2
    menu_y = rank * square_size - menu_height if is_white else rank * square_size + square_size
    
    # Ensure menu stays within screen bounds
    menu_x = max(0, min(menu_x, SCREEN_WIDTH - menu_width))
    menu_y = max(0, min(menu_y, SCREEN_HEIGHT - menu_height))
    
    # Draw semi-transparent overlay with fade-in animation
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    alpha = min(128, int(128 * (time.time() - board.promotion_start_time) / PROMOTION_ANIMATION_SPEED))
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))
    
    # Draw menu background with slide-in animation
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    draw_rounded_rect(surface, PROMOTION_MENU_COLOR, menu_rect, 10, PROMOTION_MENU_BORDER, 2)
    
    # Draw promotion message with fade-in
    message_surface = info_font.render(PROMOTION_MESSAGE, True, PROMOTION_TEXT)
    message_x = menu_x + (menu_width - message_surface.get_width()) // 2
    message_y = menu_y + 10
    surface.blit(message_surface, (message_x, message_y))
    
    # Store piece rectangles for click detection
    piece_rects = []
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw promotion options with hover animations
    pieces = ['q', 'r', 'b', 'n']
    piece_names = ['Queen', 'Rook', 'Bishop', 'Knight']
    
    for i, (piece, name) in enumerate(zip(pieces, piece_names)):
        # Create clickable area - make it larger for better clickability
        piece_rect = pygame.Rect(
            menu_x + i * square_size,
            menu_y + square_size // 2,
            square_size,
            square_size
        )
        piece_rects.append((piece_rect, piece))
        
        # Check for hover
        is_hovered = piece_rect.collidepoint(mouse_pos)
        
        # Calculate hover animation
        hover_scale = 1.0
        if is_hovered:
            hover_scale = PROMOTION_HOVER_SCALE
        
        # Draw piece background with hover effect
        if is_hovered:
            s = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            pygame.draw.rect(s, PROMOTION_HIGHLIGHT, (0, 0, square_size, square_size), border_radius=5)
            surface.blit(s, (piece_rect.x, piece_rect.y))
        
        # Draw piece with scale animation
        color = 'white' if is_white else 'black'
        piece_str = f"{color}_{piece}"
        
        # Calculate scaled position for hover effect
        scaled_size = int(square_size * hover_scale)
        offset_x = (scaled_size - square_size) // 2
        offset_y = (scaled_size - square_size) // 2
        
        # Create a surface for the scaled piece
        piece_surface = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)
        draw_piece(piece_surface, piece_str, 0, 0, scaled_size)
        surface.blit(piece_surface, (piece_rect.x - offset_x, piece_rect.y - offset_y))
        
        # Draw piece name with fade-in
        name_surface = info_font.render(name, True, PROMOTION_TEXT)
        name_x = piece_rect.x + (square_size - name_surface.get_width()) // 2
        name_y = piece_rect.y + square_size - 20
        surface.blit(name_surface, (name_x, name_y))
    
    return piece_rects

def show_error_message(message):
    """Show an error message for a short duration"""
    global error_message, error_message_time
    error_message = message
    error_message_time = time.time()

def draw_error_message(surface):
    """Draw the error message if it exists and hasn't expired"""
    global error_message, error_message_time
    
    if not error_message:
        return
    
    current_time = time.time()
    if current_time - error_message_time > ERROR_MESSAGE_DURATION:
        error_message = ""
        return
    
    # Calculate message position (center of the board)
    message_surface = info_font.render(error_message, True, ERROR_MESSAGE_COLOR)
    message_x = (BOARD_WIDTH - message_surface.get_width()) // 2
    message_y = BOARD_WIDTH // 2
    
    # Draw semi-transparent background
    bg_rect = pygame.Rect(
        message_x - 20,
        message_y - 10,
        message_surface.get_width() + 40,
        message_surface.get_height() + 20
    )
    s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    surface.blit(s, (bg_rect.x, bg_rect.y))
    
    # Draw message
    surface.blit(message_surface, (message_x, message_y))

# Add sound generation
def generate_sound(frequency, duration, volume=0.3):
    """Generate a simple stereo sound effect programmatically"""
    sample_rate = 44100
    t = numpy.linspace(0, duration, int(sample_rate * duration), False)
    tone = numpy.sin(frequency * t * 2 * numpy.pi)
    # Create stereo by duplicating the mono channel and ensure C-contiguous
    stereo_tone = numpy.vstack((tone, tone)).T.copy()  # Add .copy() to ensure C-contiguous
    stereo_tone = numpy.int16(stereo_tone * 32767 * volume)
    return pygame.sndarray.make_sound(stereo_tone)

# Initialize sound effects with fallback to generated sounds
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2)  # Initialize mixer for stereo
    SOUNDS = {
        'move': pygame.mixer.Sound('sounds/move.wav'),
        'capture': pygame.mixer.Sound('sounds/capture.wav'),
        'check': pygame.mixer.Sound('sounds/notify.wav'),
        'promotion': pygame.mixer.Sound('sounds/notify.wav'),
        'game_over': pygame.mixer.Sound('sounds/notify.wav'),
        'button_click': pygame.mixer.Sound('sounds/notify.wav')
    }
except FileNotFoundError:
    print("Sound files not found. Generating simple sound effects...")
    import numpy
    pygame.mixer.init(frequency=44100, size=-16, channels=2)  # Initialize mixer for stereo
    SOUNDS = {
        'move': generate_sound(440, 0.1),  # A4 note
        'capture': generate_sound(880, 0.2),  # A5 note
        'check': generate_sound(660, 0.3),  # E5 note
        'promotion': generate_sound(880, 0.4),  # A5 note
        'game_over': generate_sound(220, 0.5),  # A3 note
        'button_click': generate_sound(330, 0.1)  # E4 note
    }

# Add particle effects
class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.age = 0

    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.age += dt
        return self.age < self.lifetime

    def draw(self, surface):
        alpha = int(255 * (1 - self.age / self.lifetime))
        color = (*self.color[:3], alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 3)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.uniform(0.5, 1.0)
            self.particles.append(Particle(x, y, color, velocity, lifetime))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

# Add tooltip system
class Tooltip:
    def __init__(self):
        self.text = ""
        self.visible = False
        self.position = (0, 0)
        self.delay = 0.5
        self.timer = 0

    def show(self, text, position):
        self.text = text
        self.position = position
        self.visible = True
        self.timer = 0

    def hide(self):
        self.visible = False
        self.timer = 0

    def update(self, dt):
        if self.visible:
            self.timer += dt
            if self.timer < self.delay:
                self.visible = False

    def draw(self, surface):
        if not self.visible or self.timer < self.delay:
            return

        # Draw tooltip background
        text_surface = info_font.render(self.text, True, TEXT_COLOR)
        padding = 10
        rect = pygame.Rect(
            self.position[0],
            self.position[1] - text_surface.get_height() - padding * 2,
            text_surface.get_width() + padding * 2,
            text_surface.get_height() + padding * 2
        )

        # Draw shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        draw_rounded_rect(surface, (0, 0, 0, 100), shadow_rect, 5, None, 0)

        # Draw tooltip
        draw_rounded_rect(surface, THEME['dark']['panel'], rect, 5, THEME['dark']['border'], 1)
        surface.blit(text_surface, (rect.x + padding, rect.y + padding))

# Add layout constants
class UILayout:
    def __init__(self, screen_width, screen_height, board_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_width = board_width
        self.side_panel_width = screen_width - board_width
        
        # Calculate section heights
        self.header_height = 60
        self.controls_height = 200
        self.game_info_height = 200
        self.move_history_height = 300
        self.footer_height = 60
        
        # Calculate section positions
        self.header_y = 0
        self.controls_y = self.header_y + self.header_height
        self.game_info_y = self.controls_y + self.controls_height
        self.move_history_y = self.game_info_y + self.game_info_height
        self.footer_y = self.move_history_y + self.move_history_height
        
        # Calculate element spacing
        self.padding = 15
        self.element_spacing = 10
        self.section_spacing = 20

def main():
    global SCREEN_WIDTH, SQUARE_SIZE, SIDE_PANEL_WIDTH, board, info_modal_active
    
    board = ChessBoard()
    selected_square = None
    clock = pygame.time.Clock()
    last_update_time = 0
    update_interval = 0.1
    info_modal_active = False
    
    print("Game started. Window size:", SCREEN_WIDTH, "x", SCREEN_HEIGHT)
    print("\nScoring System:")
    print("Pawn: 1 point")
    print("Knight: 3 points")
    print("Bishop: 3 points")
    print("Rook: 5 points")
    print("Queen: 9 points")
    print("\nObjective: Score the most points in 12 moves by capturing high-value pieces!")
    
    # Force initial suggestion update
    board.update_suggested_moves()
    
    try:
        # Initialize UI with layout
        layout = UILayout(SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_WIDTH)
        game_ui = GameUI(layout)
        
        # Set initial toggle states
        game_ui.toggles[2].is_on = board.engine_enabled  # Engine toggle
        
        running = True
        while running:
            current_time = time.time()
            mouse_pos = pygame.mouse.get_pos()
            
            # Update UI
            game_ui.update(mouse_pos)
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Auto-play best moves for 6 moves when 'A' is pressed
                    elif event.key == pygame.K_a:
                        auto_play_best_moves(board, n=6)
                        board.update_suggested_moves()
                
                # Handle mouse clicks
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    # Check info modal close button first
                    if info_modal_active:
                        close_button_rect = draw_info_modal(screen)
                        if close_button_rect and close_button_rect.collidepoint(mouse_pos):
                            info_modal_active = False
                            continue
                    
                    # Check promotion menu first
                    if board.promotion_pending:
                        # Calculate menu position
                        file = chess.square_file(board.promotion_square)
                        rank = chess.square_rank(board.promotion_square)
                        is_white = board.board.turn == chess.WHITE
                        
                        # Menu dimensions
                        menu_width = SQUARE_SIZE * 4
                        menu_height = SQUARE_SIZE * 2
                        menu_x = file * SQUARE_SIZE - (menu_width - SQUARE_SIZE) // 2
                        menu_y = rank * SQUARE_SIZE - menu_height if is_white else rank * SQUARE_SIZE + SQUARE_SIZE
                        
                        # Ensure menu stays within screen bounds
                        menu_x = max(0, min(menu_x, SCREEN_WIDTH - menu_width))
                        menu_y = max(0, min(menu_y, SCREEN_HEIGHT - menu_height))
                        
                        # Check if click is within menu bounds
                        if menu_x <= mouse_pos[0] <= menu_x + menu_width and \
                           menu_y <= mouse_pos[1] <= menu_y + menu_height:
                            # Calculate which piece was clicked
                            piece_index = (mouse_pos[0] - menu_x) // SQUARE_SIZE
                            if 0 <= piece_index < 4:
                                pieces = ['q', 'r', 'b', 'n']
                                clicked_piece = pieces[piece_index]
                                
                                # Complete the promotion move
                                success, error_message = board.make_move(
                                    board.promotion_from_square,
                                    board.promotion_square,
                                    clicked_piece
                                )
                                if success:
                                    print(f"Promoted to {clicked_piece.upper()}")
                                    board.promotion_pending = False
                                    board.promotion_square = None
                                    board.promotion_from_square = None
                                    selected_square = None
                                    board.update_suggested_moves()
                                else:
                                    show_error_message(error_message)
                        else:
                            # Clicked outside menu - cancel promotion
                            board.promotion_pending = False
                            board.promotion_square = None
                            board.promotion_from_square = None
                            selected_square = None
                    # Not in promotion menu, check other UI elements
                    elif any(toggle.rect.collidepoint(mouse_pos) for toggle in game_ui.toggles):
                        for i, toggle in enumerate(game_ui.toggles):
                            if toggle.rect.collidepoint(mouse_pos):
                                if toggle.toggle():
                                    if i == 0:  # Side toggle
                                        board.target_side = 'black' if board.target_side == 'white' else 'white'
                                        toggle.text = f"Target Side: {board.target_side.capitalize()}"
                                    elif i == 1:  # Move limit toggle
                                        board.toggle_move_limit()
                                        toggle.text = "12-Move Limit: ON" if board.move_limit_enabled else "12-Move Limit: OFF"
                                    elif i == 2:  # Engine toggle
                                        board.toggle_engine()
                                        toggle.text = "Engine Analysis: ON" if board.engine_enabled else "Engine Analysis: OFF"
                                    elif i == 3:  # Sound toggle
                                        # Handle sound toggle
                                        pass
                                    elif i == 4:  # Theme toggle
                                        game_ui.toggle_theme()
                                        toggle.text = "Dark Mode: ON" if game_ui.theme == THEME['dark'] else "Dark Mode: OFF"
                                board.update_suggested_moves()
                                break
                    # Handle board clicks
                    elif mouse_pos[0] < BOARD_WIDTH:  # Only check board area
                        board_y = mouse_pos[1] // SQUARE_SIZE
                        board_x = mouse_pos[0] // SQUARE_SIZE
                        if 0 <= board_x < 8 and 0 <= board_y < 8:
                            clicked_square = coords_to_square(board_x, board_y)
                            
                            # Get the piece at the clicked square
                            piece = board.get_piece_at(clicked_square)
                            
                            # If no piece is selected yet, select one
                            if selected_square is None:
                                if piece:
                                    # Check if it's the correct player's turn
                                    piece_color = 'white' if piece.startswith('white') else 'black'
                                    if piece_color == 'white' and not board.board.turn:
                                        show_error_message("It's Black's turn!")
                                    elif piece_color == 'black' and board.board.turn:
                                        show_error_message("It's White's turn!")
                                    else:
                                        selected_square = clicked_square
                                        print(f"Selected piece at {chess.square_name(clicked_square)}")
                                else:
                                    show_error_message("No piece to select!")
                            else:
                                # Try to make the move
                                success, error_message = board.make_move(selected_square, clicked_square)
                                if success:
                                    print(f"Made move from {chess.square_name(selected_square)} to {chess.square_name(clicked_square)}")
                                    board.update_suggested_moves()
                                else:
                                    show_error_message(error_message)
                                    print(f"Illegal move: {chess.square_name(selected_square)} to {chess.square_name(clicked_square)}")
                                # Always clear selection after attempting a move
                                selected_square = None
            
            # Update suggestions periodically
            if current_time - last_update_time >= update_interval:
                board.update_suggested_moves()
                last_update_time = current_time
            
            # Draw everything
            screen.fill(BACKGROUND)
            
            # Draw chess board with pieces and highlights
            draw_board(screen, board, selected_square, SQUARE_SIZE)
            
            # Draw suggested moves with arrows
            draw_suggested_moves(screen, board, SQUARE_SIZE)
            
            # Draw promotion menu if needed
            promotion_menu_rect = draw_promotion_menu(screen, board, SQUARE_SIZE)
            
            # Draw loading overlay if analyzing
            draw_loading_overlay(screen, board)
            
            # Draw error message if any
            draw_error_message(screen)
            
            # Draw info modal if active
            if info_modal_active:
                draw_info_modal(screen)
            
            # Draw UI
            game_ui.draw(screen)
            
            # Update the display
            pygame.display.flip()
            clock.tick(60)
    
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        cleanup()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        cleanup() 