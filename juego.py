"""
 Descargar Pygame desde pip
"""
import pygame
from random import *
import math
from pygame import mixer

# Iniciar el juego
pygame.init()

# Establecer el tamaño de la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Configuraciones titulo, icono
pygame.display.set_caption('Guerra en el espacio')
icono = pygame.image.load('img/icono.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('img/Fondo.jpg')

# Agregar musica
mixer.music.load('sonido/MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Crear jugador
jugador = pygame.image.load('img/nave.png')
# Calculo para organizarlo en la posición que quiero
# X = 800 / 2 - tamaño icono
# Y = 600 - tamaño
# Posición inicial
jugador_x = 368
jugador_y = 536
# Posición que cambia con las flechas
jugador_x_cambio = 0
jugador_y_cambio = 0

# Crear enemigo
enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10

for e in range(cantidad_enemigos):
    # Crear enemigo
    enemigo.append(pygame.image.load('img/enemigo.png'))
    enemigo_x.append(randint(0, 736))
    enemigo_y.append(randint(50, 200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)


# Crear bala
bala = pygame.image.load('img/bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1
visibilad = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10


# Mostrar texto
def mostrar_texto(x,y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Función jugador posición
def jugador_posicion(x, y):
    pantalla.blit(jugador, (x, y))


# Enemigo
def enemigo_posicion(x, y, ene):
    pantalla.blit(enemigo[ene], (x, y))


# Bala
def disparar_bala(x, y):
    global visibilad
    visibilad = True
    pantalla.blit(bala, (x + 16, y + 10))


# Distancia entre los objetos
def distancia(x1,y1, x2, y2):
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if d < 30:
        return True
    else:
        return False


# Texto final juego
fuente_final = pygame.font.Font('freesansbold.ttf', 38)


def final_juego():
    font_finaly = fuente_final.render(f'Final del juego \n tu puntaje fue de: {puntaje}', True, (255, 255, 255))
    pantalla.blit(font_finaly, (60, 200))


# Evento quit para salir
ejecutar = True
while ejecutar:
    # fondo RGB
    # pantalla.fill((205, 144, 228))
    # Fondo imagen
    pantalla.blit(fondo, (0, 0))
    mostrar_texto(texto_x, texto_y)

    # Loop para mostrar la pantalla y otros
    for evento in pygame.event.get():
        # Cerrar pantalla
        if evento.type == pygame.QUIT:
            ejecutar = False

        # Evento para mover el personaje mediante las flechas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            if evento.key == pygame.K_UP:
                jugador_y_cambio = -0.2
            if evento.key == pygame.K_DOWN:
                jugador_y_cambio = 0.2

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('sonido/disparo.mp3')
                sonido_bala.play()
                if not visibilad:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento para dejar quieto el personaje cuando se suelte la flecha
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT or evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                jugador_x_cambio = 0
                jugador_y_cambio = 0

    # Mostrar jugador y moviemiento
    jugador_x += jugador_x_cambio
    jugador_y += jugador_y_cambio
    # Mantener dentro de la pantalla jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    elif jugador_y >= 536:
        jugador_y = 536

    # Mostrar enemigo y moviemiento
    for e in range(cantidad_enemigos):
        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            final_juego()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener dentro de la pantalla enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 768:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colisión
        colision = distancia(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            bala_y = 500
            visibilad = False
            puntaje += 1
            enemigo_x[e] = randint(0, 736)
            enemigo_y[e] = randint(50, 200)
            sonido_colision = mixer.Sound('sonido/Golpe.mp3')
            sonido_colision.play()

        enemigo_posicion(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= -24:
        bala_y = 500
        visibilad = False
    if visibilad:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador_posicion(jugador_x, jugador_y)

    # Actualizar la pantalla siempre
    pygame.display.update()


