import pygame
import chess
import sys

from node import Node
import threading

speed = 60

white = (255, 255, 255)
yellow = (235, 236, 208)
green = (119, 149, 86)
black = (0, 0, 0)
blue = (50, 80, 160, 150)

class ChessView:
    def __init__(self, board, player, ai, width, height):
        self.width = width
        self.height = height
        self.size = self.width // 8
        self.running = False
        self.result = False
        self.dragging = None
        self.board = board 
        self.player = player
        self.ai = ai
        self.valid_moves = {}  # Dictionary to store valid moves for a selected piece
        self.board = board
        self.thread = None

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Chess AI')
        self.screen = pygame.display.set_mode((width, height)) 
        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self.font = pygame.font.SysFont("Georgia", 20)

        # Load images into a dictionary
        self.piece_images = {}
        self.load_piece_images()

    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()

            if not self.board.turn == self.player:
                if self.thread is None:
                    self.thread = threading.Thread(target=self.ai_turn)
                    self.thread.start()

        pygame.quit()
        sys.exit()

    def ai_turn(self):
        if not (self.board.is_game_over() or self.board.turn == self.player):
            root = Node(self.board)
            best_move = self.ai.predict(root, iterations=1000, minimax=True)
            self.board.push(best_move) 
            print("AI played:", best_move)
            self.thread = None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.handle_mouse_up(event.pos)

        if not self.result and self.board.is_game_over():
            print("Game Over!") 
            result = self.board.result() 
            print(result)  # Print the game result (1-0, 0-1, or 1/2-1/2)
            self.result = True

    def draw(self):
        self.screen.fill(black)
        self.draw_board()
        self.draw_pieces()
        if self.dragging:
            self.highlight_valid_moves()

    def update(self):
        pygame.display.update()
        self.clock.tick(speed)

    def draw_board(self):
        # Draw the chess board
        for row in range(8):
            for col in range(8):
                square_color = yellow if (row + col) % 2 == 0 else green
                pygame.draw.rect(self.screen, square_color, (col * self.size, row * self.size, self.size, self.size))

    def draw_pieces(self):
        # Draw chess pieces on the board
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row) # chess row is reversed
                piece = self.board.piece_at(square)
                if piece:
                    piece_image = self.piece_images[piece.symbol()]
                    piece_rect = piece_image.get_rect()
                    x, y = ((col*self.size)+self.size//4), ((row*self.size)+self.size//4)
                    piece_rect.topleft = (x, y)
                    self.screen.blit(piece_image, piece_rect)

    def handle_mouse_down(self, pos):
        col = pos[0] // self.size
        row = pos[1] // self.size
        square = chess.square(col, 7 - row)
        piece = self.board.piece_at(square)

        if piece and piece.color == self.board.turn:
            self.dragging = square
            self.valid_moves = {move.to_square: move for move in self.board.legal_moves if move.from_square == square}

    def handle_mouse_up(self, pos):
        if self.dragging:
            col = pos[0] // self.size
            row = pos[1] // self.size
            target_square = chess.square(col, 7 - row)

            if target_square in self.valid_moves:
                move = self.valid_moves[target_square]
                self.board.push(move)

            self.dragging = None
            self.valid_moves = {}

    def highlight_valid_moves(self):
        for target_square in self.valid_moves:
            col, row = chess.square_file(target_square), 7 - chess.square_rank(target_square)
            center = ((col*self.size)+self.size//2, (row*self.size)+self.size//2)
            self.circle_fill(center, blue, 25)

    def reset(self):
        pass

    def circle_fill(self, xy, colour, radius):
        pygame.draw.circle(self.screen, colour, xy, radius)


    def draw_line(self, line_colour, n1, n2, width=2):
        pygame.draw.line(self.screen, line_colour, (n1.x, n1.y), (n2.x, n2.y), width)
    
    def write(self, text, colour, pos, font):
        self.screen.blit(font.render(text, True, colour), pos)

    def load_piece_images(self):
        pieces = ['b', 'k', 'n', 'p', 'q', 'r']
        for piece in pieces[:]:  # Using [:] to iterate over a copy to avoid modifying the list during iteration
            pieces.append(piece.upper())

        for piece_symbol in pieces:
            colour = 'w' if piece_symbol.isupper() else 'b'
            filename = f"{colour}{piece_symbol}.png"
            image_path = f"sprites/{filename}"
            original_image = pygame.image.load(image_path)
            scaled_size = (int(self.size * 0.5), int(self.size * 0.5))  # Adjust the scaling factor as needed
            scaled_image = pygame.transform.scale(original_image, scaled_size)
            self.piece_images[piece_symbol] = scaled_image

if __name__ == "__main__":
    pass
