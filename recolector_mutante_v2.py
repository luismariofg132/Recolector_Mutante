import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recolector Mutante 2.0")
font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.size = 50
        self.pos = [WIDTH // 2, HEIGHT // 2]
        self.lives = 3
        self.has_shield = False

    def draw(self):
        pygame.draw.rect(screen, GREEN, (*self.pos, self.size, self.size))
        if self.has_shield:
            pygame.draw.rect(screen, YELLOW, (*self.pos, self.size, self.size), 3)

    def move(self, dx, dy):
        self.pos[0] = max(0, min(WIDTH - self.size, self.pos[0] + dx))
        self.pos[1] = max(0, min(HEIGHT - self.size, self.pos[1] + dy))

class Star:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)
        self.spawn_time = time.time()

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

class PowerUp:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)
        self.kind = random.choice(["shield", "slow"])

    def draw(self):
        color = YELLOW if self.kind == "shield" else PURPLE
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))

class Obstacle:
    def __init__(self, speed):
        self.size = 40
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)
        self.dx = random.choice([-1, 1]) * speed
        self.dy = random.choice([-1, 1]) * speed

    def move(self, speed_mod):
        self.x += self.dx * speed_mod
        self.y += self.dy * speed_mod
        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT - self.size:
            self.dy *= -1

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

class Game:
    def __init__(self):
        self.player = Player()
        self.stars = []
        self.power_ups = []
        self.obstacles = []
        self.rules = {
            "player_speed": 5,
            "obstacle_speed": 3,
            "invert_controls": False,
            "num_obstacles": 3
        }
        self.level = 1
        self.score = 0
        self.score_to_advance = 5
        self.max_levels = 5
        self.level_time_limit = 30
        self.start_time = 0
        self.slow_obstacles = False
        self.slow_timer = 0

    def spawn_star(self):
        self.stars.append(Star())

    def spawn_power_up(self):
        if random.random() < 0.3:
            self.power_ups.append(PowerUp())

    def spawn_obstacles(self):
        self.obstacles.clear()
        for _ in range(self.rules["num_obstacles"]):
            self.obstacles.append(Obstacle(self.rules["obstacle_speed"]))

    def draw_info(self):
        info = font.render(f"Nivel: {self.level}  Puntos: {self.score}  Objetivo: {self.level * self.score_to_advance}  Vidas: {self.player.lives}", True, WHITE)
        screen.blit(info, (20, 20))
        if self.rules["invert_controls"]:
            inv = font.render("Controles invertidos ACTIVOS", True, RED)
            screen.blit(inv, (20, 60))
        tiempo_restante = max(0, int(self.level_time_limit - (time.time() - self.start_time)))
        timer_text = font.render(f"Tiempo restante: {tiempo_restante}s", True, WHITE)
        screen.blit(timer_text, (20, 100))

    def check_collisions(self):
        px, py = self.player.pos
        for star in self.stars[:]:
            if (px < star.x + star.size and px + self.player.size > star.x and
                py < star.y + star.size and py + self.player.size > star.y):
                self.stars.remove(star)
                elapsed = time.time() - star.spawn_time
                self.score += 3 if elapsed <= 5 else 1

        for obs in self.obstacles:
            if (px < obs.x + obs.size and px + self.player.size > obs.x and
                py < obs.y + obs.size and py + self.player.size > obs.y):
                if self.player.has_shield:
                    self.player.has_shield = False
                else:
                    self.player.lives -= 1
                return True

        for pu in self.power_ups[:]:
            if (px < pu.x + pu.size and px + self.player.size > pu.x and
                py < pu.y + pu.size and py + self.player.size > pu.y):
                self.power_ups.remove(pu)
                if pu.kind == "shield":
                    self.player.has_shield = True
                elif pu.kind == "slow":
                    self.slow_obstacles = True
                    self.slow_timer = time.time()
        return False

    def mutate_rules(self):
        mutation = random.choice(list(self.rules.keys()))
        if mutation == "invert_controls":
            self.rules[mutation] = not self.rules[mutation]
        else:
            self.rules[mutation] += 1

    def run_level(self):
        clock = pygame.time.Clock()
        self.player.pos = [WIDTH // 2, HEIGHT // 2]
        self.stars.clear()
        self.power_ups.clear()
        self.spawn_obstacles()
        for _ in range(self.level * self.score_to_advance):
            self.spawn_star()
        self.spawn_power_up()
        self.start_time = time.time()

        while True:
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]: dx -= self.rules["player_speed"]
            if keys[pygame.K_RIGHT]: dx += self.rules["player_speed"]
            if keys[pygame.K_UP]: dy -= self.rules["player_speed"]
            if keys[pygame.K_DOWN]: dy += self.rules["player_speed"]
            if self.rules["invert_controls"]:
                dx, dy = -dx, -dy
            self.player.move(dx, dy)
            for obs in self.obstacles:
                obs.move(0.5 if self.slow_obstacles else 1)
            if self.check_collisions() and self.player.lives <= 0:
                return False
            if time.time() - self.start_time > self.level_time_limit:
                self.player.lives -= 1
                return self.player.lives > 0
            if self.slow_obstacles and (time.time() - self.slow_timer > 5):
                self.slow_obstacles = False

            self.player.draw()
            for star in self.stars:
                star.draw()
            for pu in self.power_ups:
                pu.draw()
            for obs in self.obstacles:
                obs.draw()
            self.draw_info()
            pygame.display.flip()
            clock.tick(60)
            if not self.stars:
                return True

    def main_loop(self):
        # Intro
        screen.fill(BLACK)
        intro_text = font.render("\u00a1Bienvenido a Recolector Mutante 2.0!", True, WHITE)
        screen.blit(intro_text, (WIDTH // 2 - 220, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(2000)

        for i in range(3, 0, -1):
            screen.fill(BLACK)
            count_text = font.render(f"Empieza en... {i}", True, WHITE)
            screen.blit(count_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)

        while self.level <= self.max_levels and self.player.lives > 0:
            if self.run_level():
                self.mutate_rules()
                self.level += 1

        screen.fill(BLACK)
        msg = font.render("\u00a1Juego Terminado!", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()

# if __name__ == "__main__":
#     Game().main_loop()
