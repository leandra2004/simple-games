import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alien Invasion")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Define spaceship and bullet classes
class Ship:
    def __init__(self):
        self.x = screen_width / 2
        self.y = screen_height - 60
        self.width = 50
        self.height = 50
        self.speed = 5
        self.image = pygame.image.load("spaceship.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self, left, right):
        if left and self.x > 0:
            self.x -= self.speed
        if right and self.x < screen_width - self.width:
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 7
        self.color = green

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 1
        self.image = pygame.image.load("Alien.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Initialize game objects
ship = Ship()
bullets = []
aliens = []
alien_speed = 1
score = 0
font = pygame.font.SysFont("Arial", 30)

# Main game loop
running = True
left = right = False
clock = pygame.time.Clock()

while running:
    screen.fill(black)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_SPACE:
                bullet = Bullet(ship.x + ship.width // 2 - 2, ship.y)
                bullets.append(bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False

    # Move ship and bullets
    ship.move(left, right)
    for bullet in bullets[:]:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)

    # Create aliens
    if random.randint(1, 60) == 1:
        alien = Alien(random.randint(0, screen_width - 50), -50)
        aliens.append(alien)

    # Move and draw aliens
    for alien in aliens[:]:
        alien.move()
        alien.draw()
        if alien.y > screen_height:
            aliens.remove(alien)
        if alien.x < ship.x + ship.width and alien.x + alien.width > ship.x and alien.y + alien.height > ship.y:
            running = False

    # Collision detection
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if alien.x < bullet.x < alien.x + alien.width and alien.y < bullet.y < alien.y + alien.height:
                aliens.remove(alien)
                bullets.remove(bullet)
                score += 1

    # Draw everything
    ship.draw()
    for bullet in bullets:
        bullet.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()