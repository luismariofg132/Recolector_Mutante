import pygame
import sys
import os
from datetime import datetime
from recolector_mutante_v2 import Game

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
MINT = (80, 211, 172)  # Color #50D3AC

# Fuente personalizada
font_path = os.path.join("assets", "Audiowide-Regular.ttf")
font = pygame.font.Font(font_path, 32)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recolector Mutante 2.0 - Menú Principal")

DATA_PATH = "data"
PUNTAJES_FILE = os.path.join(DATA_PATH, "puntajes.txt")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

def draw_text_centered(text, y, color=WHITE, bg=None):
    """
    Dibuja un texto centrado horizontalmente en la pantalla.

    Parámetros:
    - text (str): Texto a mostrar.
    - y (int): Coordenada vertical (eje Y) donde centrar el texto.
    - color (tuple): Color del texto (por defecto: blanco).
    - bg (tuple): Color de fondo del texto (por defecto: None, es transparente).
    """
    text_surf = font.render(text, True, color, bg)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surf, text_rect)

def dibujar_fondo_con_marco():
    """
    Dibuja el fondo del menú con un marco decorativo.
    Se utiliza en todas las pantallas del menú principal.
    """
    screen.fill((10, 10, 10))
    pygame.draw.rect(screen, (30, 30, 30), (50, 50, WIDTH - 100, HEIGHT - 100), border_radius=20)
    pygame.draw.rect(screen, (80, 80, 80), (50, 50, WIDTH - 100, HEIGHT - 100), 2, border_radius=20)

def pantalla_menu():
    """
    Muestra la pantalla del menú principal con opciones de navegación.

    Retorna:
    - str: La acción seleccionada por el usuario ('jugar', 'puntajes', 'ayuda', 'creditos' o 'salir').
    """
    opciones = ["1. Jugar", "2. Ver Puntajes", "3. Ayuda", "4. Créditos", "5. Salir"]
    seleccion = -1
    while seleccion == -1:
        dibujar_fondo_con_marco()
        draw_text_centered("RECOLECTOR MUTANTE 2.0", 120, color=(255, 255, 0))
        for i, op in enumerate(opciones):
            draw_text_centered(op, 200 + i * 50, color=MINT)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "jugar"
                elif event.key == pygame.K_2:
                    return "puntajes"
                elif event.key == pygame.K_3:
                    return "ayuda"
                elif event.key == pygame.K_4:
                    return "creditos"
                elif event.key == pygame.K_5 or event.key == pygame.K_ESCAPE:
                    return "salir"

def pantalla_ayuda():
    """
    Muestra la pantalla de ayuda con instrucciones del juego.
    Permite regresar al menú principal presionando ESC.
    """
    while True:
        dibujar_fondo_con_marco()
        draw_text_centered("AYUDA", 80, color=(0, 255, 255))
        draw_text_centered("Usa las flechas para mover al personaje", 140, color=MINT)
        draw_text_centered("Evita obstáculos y recoge estrellas", 180, color=MINT)
        draw_text_centered("Recolecta power-ups (escudo, ralentizador)", 220, color=MINT)
        draw_text_centered("Presiona ESC para volver al menú", 320, color=GRAY)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def pantalla_creditos():
    """
    Muestra los créditos del juego incluyendo los desarrolladores y el docente.
    Permite regresar al menú principal presionando ESC.
    """

    while True:
        dibujar_fondo_con_marco()
        draw_text_centered("CRÉDITOS", 80, color=(255, 100, 200))
        draw_text_centered("Desarrolladores:", 140, color=MINT)
        draw_text_centered("Luis Mario Franco Gómez", 180, color=MINT)
        draw_text_centered("Lizeth Juliana Barrios Gonzales", 220, color=MINT)
        draw_text_centered("Materia: Computación Gráfica", 260, color=MINT)
        draw_text_centered("Docente: Francisco Alejandro Medina Aguirre", 300, color=MINT)
        draw_text_centered("Presiona ESC para volver al menú", 380, color=GRAY)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def pantalla_puntajes():
    """
    Muestra la pantalla de puntajes guardados.
    Carga y muestra los últimos 10 puntajes desde el archivo 'puntajes.txt'.
    Permite regresar al menú principal presionando ESC.
    """
    while True:
        dibujar_fondo_con_marco()
        draw_text_centered("PUNTAJES", 80, color=(0, 255, 0))
        if os.path.exists(PUNTAJES_FILE):
            with open(PUNTAJES_FILE, "r") as f:
                lines = f.readlines()[-10:]
            for i, line in enumerate(lines):
                draw_text_centered(line.strip(), 140 + i * 30)
        else:
            draw_text_centered("No hay puntajes guardados.", 150)
        draw_text_centered("Presiona ESC para volver al menú", 500, color=GRAY)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def guardar_puntaje(nombre, puntos):
    """
    Guarda un nuevo puntaje en el archivo 'puntajes.txt'.

    Parámetros:
    - nombre (str): Nombre del jugador.
    - puntos (int): Puntos obtenidos por el jugador.
    """
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(PUNTAJES_FILE, "a") as f:
        f.write(f"{nombre} - {puntos} pts - {fecha}\n")

# Bucle principal del menú
while True:
    accion = pantalla_menu()
    if accion == "jugar":
        juego = Game()
        juego.main_loop()
        break
    elif accion == "puntajes":
        pantalla_puntajes()
    elif accion == "ayuda":
        pantalla_ayuda()
    elif accion == "creditos":
        pantalla_creditos()
    elif accion == "salir":
        pygame.quit(); sys.exit()
