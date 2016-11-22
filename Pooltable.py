# The beginnings of a basic Pool game in Pygame
# Runs in Python 2.7 and needs a lot more work
# Ben Woodfield

'''
 I found something ver similar amongst a repo of random code, and liked the 
 look of it so I wrote it out for myself and tweaked a few things. So as it
 is now, the balls have physical interaction and movement with eachother,
 but any color ball can be clicked and launched. Poolballs will bounce off
 eachother and the table edges, and a ball will disappear when it collides
 with one of the pockets.
 
 To Do:
 
 Add a scoring system (different color balls have different point values)
 Only allow user interaction with the White Ball
 Have a cue widget that collides with the white ball only
 Cue widget to have angular direction from a fixed point 
 Enable a fouling system -Basically add the rules of a Pool Game :s
 
'''

import pygame
import random
import math

pygame.init()

BG_COLOR = (102, 140, 93)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
(SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)
BALL_RADIUS = 20
POCKET_RADIUS = 23
DRAG = 0.999
ELASTICITY = 0.9

def collide(b1, b2):
    dx = b1.x - b2.x
    dy = b1.y - b2.y
        
    distance = math.hypot(dx, dy)
    if distance <= 2 * BALL_RADIUS:
        tangent = math.atan2(dy, dx) + math.pi / 2
        angle = tangent - math.pi / 2

        if b1.speed == 0:
            angle2 = math.atan2(math.sin(angle), 1 + math.cos(angle))
            angle1 = (math.pi - angle) / 2
            speed2 = (b2.speed * math.sqrt((1 + math.cos(angle)) / 2)) * ELASTICITY
            speed1 = (b2.speed * math.sin(angle / 2)) * ELASTICITY
        elif b2.speed == 0:
            angle1 = math.atan2(math.sin(angle), 1 + math.cos(angle))
            angle2 = (math.pi - angle) / 2
            speed1 = (b1.speed * math.sqrt((1 + math.cos(angle)) / 2)) * ELASTICITY
            speed2 = (b1.speed * math.sin(angle / 2)) * ELASTICITY
        else:
            vx1_after = b2.speed * math.cos(b2.angle - angle) * math.cos(angle) + b1.speed * math.sin(b1.angle - angle) * math.cos(angle + math.pi / 2)
            vy1_after = b2.speed * math.cos(b2.angle - angle) * math.sin(angle) + b1.speed * math.sin(b1.angle - angle) * math.sin(angle + math.pi / 2)
            vx2_after = b1.speed * math.cos(b1.angle - angle) * math.cos(angle) + b2.speed * math.sin(b2.angle - angle) * math.cos(angle + math.pi / 2)
            vy2_after = b1.speed * math.cos(b1.angle - angle) * math.sin(angle) + b2.speed * math.sin(b2.angle - angle) * math.sin(angle + math.pi / 2)
            angle1 = math.atan2(vy1_after, vx1_after)
            angle2 = math.atan2(vy2_after, vx2_after)
            speed1 = (vx1_after / math.cos(angle1)) * ELASTICITY
            speed2 = (vx2_after / math.cos(angle2)) * ELASTICITY
        
        (b1.angle, b1.speed) = (angle1, speed1)
        (b2.angle, b2.speed) = (angle2, speed2)

        overlap = 2 * BALL_RADIUS - distance + 1
        b1.x += math.cos(angle) * 0.5 * overlap
        b1.y += math.sin(angle) * 0.5 * overlap
        b2.x -= math.cos(angle) * 0.5 * overlap
        b2.y -= math.sin(angle) * 0.5 * overlap

def find_ball((mouse_x, mouse_y)):
    for ball in balls:
        if math.hypot(ball.x - mouse_x, ball.y - mouse_y) <= BALL_RADIUS:
            i = balls.index(ball)
            return balls[i]

class Ball():
    def __init__(self, (x, y), color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0
        self.angle = 0

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= DRAG

    def bounce(self):
        if self.x > SCREEN_WIDTH - BALL_RADIUS:
            self.x = 2 * (SCREEN_WIDTH - BALL_RADIUS) - self.x
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY
        elif self.x < BALL_RADIUS:
            self.x = 2 * BALL_RADIUS - self.x
            self.angle = math.pi - self.angle
            self.speed *= ELASTICITY

        if self.y > SCREEN_HEIGHT - BALL_RADIUS:
            self.y = 2 * (SCREEN_HEIGHT - BALL_RADIUS) - self.y
            self.angle = -self.angle
            self.speed *= ELASTICITY
        elif self.y < BALL_RADIUS:
            self.y = 2 * BALL_RADIUS - self.y
            self.angle = -self.angle
            self.speed *= ELASTICITY

    def is_destroyed(self):
        for pocket in pockets:
            if self.x > pocket .x - BALL_RADIUS / 2 and self.x < pocket .x + BALL_RADIUS / 2 and self.y > pocket .y - BALL_RADIUS / 2 and self.y < pocket .y + BALL_RADIUS / 2:
                i = balls.index(self)
                del balls[i]

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

class Pocket():
    def __init__(self, (x, y)):
        self.x = x
        self.y = y
        self.color = BLACK

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), POCKET_RADIUS)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pool table particle system')

balls = []
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), WHITE))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), BLACK))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (227, 205, 170)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (170, 192, 227)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (170, 227, 201)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (227, 170, 196)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (143, 50, 92)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (106, 50, 143)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (59, 47, 194)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (182, 194, 47)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (194, 113, 47)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (47, 128, 194)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (56, 92, 102)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (102, 56, 56)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (66, 242, 17)))
x = random.randint(2 * POCKET_RADIUS + BALL_RADIUS, SCREEN_WIDTH - 2 * POCKET_RADIUS - BALL_RADIUS)
y = random.randint(2 * BALL_RADIUS + BALL_RADIUS, SCREEN_HEIGHT - 2 * POCKET_RADIUS - BALL_RADIUS)
balls.append(Ball((x, y), (193, 17, 242)))

pockets = []
pockets.append(Pocket((POCKET_RADIUS, POCKET_RADIUS)))
pockets.append(Pocket((SCREEN_WIDTH - POCKET_RADIUS, POCKET_RADIUS)))
pockets.append(Pocket((POCKET_RADIUS, SCREEN_HEIGHT - POCKET_RADIUS)))
pockets.append(Pocket((SCREEN_WIDTH - POCKET_RADIUS, SCREEN_HEIGHT - POCKET_RADIUS)))
pockets.append(Pocket((SCREEN_WIDTH / 2, POCKET_RADIUS)))
pockets.append(Pocket((SCREEN_WIDTH / 2, SCREEN_HEIGHT - POCKET_RADIUS)))

selected_ball = None
mouse_coords = (0, 0)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            selected_ball = find_ball((mouse_x, mouse_y))
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_ball = None

    if selected_ball:
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        dx = mouse_x - selected_ball.x
        dy = mouse_y - selected_ball.y
        selected_ball.angle = math.atan2(dy, dx)
        selected_ball.speed = math.hypot(dx, dy) * 0.1

    screen.fill(BG_COLOR)

    for pocket in pockets:
        pocket.display()

    for i, ball1 in enumerate(balls):
        ball1.move()
        ball1.bounce()
        for ball2 in balls[i + 1:]:
            collide(ball1, ball2)
        ball1.is_destroyed()
        ball1.display()

    pygame.display.flip()

pygame.quit()
