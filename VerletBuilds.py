import Verlet as vt
import pygame
import random

# initialize pygame
pygame.init()

# set the size of the window in Verlet.py
vt.window_width = 800
vt.window_height = 800

# create the window
screen = pygame.display.set_mode((vt.window_width, vt.window_height))

# set the title of the window
pygame.display.set_caption("Bouncing Balls with Verlet Integration")

# set the FPS
fpsClock = pygame.time.Clock()

# Arrays to hold objects
balls = []
rods = []

# set the background color of the window
background_color = (255, 255, 255)
# other color options
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)




# spawn balls
x = vt.window_width / 6
y = 10
radius = 10
dist = 10
# for i in range(10):
#     vt.buildBalls(2, random.randint(0,vt.window_width), random.randint(0, vt.window_height/2), x + random.randint(1,15), y + random.randint(-10,10), radius, False, balls, rods)

# vt.buildChain(25, x, y, dist, radius, black, balls, rods)

meshSize = 35
for i in range(meshSize):
    # BuildChain(Chain Length, x, y, distance, radius, color, arr1, arr2)
    vt.buildChain(25, x + (i * dist), y, 10, 1, black, balls, rods)
vt.buildMesh(balls, rods, meshSize, 25)

# Build box
# vt.buildBox(black, balls, rods)
# vt.buildBalls(5, x, y, x + 2, y, radius, False, balls, rods)


def run():
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Release mesh from fixed positions
                if event.key == pygame.K_SPACE:
                    for ball in balls:
                        ball.fixed = False

        # move the balls
        for ball in balls:
            ball.move()

        # check for collisions
        for ball in balls:
            # Param False -> no collision check with other balls

            # ball.check_collisions(balls)
            ball.check_boarder_collisions()

        for i in range(3):
            for rod in rods:
                rod.rip_checker(rods)
                rod.satisfy_constraints()
                rod.mouse_collision(rods)


        # draw the balls
        screen.fill(background_color)

        # for ball in balls:
        #     ball.draw(screen)
        for rod in rods:
            rod.draw(screen)
        pygame.display.update()
        fpsClock.tick(vt.FPS)


run()