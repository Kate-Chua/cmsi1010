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

import math
from dataclasses import dataclass
import pygame

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
pygame.mixer.init()
takeoff_sound_effect = pygame.mixer.Sound("./airplanetakeoff.mp3")
landing_sound_effect = pygame.mixer.Sound("./airplanelanding.mp3")
nyan_down_sound = pygame.mixer.Sound("./nyan_down.mp3")
nyan_up_sound = pygame.mixer.Sound("./nyan_up.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nyan Cat Landing")
clock = pygame.time.Clock()

# Load nyan cat sprite
nyan_img = pygame.image.load("nyan.png").convert_alpha()


@dataclass
class Plane:
    x: int
    y: int
    state: str = "flying"
    speed: int = MAX_PLANE_SPEED
    rotation: float = 0

    def draw(self):
        # ----- CASCADING RAINBOW COLORS -----
        base_colors = [
            (255, 0, 0),      # red
            (255, 165, 0),    # orange
            (255, 255, 0),    # yellow
            (0, 255, 0),      # green
            (0, 0, 255),      # blue
            (128, 0, 128)     # purple
        ]

        shift = (pygame.time.get_ticks() // 150) % len(base_colors)
        rainbow_colors = base_colors[shift:] + base_colors[:shift]

        stripe_height = 6
        start_x = 0
        end_x = WIDTH // 2 - 20  # stops just before nyan cat

        for i, color in enumerate(rainbow_colors):
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    start_x,
                    self.y - 18 + i * stripe_height,
                    end_x - start_x,
                    stripe_height
                )
            )

        rotated = pygame.transform.rotate(nyan_img, -self.rotation * 50)
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
    pygame.draw.rect(screen, (139, 69, 19), (x - 5, y - 20, 10, 20))
    pygame.draw.polygon(screen, (0, 128, 0),
                        [(x - 30, y - 20), (x + 30, y - 20), (x, y - 100)])


def draw_scene():
    if plane.state != "stopped":
        screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, GRASS_COLOR, GRASS_RECTANGLE)

        x = -plane.x
        while x < WIDTH:
            draw_tree(x, GRASS_TOP)
            x += TREE_SPACING

        plane.draw()
        plane.move()

    clock.tick(60)
    pygame.display.flip()


# -------- GAME LOOP --------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN and plane.state == "flying":
                plane.rotation = -0.2
                plane.state = "descending"
                nyan_down_sound.play()  # play Nyan Cat descending sound

            elif event.key == pygame.K_UP and plane.state == "descending":
                plane.rotation = 0.2
                if plane.y < GROUND_LEVEL - 100:
                    plane.state = "rising"
                    nyan_up_sound.play()  # play Nyan Cat rising sound
                else:
                    plane.state = "landing"
                    landing_sound_effect.play()

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
                takeoff_sound_effect.play()
                nyan_up_sound.play()  # also play rising sound when taking off

    draw_scene()
