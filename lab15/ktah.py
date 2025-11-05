import pygame
import math
from dataclasses import dataclass

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("K'tah")
clock = pygame.time.Clock()
frozen = False
UNFREEZE = pygame.USEREVENT + 1


@dataclass
class Agent:
    x: int
    y: int
    radius: int
    speed: int
    color: tuple

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 3.0:
            # Allow three pixels of leeway to avoid jittering
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def is_collided_with(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < (self.radius + other.radius)


@dataclass
class Player(Agent):
    x: int = WIDTH // 2
    y: int = HEIGHT // 2
    radius: int = 20
    speed: int = 5
    color: tuple = (200, 200, 255)

    def teleport(self, pos):
        self.x, self.y = pos

    def is_caught_by_any_of(self, zombies):
        for zombie in zombies:
            if self.is_collided_with(zombie):
                return True
        return False


@dataclass
class Zombie(Agent):
    speed: int = 2
    radius: int = 20
    color: tuple = (255, 0, 0)


def draw_scene():
    if player.is_caught_by_any_of(zombies):
        return
    player.move_towards(pygame.mouse.get_pos())
    if not frozen:
        for zombie in zombies:
            zombie.move_towards((player.x, player.y))
    screen.fill((0, 100, 0))
    player.draw()
    for zombie in zombies:
        zombie.draw()
    clock.tick(60)
    pygame.display.flip()


player = Player()
zombies = [
    Zombie(x=20, y=20, speed=1.8),
    Zombie(x=WIDTH-20, y=20),
    Zombie(x=20, y=HEIGHT-20, speed=2.5),
    Zombie(x=WIDTH-20, y=HEIGHT-20, speed=0.9, color=(0, 200, 0)),
    Zombie(x=20, y=40, speed=3),
    Zombie(x=WIDTH-20, y=40, speed=3),
    Zombie(x=20, y=HEIGHT-40, speed=3),
    Zombie(x=WIDTH-40, y=HEIGHT-40, speed=5, radius=40)
]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.teleport(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if not frozen:
                    frozen = True
                    pygame.time.set_timer(UNFREEZE, 5000, loops=1)
        elif event.type == UNFREEZE:
            frozen = False
    clock.tick(60)
    draw_scene()
