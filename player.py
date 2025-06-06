import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_COLOR


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0
        self.shoot_timer = 0.0  # Timer for shooting cooldown

    def draw(self, screen):
        pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        keys = pygame.key.get_pressed()
        speed = PLAYER_SPEED
        if hasattr(self, "speed_boost") and self.speed_boost:
            speed *= 2
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt, speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt, speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        cooldown = PLAYER_SHOOT_COOLDOWN
        if hasattr(self, "powered_up") and self.powered_up:
            cooldown = PLAYER_SHOOT_COOLDOWN / 3
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot_timer = cooldown
            self.shoot()

    def shoot(self):
        from constants import SHOT_RADIUS
        shot = Shot(self.position.x, self.position.y)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        if hasattr(self, "bigshot") and self.bigshot:
            shot.radius = SHOT_RADIUS * 2  # Make the bullet bigger
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN  # Reset cooldown

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt, speed=None):
        if speed is None:
            speed = PLAYER_SPEED
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * speed * dt
