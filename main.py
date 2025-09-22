import asyncio
import pygame
from settings import WIDTH, HEIGHT
from settings import *
from states.gameplay import Game


class BubbleGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мильна бульбашка")
        self.assets = self.load_assets()
        self.state = None
        self.running = True
        self.set_state('gameplay')

    def load_assets(self):
        return {
            "bubble": pygame.image.load("assets/images/bubble.png").convert_alpha(),
            "background": pygame.transform.scale(
                pygame.image.load("assets/images/background.png").convert_alpha(), (WIDTH, HEIGHT)),
            "victory": pygame.transform.scale(
                pygame.image.load("assets/images/victory_background.png").convert_alpha(), (WIDTH, HEIGHT)),
            "defeat": pygame.transform.scale(
                pygame.image.load("assets/images/defeat_background.png").convert_alpha(), (WIDTH, HEIGHT)),
            "font": pygame.font.SysFont("Arial", 36)
        }

    def set_state(self, state_name):
        if state_name == 'gameplay':
            self.state = Game(self.screen, self.assets, self)

    async def run(self):
        while self.running:
            self.state.handle_events()
            self.state.update()
            self.state.draw()
            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

        pygame.quit()


if __name__ == "__main__":
    game = BubbleGame()
    asyncio.run(game.run())
