import numpy as np

class ChessGame:
    """A simple text-based prototype for a Chess Game."""

    def __init__(self):
        # Initialize the board using NumPy for easy array handling (8 rows, 8 columns)
        # The standard notation is used: 'R'='White Rook', 'p'='Black pawn'.
        self.board = np.array([
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], # Black pieces (Row 0)
            ['p', 'p', 'p', 'p', '_', 'p', 'p', 'p'], # Black Pawns (Row 1)
            ['_', '_', '_', '_', '_', '_', '_', '_'], # Empty Row 2
            ['_', '_', '_', '_', '_', '_', '_', '_'], # Empty Row 3
            ['_', '_', '_', '_', '_', '_', '_', '_'], # Empty Row 4
            ['_', '_', '_', '_', '_', '_', '_', '_'], # Empty Row 5
            ['P', 'P', 'P', 'P', '_', 'P', 'P', 'P'], # White Pawns (Row 6)
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']  # White pieces (Row 7)
        ])
        self.current_player = 'White' # Starts with White

    def display_board(self):
        """Prints the current state of the board using a readable format."""
        print("\n" + "=" * 30)
        print("          CHESS BOARD")
        print("-" * 32)
        
        # Print column headers (A-H)
        header = "  " + " ".join([chr(ord('A') + i - 1) for i in range(1, 9)])
        print(f"{header}")

        for i, row in enumerate(self.board):
            # Row number (8-1 is the highest printed row index)
            row_num = 8 - i
            row_display = f"{row_num:2d} " + " ".join(list(row))
            print(f"{row_display}")
        
        print("-" * 32)
        print("Current Player:", self.current_player)

    def get_coords(self, algebraic):
        """Converts standard algebraic notation (e.g., 'A1') to array indices (row, col)."""
        if len(algebraic) != 2:
            return None # Invalid format
        
        col_char = algebraic[0].upper()
        row_str = algebraic[1]

        # Column calculation: A=0, B=1, ... H=7
        col = ord(col_char) - ord('A')
        
        # Row calculation: 8 (top) to 1 (bottom). Since array index 0 is the top row (Row 8),
        # we use 8 - int(row_str) for the correct index.
        row = 8 - int(row_str)
        
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None

    def get_move_input(self):
        """Prompts the user for a move in standard algebraic notation (e.g., 'A2 A4')."""
        while True:
            print("\nEnter move format (e.g., StartSquare EndSquare) or 'quit':")
            user_input = input("> ").strip().upper()
            if user_input == 'QUIT':
                return None, None
            
            try:
                start_sq, end_sq = user_input.split()
                return start_sq, end_sq
            except ValueError:
                print("Invalid format. Please enter two squares (e.g., A2 B4).")

    def make_move(self, start_square, end_square):
        """Attempts to move a piece from one square to another."""
        start_pos = self.get_coords(start_square)
        end_pos = self.get_coords(end_square)

        if not start_pos or not end_pos:
            print("Error: One or both squares are invalid.")
            return False

        # Unpack coordinates for clarity
        r1, c1 = start_pos 
        r2, c2 = end_pos

        piece = self.board[r1, c1]
        target_piece = self.board[r2, c2]

        if piece == '_':
            print("Error: No piece found at the starting square.")
            return False
        
        # --- CORE LOGIC CHECK (Placeholder for Rule Validation) ---
        
        # 1. Check if it's the current player's turn and they own the piece.
        is_white = 'A' <= start_square[0] or 'a' <= start_square[0] # Simple check proxy
        if self.current_player == 'White':
            # White pieces are uppercase (P, R, N...)
            if not ('A' <= piece <= 'Z'): 
                print("Error: It is White's turn, but the piece belongs to Black.")
                return False
        else: # Assuming 'Black' for simplicity here
            # Black pieces are lowercase (p, r, n...)
            if not ('a' <= piece <= 'z'):
                 print("Error: It is Black's turn, but the piece belongs to White.")
                 return False

        # 2. Check if the target square is occupied by a friendly piece.
        is_friendly_attack = (self.current_player == 'White' and ('A' <= target_piece <= 'Z')) or \
                              (self.current_player == 'Black' and ('a' <= target_piece <= 'z'))

        if is_friendly_attack:
            print("Illegal Move: You cannot capture your own piece!")
            return False

        # 3. *** THIS IS WHERE THE COMPLEX CHESS RULES GO ***
        # (e.g., Is the Rook moving correctly? Did the Knight jump over other pieces?)
        if not self._validate_move(piece, r1, c1, r2, c2):
            print("Illegal Move: That piece cannot move that way.")
            return False
        
        # --- EXECUTE MOVE (If all checks pass) ---
        self.board[r2, c2] = piece # Place the piece on the new square
        self.board[r1, c1] = '_'  # Clear the old square

        print(f"\n✅ Move successful: {piece} moved from {start_square} to {end_square}.")

        # Switch player and check for game end (Checkmate/Stalemate)
        self.current_player = 'Black' if self.current_player == 'White' else 'White'
        return True


    def _validate_move(self, piece, r1, c1, r2, c2):
        """
        A placeholder function for all specific chess rules. 
        For simplicity, this currently accepts almost any move that doesn't violate friendly pieces.
        *You MUST expand this function to make the game playable.*
        """
        # Example: If we wanted a Knight check (L-shape):
        # delta_r = abs(r1 - r2)
        # delta_c = abs(c1 - c2)
        # if piece.lower() == 'n':
        #     if not ((delta_r == 2 and delta_c == 1) or (delta_r == 1 and delta_c == 2)):
        #         return False
        
        # For the prototype, we assume basic movement is allowed if the piece is present.
        return True


    def run(self):
        """The main game loop."""
        print("===========================================")
        print("Welcome to Simple Command-Line Chess!")
        print("To play, enter moves like 'A2 A4' (Start Square End Square).")
        print("Note: This is a prototype. Rules for specific pieces are simplified.")
        print("Type 'quit' at any time to exit.\n")

        while True:
            self.display_board()
            start_sq, end_sq = self.get_move_input()

            if start_sq is None:
                print("\nGame ended by user.")
                break
            
            # Attempt the move and proceed to the next turn if successful
            move_successful = self.make_move(start_sq, end_sq)

            if not move_successful:
                 # If the move failed (due to rule violation or invalid input), 
                 # we do NOT switch players, allowing the user to try again.
                pass


# --- RUN THE GAME ---
if __name__ == "__main__":
    game = ChessGame()
    game.run()

