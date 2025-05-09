import pygame
import sys
import chess
import chess.engine
import os
from pathlib import Path
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
WHITE = (240, 240, 240)  # Lighter white
BLACK = (75, 115, 153)   # Nice blue-gray
HIGHLIGHT = (124, 252, 0, 180)  # Brighter green
MOVE_HIGHLIGHT = (0, 255, 0, 180)  # Brighter move highlight
CHECK_HIGHLIGHT = (255, 50, 50, 180)  # Brighter red
BEST_MOVE_HIGHLIGHT = (30, 144, 255, 180)  # Brighter blue
INPUT_BOX_HEIGHT = 80  # Taller input box
INFO_HEIGHT = 160  # More space for info
TOTAL_HEIGHT = WINDOW_SIZE + INPUT_BOX_HEIGHT + INFO_HEIGHT

# Colors for UI
LIGHT_BLUE = (200, 220, 255)
DARK_BLUE = (100, 150, 200)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Piece values
PIECE_VALUES = {
    'p': 1,  # pawn
    'n': 3,  # knight
    'b': 3,  # bishop
    'r': 5,  # rook
    'q': 9,  # queen
    'k': 0   # king (not counted in scoring)
}

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, TOTAL_HEIGHT))
pygame.display.set_caption("Chess Capture Challenge")

# Input box properties
input_box = pygame.Rect(10, 10, WINDOW_SIZE - 20, INPUT_BOX_HEIGHT - 20)
input_text = ""
input_active = False
input_font = pygame.font.SysFont('Arial', 32)
input_placeholder = "Click here and Command+V to paste FEN string, then press Enter"

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        self.engine = None
        self.best_move = None
        self.evaluation = None
        self.initialize_engine()
        self.moves_made = 0
        self.max_moves = 12  # Increased to 12 moves
        self.white_score = 0
        self.black_score = 0
        self.last_capture = None
        self.game_over = False
        self.winner = None
    
    def initialize_engine(self):
        try:
            stockfish_path = "/opt/homebrew/bin/stockfish"
            if not os.path.exists(stockfish_path):
                stockfish_path = "stockfish"
            
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            self.engine.configure({"Threads": 2, "Hash": 128})
            print("Stockfish engine initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Stockfish: {e}")
            self.engine = None
    
    def analyze_position(self):
        if not self.engine:
            return
        
        try:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
            self.best_move = info["pv"][0] if "pv" in info else None
            
            score = info.get("score", None)
            if score:
                if score.is_mate():
                    self.evaluation = f"Mate in {score.mate()}"
                else:
                    try:
                        eval_pawns = score.white().score() / 100.0
                        self.evaluation = f"{eval_pawns:+.1f}"
                    except:
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
            self.analyze_position()
            return True
        except:
            return False
    
    def get_valid_moves(self, square):
        if self.moves_made >= self.max_moves:
            return []
        
        moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                # Allow both capturing and non-capturing moves
                moves.append(move.to_square)
        return moves
    
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
    
    def make_move(self, from_square, to_square):
        if self.game_over or self.moves_made >= self.max_moves:
            return False
        
        move = chess.Move(from_square, to_square)
        if move in self.board.legal_moves:
            # Check if it's a capture move
            if self.board.is_capture(move):
                captured_piece = self.board.piece_at(to_square)
                if captured_piece:
                    piece_value = PIECE_VALUES.get(captured_piece.symbol().lower(), 0)
                    if self.board.turn:  # White's turn
                        self.white_score += piece_value
                        print(f"White captured {captured_piece.symbol()} worth {piece_value} points!")
                    else:
                        self.black_score += piece_value
                        print(f"Black captured {captured_piece.symbol()} worth {piece_value} points!")
                    self.last_capture = (captured_piece.symbol(), piece_value)
            
            self.board.push(move)
            self.moves_made += 1
            self.analyze_position()
            self.check_game_over()
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

