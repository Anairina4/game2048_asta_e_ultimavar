import pygame
from random import randint, choice
from colors import *


class Gui:
    def __init__(self, window):
        pygame.init()
        pygame.display.set_caption('2048 Game')

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.matrix = [[0, 0, 0, 0] for column in range(4)]    # The matrix that holds the values
        self.cells = []    # Store data about tiles and text to draw on the screen
        self.score = [0,0]   # List to store the score in first index and data to draw in second position
        self.highscore = [0,0] # Store the score in first index and data to draw in
        self.highscore[0] = self.get_highScore()
        self.fontEngine = pygame.font.SysFont(SCORE_LABEL_FONT, 45)
        self.over = [False, False]   # First index stores whether the game is over. Second index stores whether game is lost or won
        self.startGame()

    def startGame(self):
        #Entry point for the game. Executes every time a new board is made

        # Adding two random tiles to the matrix
        row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2

        # To populate self.cells list with required data to draw
        for i in range(1,5):
            row = []
            for j in range(4):
                rect = pygame.Rect(10+j*100, 10+i*100, 80, 80)
                textRect, textSurface = None, None

                if (x:=self.matrix[i-1][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({
                    "rect": rect,
                    "textRect": textRect,
                    "textSurface": textSurface
                })
            self.cells.append(row)

    def addNewTile(self):
          #Adds a new tile to the matrix
        row, col = randint(0,3), randint(0,3)
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = choice([2,2,2,2,4])

    def horMoveExists(self):
        ''' Checks whether a horizontal move is possible or not'''
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j+1] == self.matrix[i][j]:
                    return True
        return False

    def verMoveExists(self):
        ''' Checks whether a vertical move is possible or not '''
        for i in range(3):
            for j in range(4):
                if self.matrix[i+1][j] == self.matrix[i][j]:
                    return True
        return False

    def gameOver(self):
        ''' Checks whether the game is over or not '''
        if any(2048 in row for row in self.matrix):
            self.over = [True, True]
        if not any(0 in row for row in self.matrix) and not self.horMoveExists() and not self.verMoveExists():
            self.over = [True, False]

    def updateTiles(self):
        ''' Updates self.cells with the new data when something changes it's position on the board '''
        for i in range(4):
            for j in range(4):
                # x = self.matrix[i][j]
                # if x != 0:
                if (x:=self.matrix[i][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = self.cells[i][j]['rect'].center
                    self.cells[i][j]['textRect'] = textRect
                    self.cells[i][j]['textSurface'] = textSurface
                elif x == 0:
                    self.cells[i][j]['textRect'] = None
                    self.cells[i][j]['textSurface'] = None

    def stack(self):

        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = new_matrix

    def get_highScore(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_highScore(self, highscore):
        with open('highscore.txt', 'w') as f:
            f.write(str(highscore))

    def combine(self):
        ''' Combines two elements if they are of same value into one and updates the matrix '''
        for i in range(4):
            for j in range(3):
                x = self.matrix[i][j]
                if x != 0 and x == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score[0] += self.matrix[i][j]

        if self.score[0] > self.highscore[0]:
          self.highscore[0] = self.score[0]

    def reverse(self):
        ''' Mirrors the matrix. Ex. [[2,4,8,8],...] will give [[8,8,4,2],...] '''
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        self.matrix = new_matrix

    def transpose(self):
        ''' Takes the transpose of matrix. Ref : https://www.geeksforgeeks.org/program-to-find-transpose-of-a-matrix/ '''
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[j][i] = self.matrix[i][j]
        self.matrix = new_matrix

    def scs(self):
        ''' Helper function to stack, combine and stack '''
        oldmatrix = self.matrix
        self.stack()
        self.combine()
        self.stack()
        return oldmatrix

    def add(self):
        #Helper function to add new tile, updating tiles and checking whether game is over
        self.addNewTile()
        self.updateTiles()
        self.gameOver()

    def left(self):
        oldmatrix = self.scs()
        if oldmatrix == self.matrix:
            return
        self.add()

    def right(self):
        oldmatrix = self.matrix
        self.reverse()
        self.scs()
        self.reverse()
        if oldmatrix == self.matrix:
            return
        self.add()

    def up(self):
        oldmatrix = self.matrix
        self.transpose()
        self.scs()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.add()

    def down(self):
        oldmatrix =self.matrix
        self.transpose()
        self.reverse()
        self.scs()
        self.reverse()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.add()

    def reset(self):
        ''' Resets the game by calling the constructor '''
        self.__init__(self.window)

    def draw(self, window, matrix, cells, score, high_score, over):

     # Background and Score and High Score labels
        window.fill(GRID_COLOR)

        score_surface_text = pygame.font.SysFont(SCORE_LABEL_FONT, 20).render('Score : ', True, (0,0,0))
        score_rect_text = score_surface_text.get_rect()
        score_rect_text.top = 25
        window.blit(score_surface_text, score_rect_text) # write 'score' on window

        high_score_surface_text = pygame.font.SysFont(SCORE_LABEL_FONT,20).render('High score:', True, (0,0,0))
        high_score_rect_text = high_score_surface_text.get_rect()
        high_score_rect_text.top = 60
        window.blit(high_score_surface_text, high_score_rect_text) # write 'highscore' on window

    #  Score as value
        scoreSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 20).render(str(score[0]), True, (0,0,0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 25
        scoreRect.left = score_rect_text.right + 10
        window.blit(scoreSurface, scoreRect)

    # High score as value
        high_score_surface = pygame.font.SysFont(SCORE_LABEL_FONT, 20).render(str(high_score[0]), True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.top = 60
        high_score_rect.left = high_score_rect_text.right + 10
        window.blit(high_score_surface, high_score_rect)

    # Cells
        for i in range(4):
            for j in range(4):
                cell = cells[i][j]
                if (x:=matrix[i][j]) != 0:
                    pygame.draw.rect(window, CELL_COLORS[x], cell['rect'])
                    window.blit(cell['textSurface'], cell['textRect'])
                elif x == 0:
                    pygame.draw.rect(window, EMPTY_CELL_COLOR, cell['rect'])
    # Game Over
        if over[0] and over[1]:
            gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('2048 Completed. Ctrl + q to reset', True, (0,0,0))
            gameOverRect = gameOverSurface.get_rect()
            gameOverRect.center = (WIDTH//2, HEIGHT//2)
            window.blit(gameOverSurface, gameOverRect)
        if over[0] and not over[1]:
            gameOverSurface = pygame.font.SysFont(SCORE_LABEL_FONT, 25).render('No moves left. Ctrl + q to reset', True, (0,0,0))
            gameOverRect = gameOverSurface.get_rect()
            gameOverRect.center = (WIDTH//2, HEIGHT//2)
            window.blit(gameOverSurface, gameOverRect)

        pygame.display.update()



