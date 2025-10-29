"""A simple generator of Mondrian-style colored rectangles.
Based on an original JavaScript implementation by Max Halford
at https://maxhalford.github.io/blog/mondrian/
"""

import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mondrian")

COLORS = [
    # Most of the squares will be white, so it’s included many times.
    # That way, the random.choice function will pick white with a
    # higher probability than the other colors.
    pygame.Color("white"),
    pygame.Color("white"),
    pygame.Color("white"),
    pygame.Color("white"),
    pygame.Color("black"),
    pygame.Color("red"),
    pygame.Color("blue"),
    pygame.Color("yellow"),
]

# We don't want any of the rectangles to be smaller than a percentage of
# the width and height of the screen.
X_PADDING = int(WIDTH * 0.05)
Y_PADDING = int(HEIGHT * 0.05)
LINE_WIDTH = 5


def draw_and_split(rect, level):
    # First, draw the rectangle, filled and outlined
    pygame.draw.rect(screen, random.choice(COLORS), rect)
    pygame.draw.rect(screen, pygame.Color("black"), rect, LINE_WIDTH)

    # Determine whether the recursion should stop, and if so, return
    if level == 0:
        # We've gone as deep as we want to go
        return
    if rect.width < 2 * X_PADDING or rect.height < 2 * Y_PADDING:
        # Rectangle is too small to split
        return

    # If we get here, we need to split. Always split in the direction that
    # has the most space, either horizontally or vertically. To split, choose
    # a random value within the longer axis, but not too close to the edges
    # to avoid creating rectangles that are too small. This is where the
    # X_PADDING and Y_PADDING come in. The two rectangles on either side of
    # the split will be called r1 and r2, and they will be drawn recursively.
    if rect.width > rect.height:
        x = random.randint(rect.left + X_PADDING, rect.right - X_PADDING)
        r1 = pygame.Rect(rect.left, rect.top, x - rect.left, rect.height)
        r2 = pygame.Rect(x, rect.top, rect.right - x, rect.height)
    else:
        y = random.randint(rect.top + Y_PADDING, rect.bottom - Y_PADDING)
        r1 = pygame.Rect(rect.left, rect.top, rect.width, y - rect.top)
        r2 = pygame.Rect(rect.left, y, rect.width, rect.bottom - y)

    draw_and_split(r1, level - 1)
    draw_and_split(r2, level - 1)


def draw_scene():
    # Clear screen then draw outer rectangle to take up the whole display
    screen.fill(pygame.Color("white"))
    outer_rectangle = pygame.Rect(0, 0, WIDTH, HEIGHT)
    draw_and_split(outer_rectangle, 5)
    pygame.display.flip()


draw_scene()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # A click "starts over" with a new scene!
            draw_scene()