def draw_piece(surface, piece, x, y):
    if not piece:
        return
    
    color = SILVER if piece.startswith('white') else DARK_BLUE
    piece_type = piece.split('_')[1]
    
    # Draw a larger circle for the piece
    radius = int(SQUARE_SIZE * 0.4)  # Increased size
    pygame.draw.circle(surface, color, (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), radius)
    
    # Draw piece letter with larger font
    font = pygame.font.SysFont('Arial Bold', int(SQUARE_SIZE * 0.6))  # Larger font
    text = font.render(piece_type.upper(), True, WHITE if color == DARK_BLUE else BLACK)
    text_rect = text.get_rect(center=(x + SQUARE_SIZE//2, y + SQUARE_SIZE//2))
    surface.blit(text, text_rect)

def get_clipboard_content():
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Error getting clipboard content: {e}")
    return ""

def main():
    board = ChessBoard()
    selected_square = None
    clock = pygame.time.Clock()
    input_text = ""
    input_active = False
    
    # Create fonts
    title_font = pygame.font.SysFont('Arial Bold', 32)
    info_font = pygame.font.SysFont('Arial', 28)
    score_font = pygame.font.SysFont('Arial Bold', 36)
    coord_font = pygame.font.SysFont('Arial', 20)  # Added coordinate font
    
    print("Game started. Window size:", WINDOW_SIZE)
    print("\nScoring System:")
    print("Pawn: 1 point")
    print("Knight: 3 points")
    print("Bishop: 3 points")
    print("Rook: 5 points")
    print("Queen: 9 points")
    print("\nObjective: Score the most points in 12 moves by capturing high-value pieces!")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if input_box.collidepoint(x, y):
                    input_active = True
                    print("Input box activated - use Command+V to paste")
                else:
                    input_active = False
                
                if INPUT_BOX_HEIGHT <= y < WINDOW_SIZE + INPUT_BOX_HEIGHT:
                    board_y = (y - INPUT_BOX_HEIGHT) // SQUARE_SIZE
                    board_x = x // SQUARE_SIZE
                    clicked_square = coords_to_square(board_x, board_y)
                    
                    if selected_square is None:
                        if board.get_piece_at(clicked_square):
                            selected_square = clicked_square
                            print(f"Selected square: {chess.square_name(selected_square)}")
                    else:
                        if clicked_square in board.get_valid_moves(selected_square):
                            board.make_move(selected_square, clicked_square)
                            print(f"Move made: {chess.square_name(selected_square)} -> {chess.square_name(clicked_square)}")
                        selected_square = None
            
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip():
                            if board.set_from_fen(input_text.strip()):
                                print(f"Board set from FEN: {input_text}")
                            else:
                                print("Invalid FEN string")
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_META):
                        clipboard_text = get_clipboard_content()
                        if clipboard_text:
                            input_text = clipboard_text
                            print(f"Pasted text: {input_text}")
                    else:
                        if event.unicode.isprintable():
                            input_text += event.unicode
        
        screen.fill(WHITE)
        
        # Draw input box with better styling
        if input_active:
            box_color = LIGHT_BLUE
        else:
            box_color = (220, 220, 220)
        
        pygame.draw.rect(screen, box_color, input_box)
        pygame.draw.rect(screen, DARK_BLUE, input_box, 3)  # Thicker border
        
        if input_text:
            text_surface = title_font.render(input_text, True, (0, 0, 0))
        else:
            text_surface = info_font.render(input_placeholder, True, (150, 150, 150))
        
        text_y = input_box.y + (input_box.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (input_box.x + 10, text_y))
        
        # Draw the board with improved visuals
        for rank in range(BOARD_SIZE):
            for file in range(BOARD_SIZE):
                square = coords_to_square(file, rank)
                color = WHITE if (rank + file) % 2 == 0 else BLACK
                rect = pygame.Rect(
                    file * SQUARE_SIZE,
                    rank * SQUARE_SIZE + INPUT_BOX_HEIGHT,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                pygame.draw.rect(screen, color, rect)
                
                # Draw coordinates
                if rank == 7:  # Draw file letters
                    coord_font = pygame.font.SysFont('Arial', 20)
                    file_text = coord_font.render(chr(file + 97), True, BLACK if color == WHITE else WHITE)
                    screen.blit(file_text, (file * SQUARE_SIZE + 5, rank * SQUARE_SIZE + INPUT_BOX_HEIGHT + SQUARE_SIZE - 25))
                if file == 0:  # Draw rank numbers
                    rank_text = coord_font.render(str(8 - rank), True, BLACK if color == WHITE else WHITE)
                    screen.blit(rank_text, (5, rank * SQUARE_SIZE + INPUT_BOX_HEIGHT + 5))
                
                if selected_square == square:
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(s, HIGHLIGHT, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(s, (file * SQUARE_SIZE, rank * SQUARE_SIZE + INPUT_BOX_HEIGHT))
                
                if selected_square and square in board.get_valid_moves(selected_square):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(s, MOVE_HIGHLIGHT, (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//4)
                    screen.blit(s, (file * SQUARE_SIZE, rank * SQUARE_SIZE + INPUT_BOX_HEIGHT))
                
                if board.best_move and (
                    square == board.best_move.from_square or 
                    square == board.best_move.to_square
                ):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(s, BEST_MOVE_HIGHLIGHT, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(s, (file * SQUARE_SIZE, rank * SQUARE_SIZE + INPUT_BOX_HEIGHT))
                
                piece = board.get_piece_at(square)
                if piece:
                    draw_piece(screen, piece, file * SQUARE_SIZE, rank * SQUARE_SIZE + INPUT_BOX_HEIGHT)
        
        # Draw game info with improved styling
        if not board.game_over:
            turn_text = "Current Turn: White" if board.board.turn else "Current Turn: Black"
            moves_text = f"Moves: {board.moves_made}/{board.max_moves}"
        else:
            if board.winner == "Draw":
                turn_text = "Game Over - It's a Draw!"
            else:
                turn_text = f"Game Over - {board.winner} Wins!"
            moves_text = "Final Score"
        
        white_score_text = f"White: {board.white_score} points"
        black_score_text = f"Black: {board.black_score} points"
        
        if board.last_capture:
            last_capture_text = f"Last Capture: {board.last_capture[0]} (+{board.last_capture[1]} pts)"
        else:
            last_capture_text = "No captures yet"
        
        if not board.game_over:
            remaining_text = f"Remaining: {board.max_moves - board.moves_made} moves"
        else:
            remaining_text = "Game Over!"
        
        # Draw info with new fonts and colors
        y_offset = WINDOW_SIZE + INPUT_BOX_HEIGHT + 20
        
        turn_surface = title_font.render(turn_text, True, DARK_BLUE)
        moves_surface = info_font.render(moves_text, True, (0, 0, 0))
        white_score_surface = score_font.render(white_score_text, True, DARK_BLUE)
        black_score_surface = score_font.render(black_score_text, True, DARK_BLUE)
        last_capture_surface = info_font.render(last_capture_text, True, (0, 0, 0))
        remaining_surface = title_font.render(remaining_text, True, DARK_BLUE)
        
        # Draw info with better spacing
        screen.blit(turn_surface, (20, y_offset))
        screen.blit(moves_surface, (20, y_offset + 40))
        screen.blit(white_score_surface, (20, y_offset + 80))
        screen.blit(black_score_surface, (20, y_offset + 120))
        screen.blit(remaining_surface, (WINDOW_SIZE//2 + 20, y_offset))
        screen.blit(last_capture_surface, (WINDOW_SIZE//2 + 20, y_offset + 80))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 