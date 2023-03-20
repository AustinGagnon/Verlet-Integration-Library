import pygame
import random
import math


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~ Global Variables
# ~ Variables can be overwritten from main.py
GRAVITY = 1.01                    # Gravity
window_width = 500                # Width - Default 500
window_height = 600               # Height - Default 600
FPS = 40                          # Frames Per Second
MAX_SPEED = 150                   # Caps ball movement speed
CUT_DIST = 90                     # Defines radius of cutting distance (Higher = harder to tear)
TEAR_DIST = 90                    # Sets force needed to rip curtain (Higher = harder to tear)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# define the Ball class
class Ball:
    def __init__(self, x, y, px, py, radius, color, fixed):
        self.x = x
        self.y = y
        self.prev_x = px
        self.prev_y = py
        self.radius = radius
        self.color = color
        self.fixed = fixed

    def move(self):
        if not self.fixed:
            temp_x = self.x
            temp_y = self.y
            temp_dX = self.x - self.prev_x
            temp_dY = (self.y - self.prev_y) + 0.5 * GRAVITY
            if temp_dX > 0:
                self.x += min(MAX_SPEED, temp_dX)
            else:
                self.x += max(-MAX_SPEED, temp_dX)
            if temp_dY > 0:
                self.y += min(MAX_SPEED, temp_dY)
            else:
                self.y += max(-MAX_SPEED, temp_dY)
            self.prev_x = temp_x
            self.prev_y = temp_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collisions(self, balls):
        Mouse_X, Mouse_Y = pygame.mouse.get_pos()
        balls.append(Ball(Mouse_X, Mouse_Y, Mouse_X, Mouse_Y, 30, (255,255,255), False))
        for ball in balls:
            if ball != self and not self.fixed:
                distance = ((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5
                if distance < self.radius + ball.radius:
                    overlap = self.radius + ball.radius - distance
                    theta = math.atan2(self.y - ball.y, self.x - ball.x)
                    self.x += 0.5 * overlap * math.cos(theta)
                    self.y += 0.5 * overlap * math.sin(theta)
                    ball.x -= 0.5 * overlap * math.cos(theta)
                    ball.y -= 0.5 * overlap * math.sin(theta)
        balls.pop()

    def check_boarder_collisions(self):
        if self.x - self.radius < 0:
            self.x = self.radius
            self.prev_x = (self.x - self.prev_x) + self.x

        elif self.x + self.radius > window_width:
            self.x = window_width - self.radius
            self.prev_x = (self.x - self.prev_x) + self.x

        if self.y - self.radius < 0:
            self.y = self.radius
            self.prev_y = (self.y - self.prev_y) + self.y

        elif self.y + self.radius > window_height:
            overlap = max(0, self.y - window_height)
            self.y = window_height - self.radius
            self.prev_y = self.y
            # self.prev_y = (self.y - self.prev_y) + self.y + overlap


# define the Rod class
class Rod:
    def __init__(self, ball1, ball2):
        self.ball1 = ball1
        self.ball2 = ball2
        self.dx = self.ball2.x - self.ball1.x
        self.dy = self.ball2.y - self.ball1.y
        self.length = ( self.dx ** 2 + self.dy ** 2) ** 0.5

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (int(self.ball1.x), int(self.ball1.y)),
                         (int(self.ball2.x), int(self.ball2.y)), 2)

    def satisfy_constraints(self):
        dx = self.ball2.x - self.ball1.x
        dy = self.ball2.y - self.ball1.y
        distance = max(.001, (dx ** 2 + dy ** 2) ** 0.5)
        difference = self.length - distance
        percent = difference / distance / 2
        dx *= percent
        dy *= percent
        if not self.ball1.fixed:
            self.ball1.x -= dx
            self.ball1.y -= dy
        if not self.ball2.fixed:
            self.ball2.x += dx
            self.ball2.y += dy

    def mouse_collision(self, rods):
        Mouse_X, Mouse_Y = pygame.mouse.get_pos()
        dx = self.ball2.x - self.ball1.x
        dy = self.ball2.y - self.ball1.y
        base = max(.001, (dx ** 2 + dy ** 2) ** 0.5)
        dx = Mouse_X - self.ball1.x
        dy = Mouse_Y - self.ball1.y
        height = max(.001, (dx ** 2 + dy ** 2) ** 0.5)
        area = base * height
        if area < CUT_DIST:
            rods.remove(self)

    def rip_checker(self, rods):
        dx = self.ball2.x - self.ball1.x
        dy = self.ball2.y - self.ball1.y
        distance = ((dx ** 2 + dy ** 2) ** 0.5)
        if distance > TEAR_DIST:
            rods.remove(self)



def buildBalls(n, x, y, px, py, radius, withRods, balls, rods):
    for i in range(n):
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        balls.append(Ball(x, y, px, py, radius, color, False))
        if withRods:
            if i > 0:
                l = max(0, len(balls) - 2)
                rods.append(Rod(balls[l+i-1], balls[l+i]))


def buildBox(color, balls, rods):
    balls.append(Ball(10, 10, 10, 10, 2, color, False))
    balls.append(Ball(70, 10, 70, 10, 2, color, False))
    balls.append(Ball(10, 70, 10, 70, 2, color, False))
    balls.append(Ball(70, 70, 70, 70, 2, color, False))
    rods.append(Rod(balls[0], balls[1]))
    rods.append(Rod(balls[0], balls[2]))
    rods.append(Rod(balls[1], balls[3]))
    rods.append(Rod(balls[2], balls[3]))
    rods.append(Rod(balls[0], balls[3]))
    rods.append(Rod(balls[1], balls[2]))

def buildChain(n, head_x, head_y, dist, radius, color, balls, rods, swing):
    balls.append(Ball(head_x, head_y, head_x, head_y, radius, color, True))
    l = len(balls) - 1
    for i in range(n-1):
        balls.append(Ball(head_x + ((i+1)*swing), head_y + ((i+1)*dist), head_x + ((i+1)*dist), head_y + ((i+1)*dist),
                          radius, color, False))
        rods.append(Rod(balls[l+i], balls[l+i+1]))

def buildMesh(balls, rods, columns, rows):
    for i in range(columns-1):
        for j in range(rows):
            rods.append(Rod(balls[(i*rows)+j], balls[(i*rows)+j+rows]))