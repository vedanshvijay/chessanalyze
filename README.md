# Chess Capture Challenge

**Developed by Vedansh Vijay Vargia**  
[LinkedIn](https://www.linkedin.com/in/vedansh-vijayvargia-41a64421b/) | [GitHub](https://github.com/vedanshvijay/vedanshvijay)

*Experience a dynamic and interactive chess journey! Click around, explore move suggestions, and dive into real-time analysis as you challenge your chess skills.*

## Features

- 🎮 **Interactive Chess Board**: Engage with a modern UI that allows you to click and move pieces seamlessly.
- 🤖 **Real-time Move Analysis**: Utilize the Stockfish engine for instant feedback on your moves.
- 📊 **Move Suggestions**: Get detailed explanations for suggested moves, helping you learn and improve your strategy.
- 🎯 **Point-based Scoring System**: Capture pieces to score points based on their value.
- ⚡ **Fast and Responsive Gameplay**: Enjoy smooth interactions and quick responses to your actions.
- 🎨 **Beautiful Modern Interface**: A visually appealing design that enhances your gaming experience.
- 📱 **Responsive Design**: The game adapts to different screen sizes for optimal play on any device.
- 🔍 **Visual Move Indicators**: Arrows and highlights show you the best moves and capture opportunities.
- 👑 **Full Chess Rules Support**: Including:
  - Pawn promotion
  - Castling
  - En passant
  - All standard chess moves

## Interactive Components

### Move Suggestions
- As you play, the game provides real-time suggestions for your next moves based on the current board state. 
- Each suggestion comes with a detailed explanation, helping you understand the reasoning behind the recommended moves.

### Real-time Analysis
- The Stockfish engine analyzes your moves and provides feedback on the position, including potential threats and opportunities.
- You can see how your moves affect the game and learn from the analysis to improve your skills.

### User Engagement
- The game encourages exploration by allowing you to click on pieces to see valid moves and potential captures.
- Interactive toggles let you customize your experience, such as enabling/disabling sound effects or switching between light and dark themes.

## Technical Stack

### Core Technologies
- **Python 3.x**: Main programming language
- **Pygame**: Game development and graphics
- **python-chess**: Chess logic and move validation
- **Stockfish**: Chess engine for move analysis

### Key Libraries
- `pygame`: For graphics and user interface
- `chess`: For chess logic and move validation
- `chess.engine`: For integration with Stockfish
- `math`: For calculations and animations
- `time`: For timing and animations
- `sys`: For system operations
- `os`: For file and path operations
- `subprocess`: For clipboard operations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chess-capture-challenge.git
cd chess-capture-challenge
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Stockfish:
- **macOS**: `brew install stockfish`
- **Linux**: `sudo apt-get install stockfish`
- **Windows**: Download from [Stockfish website](https://stockfishchess.org/download/)

## Game Rules

### Scoring System
- Pawn: 1 point
- Knight: 3 points
- Bishop: 3 points
- Rook: 5 points
- Queen: 9 points
- King: Not counted in scoring

### Game Modes
1. **12-Move Challenge**: Score as many points as possible in 12 moves.
2. **Unlimited Mode**: Play without move restrictions.

## Controls

- **Mouse**: Click to select and move pieces.
- **A Key**: Auto-play best moves for 6 turns.
- **Escape**: Quit game.
- **FEN Input**: Paste FEN string to load custom positions.

## Features in Detail

### Move Analysis
- Real-time position evaluation.
- Best move suggestions with detailed explanations.
- Capture opportunities highlighted.
- Strategic move recommendations.

### UI Elements
- Interactive chess board with responsive design.
- Side panel with game information and controls.
- Move suggestion box with visual indicators.
- Loading overlay during analysis.
- Promotion menu for pawn promotions.
- Score display and move counter.

### Visual Indicators
- Legal move highlights.
- Suggested move arrows.
- Capture indicators.
- Check highlights.
- Promotion prompts.

## Development

### Project Structure
```
chess-capture-challenge/
├── chess_game.py      # Main game file
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

### Key Components
1. **ChessBoard Class**: Core game logic.
2. **UI Components**: Drawing functions and interactive elements.
3. **Move Analysis**: Engine integration for real-time feedback.
4. **Event Handling**: User input processing and interaction management.

## Performance Optimization

- Move caching for faster response.
- Optimized engine settings for efficient analysis.
- Efficient rendering for smooth gameplay.
- Responsive design for various screen sizes.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Stockfish chess engine.
- python-chess library.
- Pygame community.

## GitHub Features

- ⚙️ Continuous Integration with GitHub Actions for automatic testing.
- 🛠️ Issue tracking and pull request templates to streamline contributions.
- 📦 GitHub Packages for dependency and release management.
- 🔒 Automated security and code scanning tools integrated via GitHub.
- 🚀 GitHub Pages for hosting project documentation and demos.