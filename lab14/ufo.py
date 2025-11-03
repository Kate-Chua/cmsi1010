from dataclasses import dataclass
import pygame
import sys

WIDTH, HEIGHT = 800, 600
SKY_COLOR = (0, 255, 255)
SUN_COLOR = (255, 200, 0)
SUN_POSITION = (WIDTH - 50, 20)
SUN_RADIUS = 150
GRASS_COLOR = (0, 128, 0)
GRASS_HEIGHT = 100
GRASS_TOP = HEIGHT - GRASS_HEIGHT
GRASS_RECTANGLE = (0, GRASS_TOP, WIDTH, GRASS_HEIGHT)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invasion")
clock = pygame.time.Clock()


class Alien:
    def __init__(self):
        self.x = 350
        self.y = 450
        self.speed = 5
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


@dataclass
class UFO:
    x: int
    y: int
    width: int = 100
    height: int = 30
    color: tuple = (128, 128, 128)
    speed: int = 1

    def draw(self):
        pygame.draw.ellipse(screen, self.color,
                            (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.x = -self.width
        pygame.draw.ellipse(screen, self.color, (self.x + self.width //
                            4, self.y - self.height // 3, self.width // 2, self.height))


ufos = [
    UFO(x=0, y=50),
    UFO(x=200, y=100, speed=3.5, width=80, height=20),
    UFO(x=400, y=150, color=(160, 160, 160), width=120, speed=3),
    UFO(x=600, y=200, speed=4)
]

alien = Alien()


def draw_scene():
    screen.fill(SKY_COLOR)
    pygame.draw.circle(screen, SUN_COLOR, SUN_POSITION, SUN_RADIUS)
    pygame.draw.rect(screen, GRASS_COLOR, GRASS_RECTANGLE)
    for ufo in ufos:
        ufo.draw()
        ufo.move()
    alien.draw(screen)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    alien.move(keys)
    draw_scene()
    clock.tick(60)
