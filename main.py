import Verlet as vt
import pygame
import random

# Initialize pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((vt.window_width, vt.window_height))

# Set the title of the window
pygame.display.set_caption("Bouncing Balls with Verlet Integration")

# Initialize font
pygame.font.init()

# Set font
font = pygame.font.SysFont("Arial", 30)

# set the FPS
fpsClock = pygame.time.Clock()

# Initialize arrays to hold objects
balls = []
rods = []

# Set Default colors
background_color = (255, 255, 255)
black = (0,0,0)


# ~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
StartStatus = False
CreateBall = False
CreateSingleChain = False
CreateMesh = False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~ BUILD BOUNCING BALLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SpawnBalls():
    global CreateBall
    CreateBall = True
    n = 50              # Number of ball pairs created (i.e. n=10 results in 20 spawned balls)
    for i in range(n):
        # Ball Building Variables -
        x = random.randint(0, vt.window_width)
        y = random.randint(0, vt.window_height)
        dx = x + random.randint(-10, 10)
        dy = y + random.randint(0, 15)
        radius = random.randint(8, 14)
        CreateRods = False

        vt.buildBalls(2, x, y, dx, dy, radius, CreateRods, balls, rods)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~ BUILD SINGLE CHAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SpawnSingleChain():
    global CreateSingleChain
    # Single Chain Building Variables -
    x = vt.window_width / 2             # X Placement first joint in Chain
    y = 10                              # Y Placement first joint in Chain
    chainSize = 20                      # Number of Rows chain
    distY = 10                          # Distance between each joint
    radius = 1                          # Radius of Joints (Keep low for chain)
    color = black                       # Color of Joints (If balls are drawn to screen)
    swingAmt = 10                       # Adds offset to each row by adding to x start position
    CreateSingleChain = True

    vt.buildChain(chainSize, x, y, distY, radius, color, balls, rods, swingAmt)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~ BUILD MESH
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SpawnMesh():
    global CreateMesh
    # Mesh Building Variables -
    x = vt.window_width / 5             # X Placement top left Mesh
    y = 10                              # Y Placement top left Mesh
    meshSize = 30                       # Number of Columns in Mesh
    chainSize = 20                      # Number of Rows in Mesh
    distX = 8                          # Distance between each column
    distY = 12                          # Distance between each row
    radius = 0                          # Radius of Joints (Keep low for mesh)
    color = black                       # Color of Joints (Not visible for mesh)
    swingAmt = random.randint(0,20)                      # Adds offset to each row by adding to x start position
    CreateMesh = True

    for i in range(meshSize):
        vt.buildChain(chainSize, x + (i * distX), y, distY, radius, color, balls, rods, swingAmt)
    vt.buildMesh(balls, rods, meshSize, chainSize, distX)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Build box
# vt.buildBox(black, balls, rods)


def start_menu():
    screen.fill(background_color)
    text_surface = font.render("Press Space to Start", False, black)
    text_rect = text_surface.get_rect(center=(vt.window_width / 2, vt.window_height / 4))
    screen.blit(text_surface, text_rect)
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Release mesh from fixed positions
                if event.key == pygame.K_SPACE:
                    reset()
        pygame.display.update()

def reset():
    global StartStatus
    global balls
    global rods

    StartStatus = False
    balls = []
    rods = []

    # SpawnBalls()
    # SpawnSingleChain()
    SpawnMesh()
    run()



def run():
    global StartStatus
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Release mesh from fixed positions
                if event.key == pygame.K_SPACE:
                    if StartStatus:
                        reset()
                    else:
                        StartStatus = True
                        for ball in balls:
                            ball.fixed = False

        # update ball positions
        for ball in balls:
            ball.move()

        # check for collisions
        for ball in balls:
            if CreateBall:
                ball.check_collisions(balls)
            ball.check_boarder_collisions()

        for i in range(1):
            for rod in rods:
                if CreateMesh or CreateSingleChain:
                    rod.mouse_collision(rods)
                    rod.rip_checker(rods)
                rod.satisfy_constraints()

        screen.fill(background_color)
        if CreateBall:
            for ball in balls:
                ball.draw(screen)
        for rod in rods:
            rod.draw(screen)
        if StartStatus:
            text_surface = font.render("Press Space to Start", False, black)
            text_rect = text_surface.get_rect(center=(vt.window_width / 2, vt.window_height / 4))
            screen.blit(text_surface, text_rect)
        pygame.display.update()
        fpsClock.tick(vt.FPS)


if __name__ == "__main__":
    start_menu()