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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Landing")
clock = pygame.time.Clock()


@dataclass
class Plane:
    x: int
    y: int
    state: str = "flying"
    speed: int = MAX_PLANE_SPEED
    rotation: int = 0
    color: tuple = (100, 100, 100)

    def draw(self):
        base_coords = [
            (-16, 0), (-13, 2), (-15, 7), (-12, 7), (-8, 2), (-1, 2),
            (-6, 6), (-5, 6), (8, 2), (16, 2), (19, -2), (8, -2),
            (-5, -8), (-6, -8), (-1, -2), (-13, -2)]
        rotated = base_coords if self.rotation == 0 else [
            (x * math.cos(self.rotation) - y * math.sin(self.rotation),
             x * math.sin(self.rotation) + y * math.cos(self.rotation))
            for x, y in base_coords]
        coords = [(WIDTH//2 + 4*x, self.y - 4*y) for x, y in rotated]
        pygame.draw.polygon(screen, self.color, coords)

    # The states are:
    #
    # "flying"     : the plane is in the air at the cruising altitude,
    #                moving forward. The user can press the down arrow
    #                key to start descending.
    # "descending" : the plane is descending towards the ground, facing
    #                downwards. The user can press the up arrow key to
    #                raise the nose and start landing. If they raise the
    #                nose too early, the plane will start rising again.
    #                If they raise the nose too late, the plane will
    #                crash. Raising it just right will put the plane
    #                in the "landing" state.
    # "landing"    : the plane has just brought the nose up, right above
    #                the ground, and is still going down. When it hits
    #                the ground, it will be in the "touching" state.
    # "touching"   : the plane has just touched the ground, and is
    #                still moving forward with the nose up. The user
    #                can press the down arrow key to lower the nose,
    #                but it will still be moving forward fast.
    # "down"       : the user has just lowered the nose so all wheels
    #                are on the ground and the plane is moving
    #                forward. The user needs to press the Return key
    #                here to start braking.
    # "braking"    : the plane is on the ground, decelerating. When
    #                it comes to a stop, it will be in the "stopped"
    #                state.
    # "stopped"    : the plane has come to a stop on the ground.
    #                In the stopped state, the user can press the right
    #                arrow key to start the plane moving again.
    # "starting"   : the plane is starting to move on the ground, and
    #                the user can press the up arrow key to take off.
    # "rising"     : the plane is rising after touching down. It will
    #                keep rising until it reaches the cruising altitude
    #                in which case it will automatically level off and
    #                return to the "flying" state.
    # "crashed"    : the plane has crashed and is no longer moving.

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
                # Added plane takeoff sound effect
                takeoff_sound_effect.play()
    draw_scene()
