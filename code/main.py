import pygame, sys
from settings import *
from view import View
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Долбоящер спешит на помощь!')
        pygame.display.set_icon(pygame.image.load('../Logotip.png'))
        self.clock = pygame.time.Clock()
        self.view = View()
        self.player = Player

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill("black")
            self.view.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
