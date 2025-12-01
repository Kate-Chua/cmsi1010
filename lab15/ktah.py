from dataclasses import dataclass
import math
import pygame
import pygame.freetype

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("K'tah")
clock = pygame.time.Clock()
font = pygame.freetype.SysFont('sans', 100)

frozen = False
scarecrow = None
game_over = False

UNFREEZE = pygame.USEREVENT + 1
REMOVE_SCARECROW = pygame.USEREVENT + 2


@dataclass
class Agent:
    x: int
    y: int
    radius: int
    speed: int
    color: tuple

    def is_collided_with(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < (self.radius + other.radius)

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
    color: tuple = (80, 255, 0)


@dataclass
class Scarecrow(Agent):
    speed: int = 0
    radius: int = 15
    color: tuple = (255, 255, 0)


def draw_scene():
    if player.is_caught_by_any_of(zombies):
        global game_over
        game_over = True
        font.render_to(screen, (20, 20), "GAME OVER", (255, 0, 0))
        pygame.display.flip()
        return
    player.move_towards(pygame.mouse.get_pos())
    if not frozen:
        for zombie in zombies:
            if scarecrow:
                zombie.move_towards((scarecrow.x, scarecrow.y))
            else:
                zombie.move_towards((player.x, player.y))
    screen.fill((0, 100, 0))
    player.draw()
    for zombie in zombies:
        zombie.draw()
    if scarecrow:
        scarecrow.draw()
    pygame.display.flip()


player = Player()
zombies = [
    Zombie(x=20, y=20, speed=1.8),
    Zombie(x=WIDTH-20, y=20),
    Zombie(x=20, y=HEIGHT-20, speed=2.5),
    Zombie(x=WIDTH-20, y=HEIGHT-20, speed=0.9)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                player.teleport(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if not frozen:
                    frozen = True
                    pygame.time.set_timer(UNFREEZE, 5000, loops=1)
            if event.key == pygame.K_s:
                if not scarecrow:
                    scarecrow = Scarecrow(x=player.x, y=player.y)
                    pygame.time.set_timer(REMOVE_SCARECROW, 5000, loops=1)
        elif event.type == UNFREEZE:
            frozen = False
        elif event.type == REMOVE_SCARECROW:
            scarecrow = None
    clock.tick(60)
    draw_scene()
