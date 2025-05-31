import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import random


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # Player-asteroid collision
        for asteroid in asteroids:
            if asteroid.collides_with(player):
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

        screen.fill(BG_COLOR)

        for obj in drawable:
            obj.draw(screen)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, SCORE_COLOR)
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
