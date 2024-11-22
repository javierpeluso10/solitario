import pygame
import random

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
ANCHO, ALTO = 1000, 700
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Solitario Klondike")

# Colores
BLANCO = (255, 255, 255)
VERDE = (34, 139, 34)

# Cargar fuentes
FUENTE = pygame.font.SysFont('Arial', 24)

# Constantes globales
PALOS = ["Hearts", "Shades", "Diamonds", "Clubs"]
VALORES = list(range(1, 14))
carta_seleccionada = None
offset_x = offset_y = 0

# Clase Carta
class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.visible = False
        self.rect = pygame.Rect(0, 0, 70, 100)  # Tamaño de la carta
        self.imagen = pygame.image.load(f"images/{valor}{palo[0]}.png")
        self.imagen = pygame.transform.scale(self.imagen, (70, 100))
        self.dorso = pygame.image.load("images/back.png")
        self.dorso = pygame.transform.scale(self.dorso, (70, 100))
        self.imagen = pygame.image.load(f"images/{valor}{palo[0]}.png")
        print(f"Intentando cargar: images/{valor}{palo[0]}.png")
        
    def dibujar(self, pantalla, x, y):
        self.rect.topleft = (x, y)
        if self.visible:
            pantalla.blit(self.imagen, (x, y))
        else:
            pantalla.blit(self.dorso, (x, y))


# Funciones del juego
def crear_mazo():
    mazo = [Carta(valor, palo) for palo in PALOS for valor in VALORES]
    random.shuffle(mazo)
    return mazo


def configurar_tablero(mazo):
    columnas = [[] for _ in range(7)]
    for i in range(7):
        columnas[i].extend(mazo[:i + 1])
        mazo = mazo[i + 1:]
        columnas[i][-1].visible = True
    return columnas, mazo


def dibujar_tablero(columnas, bases):
    PANTALLA.fill(VERDE)
    x_inicial = 50
    y_base = 50

    # Dibujar bases
    for i, base in enumerate(bases):
        x = x_inicial + i * 100
        if base:
            base[-1].dibujar(PANTALLA, x, y_base)
        else:
            pygame.draw.rect(PANTALLA, BLANCO, (x, y_base, 70, 100), 2)

    # Dibujar columnas
    for i, columna in enumerate(columnas):
        x = x_inicial + i * 100
        y = 200
        for carta in columna:
            carta.dibujar(PANTALLA, x, y)
            y += 30  # Superposición entre cartas


def manejar_eventos(evento, columnas, bases):
    global carta_seleccionada, offset_x, offset_y

    if evento.type == pygame.MOUSEBUTTONDOWN:
        x, y = evento.pos
        for columna in columnas:
            for carta in columna:
                if carta.rect.collidepoint(x, y) and carta.visible:
                    carta_seleccionada = carta
                    offset_x, offset_y = x - carta.rect.x, y - carta.rect.y
                    return

    elif evento.type == pygame.MOUSEBUTTONUP:
        if carta_seleccionada:
            x, y = evento.pos

            # Intentar mover a las bases
            for base in bases:
                if base and base[-1].rect.collidepoint(x, y):
                    if validar_movimiento_base(carta_seleccionada, base):
                        base.append(carta_seleccionada)
                        quitar_carta_de_origen(columnas, carta_seleccionada)
                        carta_seleccionada = None
                        return

            # Intentar mover a las columnas
            for columna in columnas:
                if columna and columna[-1].rect.collidepoint(x, y):
                    if validar_movimiento(carta_seleccionada, columna[-1]):
                        columna.append(carta_seleccionada)
                        quitar_carta_de_origen(columnas, carta_seleccionada)
                        carta_seleccionada = None
                        return

            carta_seleccionada = None

    elif evento.type == pygame.MOUSEMOTION:
        if carta_seleccionada:
            carta_seleccionada.rect.x = evento.pos[0] - offset_x
            carta_seleccionada.rect.y = evento.pos[1] - offset_y


def validar_movimiento(carta, destino):
    # Las cartas deben alternar colores y ser descendentes
    colores = {"Corazones": "rojo", "Diamantes": "rojo", "Picas": "negro", "Tréboles": "negro"}
    if colores[carta.palo] != colores[destino.palo] and carta.valor == destino.valor - 1:
        return True
    return False


def validar_movimiento_base(carta, base):
    if not base and carta.valor == 1:  # Solo As en bases vacías
        return True
    elif base and carta.palo == base[-1].palo and carta.valor == base[-1].valor + 1:
        return True
    return False


def quitar_carta_de_origen(columnas, carta):
    for columna in columnas:
        if carta in columna:
            columna.remove(carta)
            if columna:  # Hacer visible la última carta
                columna[-1].visible = True
            return


def verificar_victoria(bases):
    return all(len(base) == 13 for base in bases)


# Bucle principal
def main():
    mazo = crear_mazo()
    columnas, mazo = configurar_tablero(mazo)
    bases = [[] for _ in range(4)]  # Montones de base

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            manejar_eventos(evento, columnas, bases)

        dibujar_tablero(columnas, bases)

        if verificar_victoria(bases):
            print("¡Felicidades, has ganado!")
            corriendo = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
