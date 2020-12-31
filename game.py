import sys
import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

EMPTY = 0
HUMAN = 1
COMPUTER = 2

ROWS = 6
COLUMNS = 7

SQUARE_SIZE = 100
CIRCLE_RADIUS = 40

FONT_SIZE = 90
TEXT_LOCATION = (150, 175)

class ConnectFour:

    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((COLUMNS * SQUARE_SIZE, ROWS * SQUARE_SIZE))
        pygame.display.set_caption("Connect Four")
        self.font = pygame.font.SysFont("Consolas", FONT_SIZE)

        self.board = [[EMPTY for j in range(COLUMNS)] for i in range(ROWS)]
        self.human_turn = True

    def run_game_loop(self):
        clock = pygame.time.Clock()
        is_game_over = False
        while not is_game_over:
            self.draw_board()
            if self.check_win(HUMAN):
                text = self.font.render("You win!", True, BLACK)
                self.display.blit(text, TEXT_LOCATION)
                is_game_over = True
            elif self.check_win(COMPUTER):
                text = self.font.render("You lose!", True, BLACK)
                self.display.blit(text, TEXT_LOCATION)
                is_game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                
            self.shade_next_move(pygame.mouse.get_pos()[0])
            pygame.display.update()
            clock.tick(60)

        if is_game_over:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

    def draw_board(self):
        pygame.draw.rect(self.display, BLUE, (0, 0, COLUMNS * SQUARE_SIZE, ROWS * SQUARE_SIZE))

        for i in range(ROWS):
            for j in range(COLUMNS):
                center = ((j  +  0.5) * SQUARE_SIZE, (i  +  0.5) * SQUARE_SIZE)
                if self.board[i][j] == 0:
                    color = WHITE
                elif self.board[i][j] == HUMAN:
                    color = RED
                elif self.board[i][j] == COMPUTER:
                    color = YELLOW
                pygame.draw.circle(self.display, color, center, CIRCLE_RADIUS)

    def drop_player(self, column, player):
        for i in range(ROWS - 1, -1, -1):
            if self.board[i][column] == EMPTY:
                self.board[i][column] = player
                break

    def shade_next_move(self, mouse_x):
        for j in range(COLUMNS):
            if j * SQUARE_SIZE <= mouse_x < (j + 1) * SQUARE_SIZE:
                next_row = ROWS - 1
                while self.board[next_row][j] != EMPTY:
                    next_row -= 1
                center = ((j  +  0.5) * SQUARE_SIZE, (next_row  +  0.5) * SQUARE_SIZE)
                pygame.draw.circle(self.display, GREY, center, CIRCLE_RADIUS)
                break

    def handle_mouse_click(self, event):
        mouse_x = event.pos[0]
        for j in range(COLUMNS):
            if j * SQUARE_SIZE <= mouse_x < (j  +  1) * SQUARE_SIZE:
                if self.human_turn:
                    self.drop_player(j, HUMAN)
                    self.human_turn = not self.human_turn
                    break
                else:
                    self.drop_player(j, COMPUTER)
                    self.human_turn = not self.human_turn
                    break

    def check_win(self, player):
        # Check rows
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if self.board[row][col] == player and self.board[row][col + 1] == player and \
                    self.board[row][col + 2] == player and self.board[row][col + 3] == player:
                    return True

        # Check columns
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if self.board[row][col] == player and self.board[row + 1][col] == player and \
                    self.board[row + 2][col] == player and self.board[row + 3][col] == player:
                    return True

        # Check right diaganols
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if self.board[row][col] == player and self.board[row + 1][col + 1] == player \
                    and self.board[row + 2][col + 2] == player and \
                    self.board[row + 3][col + 3] == player:
                    return True

        # Check left diaganols
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if self.board[row][col] == player and self.board[row - 1][col + 1] == player and \
                    self.board[row - 2][col + 2] == player and \
                    self.board[row - 3][col + 3] == player:
                    return True
        return EMPTY


if __name__ == "__main__":
    ConnectFour().run_game_loop()
