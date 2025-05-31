import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import random


class PowerUp:
    def __init__(self, x, y, kind="rapid"):
        self.position = pygame.Vector2(x, y)
        self.radius = 15
        self.active = True
        self.kind = kind  # "rapid", "shield", "speed", "bigshot"

    def draw(self, screen):
        color = (0, 255, 0)
        if self.kind == "shield":
            color = (0, 200, 255)
        elif self.kind == "speed":
            color = (255, 0, 255)
        elif self.kind == "bigshot":
            color = (255, 128, 0)
        pygame.draw.circle(screen, color, self.position, self.radius)
        pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius, 3)

    def collides_with(self, player):
        return self.position.distance_to(player.position) < (self.radius + player.radius)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)  # For score display

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    score = 0
    dt = 0
    powerup = None
    powerup_given = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # Power-up spawn logic
        if not powerup_given and score >= 100:
            kind = random.choice(["rapid", "shield", "speed", "bigshot"])
            powerup = PowerUp(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, kind)
            powerup_given = True

        # Player-asteroid collision
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if hasattr(player, "shielded") and player.shielded:
                    asteroid.kill()
                    continue
                print("Game over! Final Score:", score)
                sys.exit()

        # Bullet-asteroid collision
        for asteroid in asteroids.copy():
            for shot in shots.copy():
                if asteroid.collides_with(shot):
                    old_radius = asteroid.radius
                    if old_radius > ASTEROID_MIN_RADIUS:
                        random_angle = random.uniform(20, 50)
                        v1 = asteroid.velocity.rotate(random_angle) * 1.2
                        v2 = asteroid.velocity.rotate(-random_angle) * 1.2
                        new_radius = old_radius - ASTEROID_MIN_RADIUS
                        a1 = Asteroid(asteroid.position.x, asteroid.position.y, new_radius)
                        a2 = Asteroid(asteroid.position.x, asteroid.position.y, new_radius)
                        a1.velocity = v1
                        a2.velocity = v2
                    asteroid.kill()
                    shot.kill()
                    score += 100  # Add points for destroying an asteroid

        # Power-up collection
        if powerup and powerup.active and powerup.collides_with(player):
            if powerup.kind == "rapid":
                player.powered_up = True
                player.powerup_time = pygame.time.get_ticks()
            elif powerup.kind == "shield":
                player.shielded = True
                player.shield_time = pygame.time.get_ticks()
            elif powerup.kind == "speed":
                player.speed_boost = True
                player.speed_time = pygame.time.get_ticks()
            elif powerup.kind == "bigshot":
                player.bigshot = True
                player.bigshot_time = pygame.time.get_ticks()
            powerup.active = False
            print(f"Power-up collected: {powerup.kind}!")

        # Power-up durations (5 seconds each)
        now = pygame.time.get_ticks()
        if hasattr(player, "powered_up") and player.powered_up:
            if now - player.powerup_time > 5000:
                player.powered_up = False
        if hasattr(player, "shielded") and player.shielded:
            if now - player.shield_time > 5000:
                player.shielded = False
        if hasattr(player, "speed_boost") and player.speed_boost:
            if now - player.speed_time > 5000:
                player.speed_boost = False
        if hasattr(player, "bigshot") and player.bigshot:
            if now - player.bigshot_time > 5000:
                player.bigshot = False

        screen.fill(BG_COLOR)

        for obj in drawable:
            obj.draw(screen)

        # Draw power-up if active
        if powerup and powerup.active:
            powerup.draw(screen)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, SCORE_COLOR)
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
