import pygame
from colors import WIDTH, HEIGHT
from gui import *
from colors import FPS
class Game2048:

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Gui(self.window)

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.highscore[0] = 0
                    self.running = False
                    break

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.game.left()
                    if event.key == pygame.K_RIGHT:
                        self.game.right()
                    if event.key == pygame.K_UP:
                        self.game.up()
                    if event.key == pygame.K_DOWN:
                        self.game.down()
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL and self.game.over:
                        self.game.reset()

    def run(self):

        while self.running:
            self.clock.tick(FPS)
            self.game.draw(self.window,self.game.matrix, self.game.cells, self.game.score, self.game.highscore, self.game.over)
            self.handle_events()
            self.game.save_highScore(self.game.highscore[0])
        pygame.quit()
        quit()




