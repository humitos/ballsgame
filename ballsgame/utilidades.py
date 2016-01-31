from config import PILAS_SCREEN_X, PILAS_SCREEN_Y


def esta_fuera_de_la_pantalla(actor):
    if actor.fijo:
        return False

    izquierda = -PILAS_SCREEN_X / 2
    derecha = PILAS_SCREEN_X / 2
    arriba = PILAS_SCREEN_Y / 2
    abajo = -PILAS_SCREEN_Y / 2
    return actor.derecha < izquierda or \
        actor.izquierda > derecha or \
        actor.abajo > arriba or \
        actor.arriba < abajo


def crear_bombas(bombas, actor):
    for i in range(2):
        bombas.agregar(actor())

    for bomba in bombas:
        if esta_fuera_de_la_pantalla(bomba):
            bomba.iniciar()
