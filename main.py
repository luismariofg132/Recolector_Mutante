
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
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recolector Mutante 2.0 - Menú Principal")

DATA_PATH = "data"
PUNTAJES_FILE = os.path.join(DATA_PATH, "puntajes.txt")

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

def draw_text_centered(text, y, color=WHITE):
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y))

def pantalla_menu():
    opciones = ["1. Jugar", "2. Ver Puntajes", "3. Ayuda", "4. Créditos", "5. Salir"]
    seleccion = -1
    while seleccion == -1:
        screen.fill(BLACK)
        draw_text_centered("RECOLECTOR MUTANTE 2.0", 100)
        for i, op in enumerate(opciones):
            draw_text_centered(op, 180 + i * 50)
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
    while True:
        screen.fill(BLACK)
        draw_text_centered("AYUDA", 60)
        draw_text_centered("Usa las flechas para mover al personaje", 120)
        draw_text_centered("Evita obstáculos y recoge estrellas", 160)
        draw_text_centered("Recolecta power-ups (escudo, ralentizador)", 200)
        draw_text_centered("Presiona ESC para volver al menú", 280)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def pantalla_creditos():
    while True:
        screen.fill(BLACK)
        draw_text_centered("CRÉDITOS", 60)
        draw_text_centered("Desarrolladores:", 120)
        draw_text_centered("Luis Mario Franco Gómez", 160)
        draw_text_centered("Lizeth Juliana Barrios Gonzales", 200)
        draw_text_centered("Materia: Computación Gráfica", 240)
        draw_text_centered("Docente: Francisco Alejandro Medina Aguirre", 280)
        draw_text_centered("Presiona ESC para volver al menú", 360)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def pantalla_puntajes():
    while True:
        screen.fill(BLACK)
        draw_text_centered("PUNTAJES", 60)
        if os.path.exists(PUNTAJES_FILE):
            with open(PUNTAJES_FILE, "r") as f:
                lines = f.readlines()[-10:]
            for i, line in enumerate(lines):
                draw_text_centered(line.strip(), 120 + i * 30)
        else:
            draw_text_centered("No hay puntajes guardados.", 150)
        draw_text_centered("Presiona ESC para volver al menú", 500)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def guardar_puntaje(nombre, puntos):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(PUNTAJES_FILE, "a") as f:
        f.write(f"{nombre} - {puntos} pts - {fecha}\n")

# Bucle principal del menú
while True:
    accion = pantalla_menu()
    if accion == "jugar":
        print("Iniciar juego...")
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
