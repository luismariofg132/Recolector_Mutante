import pygame
import sys
import random
import time
import os
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recolector Mutante 2.0")
font_path = "./assets/Audiowide-Regular.ttf"
font = pygame.font.Font(font_path, 28)


BACKGROUND_PATH = "./assets/background.png"
background = pygame.image.load(BACKGROUND_PATH)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

MUSIC_PATH = "./assets/song.mp3"
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def guardar_puntaje(puntos):
    """
    Guarda el puntaje obtenido en el archivo 'puntajes.txt', junto con la fecha y hora actual.

    Parámetros:
    - puntos (int): Puntuación obtenida por el jugador.
    """
    ruta = os.path.join("data", "puntajes.txt")
    if not os.path.exists("data"):
        os.makedirs("data")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(ruta, "a") as f:
        f.write(f"{puntos} pts - {fecha}\n")

class Player:
    """
    Representa al jugador dentro del juego.
    Controla la posición, vidas, escudo y renderizado del personaje.
    """
    def __init__(self):
        self.size = 50
        self.pos = [WIDTH // 2, (HEIGHT + UI_HEIGHT) // 2]
        self.lives = 3
        self.has_shield = False
        self.image = pygame.image.load("./assets/collector.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, immune=False):
        """
        Dibuja al jugador en pantalla, con efecto de parpadeo si es inmune y con borde si tiene escudo.

        Parámetros:
        - immune (bool): Indica si el jugador está en estado de inmunidad (parpadea si es True).
        """
        if immune:
            # Parpadea solo si ha pasado un número impar de décimas de segundo
            ticks = pygame.time.get_ticks() // 100
            if ticks % 2 == 0:
                return  # No dibuja este frame → efecto parpadeo

        screen.blit(self.image, self.pos)

        if self.has_shield:
            pygame.draw.rect(screen, YELLOW, (*self.pos, self.size, self.size), 3)


    def move(self, dx, dy):
        """
        Mueve al jugador en el eje X e Y respetando los límites de la pantalla.

        Parámetros:
        - dx (int): Desplazamiento en el eje X.
        - dy (int): Desplazamiento en el eje Y.
        """

        self.pos[0] = max(0, min(WIDTH - self.size, self.pos[0] + dx))
        self.pos[1] = max(UI_HEIGHT, min(HEIGHT - self.size, self.pos[1] + dy))

class Star:
    """
    Representa una estrella que el jugador puede recolectar para obtener puntos.
    """

    def __init__(self):
        """
        Inicializa una estrella con posición aleatoria y registra su tiempo de aparición.
        Carga la imagen correspondiente.
        """
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(UI_HEIGHT, HEIGHT - self.size)
        self.spawn_time = time.time()
        self.image = pygame.image.load("./assets/start.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self):
        """Dibuja la estrella en pantalla."""
        screen.blit(self.image, (self.x, self.y))

class PowerUp:
    """
    Representa un potenciador que puede otorgar un escudo o ralentizar los obstáculos.
    """
    def __init__(self):
        """
        Inicializa un PowerUp con tipo aleatorio ('shield' o 'slow') y posición aleatoria.
        Carga la imagen correspondiente.
        """
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(UI_HEIGHT, HEIGHT - self.size)
        self.kind = random.choice(["shield", "slow"])
        filename = "shield.png" if self.kind == "shield" else "slow.png"
        self.image = pygame.image.load(f"./assets/{filename}")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


    def draw(self):
        """Dibuja el PowerUp en pantalla."""
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    """
    Representa un obstáculo móvil que el jugador debe evitar.
    """
    def __init__(self, speed):
        """
        Inicializa el obstáculo con una velocidad y dirección aleatoria.

        Parámetros:
        - speed (int): Velocidad del obstáculo.
        """
        self.size = 40
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(UI_HEIGHT, HEIGHT - self.size)
        self.dx = random.choice([-1, 1]) * speed
        self.dy = random.choice([-1, 1]) * speed
        self.image = pygame.image.load("./assets/obstacle.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move(self, speed_mod):
        """
        Mueve el obstáculo por la pantalla y rebota en los bordes.

        Parámetros:
        - speed_mod (float): Modificador de velocidad (por ejemplo, para ralentizar).
        """
        self.x += self.dx * speed_mod
        self.y += self.dy * speed_mod
        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.dx *= -1
        if self.y <= UI_HEIGHT or self.y >= HEIGHT - self.size:
            self.dy *= -1

    def draw(self):
        """Dibuja el obstáculo en pantalla."""
        screen.blit(self.image, (self.x, self.y))

class Game:
    """
    Controlador principal del juego. Maneja la lógica del flujo del juego,
    niveles, eventos, colisiones y renderizado.
    """
    def __init__(self):
        """
        Inicializa el juego: jugador, listas de objetos, reglas, nivel y puntaje.
        """
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
        self.immunity_start_time = 0
        self.immunity_duration = 3

    def spawn_star(self):
        """Agrega una nueva estrella al juego."""
        self.stars.append(Star())

    def spawn_power_up(self):
        """Agrega aleatoriamente un PowerUp al juego con probabilidad del 30%."""
        if random.random() < 0.3:
            self.power_ups.append(PowerUp())

    def spawn_obstacles(self):
        """Genera una nueva lista de obstáculos según las reglas del nivel actual."""
        self.obstacles.clear()
        for _ in range(self.rules["num_obstacles"]):
            self.obstacles.append(Obstacle(self.rules["obstacle_speed"]))

    def draw_info(self):
        """
        Muestra la interfaz de información: nivel, puntaje, objetivo, tiempo restante,
        vidas del jugador y si los controles están invertidos.
        """
        # Fondo redondeado para la barra de información
        info_bg_rect = pygame.Rect(10, 10, WIDTH - 20, UI_HEIGHT - 20)
        pygame.draw.rect(screen, (20, 20, 20), info_bg_rect, border_radius=15)
        pygame.draw.rect(screen, (80, 80, 80), info_bg_rect, 2, border_radius=15)

        # Mostrar corazones como vidas
        heart_img = pygame.image.load("./assets/heart.png")
        heart_img = pygame.transform.scale(heart_img, (30, 30))
        for i in range(self.player.lives):
            screen.blit(heart_img, (WIDTH - 40 * (i + 1), 20))

        # Texto estilizado
        nivel_text = font.render(f"Nivel: {self.level}", True, WHITE)
        puntos_text = font.render(f"Puntos: {self.score}", True, WHITE)
        objetivo_text = font.render(f"Objetivo: {self.level * self.score_to_advance}", True, WHITE)
        tiempo_restante = max(0, int(self.level_time_limit - (time.time() - self.start_time)))
        tiempo_text = font.render(f"Tiempo: {tiempo_restante}s", True, WHITE)

        # Posicionar textos
        screen.blit(nivel_text, (30, 20))
        screen.blit(puntos_text, (30, 55))
        screen.blit(objetivo_text, (250, 20))
        screen.blit(tiempo_text, (250, 55))

        # Aviso si controles invertidos
        if self.rules["invert_controls"]:
            inv_text = font.render("Controles invertidos ACTIVOS", True, RED)
            screen.blit(inv_text, (30, 90))


    def check_collisions(self):
        """
        Verifica colisiones entre el jugador y estrellas, obstáculos o PowerUps.
        Aplica efectos como pérdida de vida, inmunidad, escudo o ralentización.

        Retorna:
        - bool: Siempre False (puede ser útil para señales futuras).
        """

        px, py = self.player.pos
        now = time.time()
        immune = now - self.immunity_start_time < self.immunity_duration

        for star in self.stars[:]:
            if (px < star.x + star.size and px + self.player.size > star.x and
                py < star.y + star.size and py + self.player.size > star.y):
                self.stars.remove(star)
                elapsed = time.time() - star.spawn_time
                self.score += 3 if elapsed <= 5 else 1

        for obs in self.obstacles:
            if (px < obs.x + obs.size and px + self.player.size > obs.x and
                py < obs.y + obs.size and py + self.player.size > obs.y):
                if immune:
                    continue
                if self.player.has_shield:
                    self.player.has_shield = False
                else:
                    self.player.lives -= 1
                    self.immunity_start_time = now  # ← Corrección aquí

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
        """
        Realiza una mutación aleatoria en las reglas del juego:
        aumenta velocidad, número de obstáculos o invierte controles.
        """
        mutation = random.choice(list(self.rules.keys()))
        if mutation == "invert_controls":
            self.rules[mutation] = not self.rules[mutation]
        else:
            self.rules[mutation] += 1

    def run_level(self):
        """
        Ejecuta un nivel completo del juego.

        Retorna:
        - bool: True si se completó el nivel, False si se pierde una vida o termina el juego.
        """
        clock = pygame.time.Clock()
        self.player.pos = [WIDTH // 2, (HEIGHT + UI_HEIGHT) // 2]
        self.stars.clear()
        self.power_ups.clear()
        self.spawn_obstacles()
        for _ in range(self.level * self.score_to_advance):
            self.spawn_star()
        self.spawn_power_up()
        self.start_time = time.time()
        self.immunity_start_time = time.time()

        while True:
            screen.blit(background, (0, 0))
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, UI_HEIGHT))

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

            self.check_collisions()

            if time.time() - self.start_time > self.level_time_limit:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    return False
                else:
                    return True

            if self.slow_obstacles and (time.time() - self.slow_timer > 5):
                self.slow_obstacles = False

            immune = (time.time() - self.immunity_start_time) < self.immunity_duration
            self.player.draw(immune)
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

            if self.player.lives <= 0:
                # Mostrar pantalla de colisión antes de terminar
                screen.blit(background, (0, 0))
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, UI_HEIGHT))
                immune = (time.time() - self.immunity_start_time) < self.immunity_duration
                self.player.draw(immune)

                for obs in self.obstacles:
                    obs.draw()
                for star in self.stars:
                    star.draw()
                for pu in self.power_ups:
                    pu.draw()
                self.draw_info()
                pygame.display.flip()
                pygame.time.delay(1000)  # Espera 1 segundo para mostrar que perdió la vida
                return False


    def main_loop(self):
        """
        Bucle principal del juego. Maneja la presentación inicial,
        la ejecución de niveles y el final del juego.
        Guarda el puntaje final al terminar.
        """
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, UI_HEIGHT))
        sub_text = font.render("Prepárate para recolectar... ¡y sobrevivir!", True, WHITE)
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        screen.blit(sub_text, sub_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

        for i in range(3, 0, -1):
            screen.blit(background, (0, 0))
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, UI_HEIGHT))
            count_text = font.render(f"Empieza en... {i}", True, WHITE)
            screen.blit(count_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)

        while self.level <= self.max_levels and self.player.lives > 0:
            if self.run_level():
                self.mutate_rules()
                self.level += 1

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, UI_HEIGHT))
        msg = font.render("\u00a1Juego Terminado!", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)

        guardar_puntaje(self.score)

        pygame.quit()

if __name__ == "__main__":
    Game().main_loop()
