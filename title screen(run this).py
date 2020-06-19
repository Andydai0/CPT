import pygame
import pygame.freetype
import pygame.key
import random
import time 
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
from game import Game
pygame.init()

BLUE = (0, 0, 0)
WHITE = (255, 255, 255)
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("comicsansms", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
       
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        
        surface.blit(self.image, self.rect)


class Player:

    def __init__(self, score=0,):
        self.score = score


def main():
    screen = pygame.display.set_mode((1000, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)

        if game_state == GameState.SELECT:
            player = Player()
            game_state = select(screen, player)

        if game_state == GameState.NORMAL:
            player = Player()
            game_state = normal(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):

    start_btn = UIElement(
        center_position=(500, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(500, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    no_btn = UIElement(
        center_position=(500, 200),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Bullet Dodger by Andy and Dawson",
    )

    buttons = RenderUpdates(start_btn, quit_btn, no_btn)

    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )
    nextlevel_btn = UIElement(
        center_position=(500, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Select difficulty",
        action=GameState.SELECT,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn)
    return game_loop(screen, buttons)

def select(screen, buttons):
    start_btn = UIElement(
        center_position=(500, 300),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Normal",
        action=GameState.NORMAL,
    )

    buttons = RenderUpdates(start_btn)

    return game_loop(screen, buttons)


def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

def normal(screen, player):
    SIZE_X = 1000
    SIZE_Y = 600
    BULLET = 5

    if __name__ == '__main__':
        pygame.font.init()
        pygame.init()

        screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
        clock = pygame.time.Clock()

        game = Game(SIZE_X, SIZE_Y, BULLET)
        game_exit = False
        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
            foreground = pygame.Surface((SIZE_X, SIZE_Y), pygame.SRCALPHA)
            foreground.fill(pygame.Color('black'))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game = Game(SIZE_X, SIZE_Y, BULLET)

            game.tick()
            game.draw(foreground)

            screen.fill((255, 255, 255))
            screen.blit(foreground, (0, 0))
            pygame.display.flip()

            clock.tick(60)

    pygame.quit()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    SELECT = 2
    NORMAL = 3



if __name__ == "__main__":
    main()