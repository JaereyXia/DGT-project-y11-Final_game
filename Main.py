"""
Jerry Shi
tool:python
game idea: 3rd person shooting game
"""

import pygame.time
from data import *
from player import Player

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        self.b = (0, 0, 0)

        #groups
        self.all_sprites = pygame.sprite.Group()

        self.player = Player((400, 300), self.all_sprites)#所有实体

    def run(self):
        while self.running:
            #data time
            dt = self.clock.tick() / 1000

            #loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #updata
            self.all_sprites.update(dt)

            #draw
            self.display.fill(self.b)
            self.all_sprites.draw(self.display)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    G = Game()
    G.run()
