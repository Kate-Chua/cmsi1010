"""A animation of a plane landing, controlled by the user.

The plane begins in a flying state. The user presses the down arrow key to
start descending. When the plane is close to the ground, the user must
press the up arrow key to raise the nose, otherwise the plane will crash.
After the plane touches the ground, the user presses the down arrow key
to lower the nose. Then they must press the return key to start braking.
The plane will come to a stop. At this point, the user can press the right
arrow key to start the plane again. It will accelerate on the ground until
it is going fast enough, at which point the user presses the up arrow key
to take off. The plane will then rise to a cruising altitude and fly until
the user presses the down arrow key to start descending again.
"""
# -------------

"""
This code has been altered from the original version in the following ways:
• Added Nyan Cat background music that loops continously
• Changed the plan into a Nyan Cat
• Added a rainbow trail behind the Nyan Cat while flying
• Changed the background to a looping image of a starry sky
"""

import pygame
import math
from dataclasses import dataclass

WIDTH, HEIGHT = 1024, 600
SKY_COLOR = (135, 240, 255)
GRASS_COLOR = (128, 255, 100)
GRASS_HEIGHT = 100
GRASS_TOP = HEIGHT - GRASS_HEIGHT
GRASS_RECTANGLE = (0, GRASS_TOP, WIDTH, GRASS_HEIGHT)
GROUND_LEVEL = HEIGHT - (GRASS_HEIGHT // 2)
TREE_SPACING = 173
MAX_PLANE_SPEED = 23
CRUISING_ALTITUDE = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nyan Cat Landing")
clock = pygame.time.Clock()

# Music
nyan_theme = pygame.mixer.Sound("./nyan_loop.mp3")
nyan_theme.play(loops=-1)

# Images
nyan_img = pygame.image.load("nyan.png").convert_alpha()
dead_nyan_img = pygame.image.load("dead.png").convert_alpha()
dead_nyan_img = pygame.transform.scale(dead_nyan_img, (200, 150))
bg = pygame.image.load("background.jpg").convert()
bg_width = bg.get_width()
bg_x1 = 0
bg_x2 = bg_width
scroll_speed = 3


@dataclass
class Plane:
    x: int
    y: int
    state: str = "flying"
    speed: int = MAX_PLANE_SPEED
    rotation: float = 0

    def draw_rainbow(self):
        if self.state != "stopped":
            colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                      (0, 255, 0), (0, 0, 255), (128, 0, 128)]
            shift = (pygame.time.get_ticks() // 150) % len(colors)
            stripe_h = 6
            max_x = WIDTH // 2 - 20
            base_y = self.y - 18
            for i in range(len(colors)):
                color = colors[(i + shift) % len(colors)]
                pygame.draw.rect(screen, color, (0, base_y +
                                 i*stripe_h, max_x, stripe_h))

    def draw(self):
        # Only draw rainbow if not stopped or crashed
        if self.state != "stopped" and self.state != "crashed":
            colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                      (0, 255, 0), (0, 0, 255), (128, 0, 128)]
            shift = (pygame.time.get_ticks() // 150) % len(colors)
            stripe_h = 6
            max_x = WIDTH//2 - 20
            base_y = self.y - 18
            for i in range(len(colors)):
                color = colors[(i + shift) % len(colors)]
                pygame.draw.rect(screen, color, (0, base_y +
                                 i*stripe_h, max_x, stripe_h))

        # Draw dead nyan if crashed
        if self.state == "crashed":
            img = dead_nyan_img
        else:
            img = nyan_img

        rotated = pygame.transform.rotate(img, -self.rotation * 50)
        rect = rotated.get_rect(center=(WIDTH // 2, self.y))
        screen.blit(rotated, rect)

    def move(self):
        if self.state != "stopped":
            self.x += self.speed % TREE_SPACING
        if self.state == "flying":
            pass
        elif self.state == "descending":
            self.y += self.speed * 0.1
            if self.y >= GROUND_LEVEL:
                self.state = "crashed"
                self.color = (255, 0, 0)  # red for crashed
                self.speed = 0
                self.y = GROUND_LEVEL
        elif self.state == "landing":
            self.y += self.speed * 0.1
            if self.y >= GROUND_LEVEL:
                self.state = "touching"
                self.y = GROUND_LEVEL
        elif self.state == "touching":
            pass
        elif self.state == "down":
            pass
        elif self.state == "braking":
            self.speed -= 0.1
            if self.speed <= 0:
                self.speed = 0
                self.state = "stopped"
        elif self.state == "starting":
            self.y = GROUND_LEVEL
            self.speed += 0.1
            if self.speed >= MAX_PLANE_SPEED:
                self.speed = MAX_PLANE_SPEED
        elif self.state == "rising":
            self.y -= self.speed * 0.1
            if self.y <= CRUISING_ALTITUDE:
                self.y = CRUISING_ALTITUDE
                self.state = "flying"
                self.rotation = 0


plane = Plane(0, y=CRUISING_ALTITUDE)


def draw_tree(x, y):
    pygame.draw.rect(screen, (139, 69, 19), (x-5, y-20, 10, 20))
    pygame.draw.polygon(screen, (0, 128, 0), [
                        (x-30, y-20), (x+30, y-20), (x, y-100)])


def draw_scene():
    # The code below is to simulate a scrolling background
    global bg_x1, bg_x2

    if plane.state == "stopped" or plane.state == "crashed":
        current_scroll = 0
    else:
        current_scroll = scroll_speed

    bg_x1 -= current_scroll
    bg_x2 -= current_scroll

    if bg_x1 <= -bg_width:
        bg_x1 = bg_x2 + bg_width
    if bg_x2 <= -bg_width:
        bg_x2 = bg_x1 + bg_width

    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x2, 0))

    pygame.draw.rect(screen, GRASS_COLOR, GRASS_RECTANGLE)
    x = -plane.x
    while x < WIDTH:
        draw_tree(x, GRASS_TOP)
        x += TREE_SPACING
    plane.draw()
    plane.move()
    clock.tick(60)
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and plane.state == "flying":
                plane.rotation = -0.2
                plane.state = "descending"
            elif event.key == pygame.K_UP and plane.state == "descending":
                plane.rotation = 0.2
                if plane.y < GROUND_LEVEL - 100:
                    plane.state = "rising"
                else:
                    plane.state = "landing"
            elif event.key == pygame.K_DOWN and plane.state == "touching":
                plane.rotation = 0
                plane.state = "down"
            elif event.key == pygame.K_RETURN and plane.state == "down":
                plane.state = "braking"
            elif event.key == pygame.K_RIGHT and plane.state == "stopped":
                plane.state = "starting"
            elif event.key == pygame.K_UP and plane.state == "starting" \
                    and plane.speed == MAX_PLANE_SPEED:
                plane.rotation = 0.1
                plane.state = "rising"

    draw_scene()
