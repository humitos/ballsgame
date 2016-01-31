import pilasengine

from config import PILAS_SCREEN_X, PILAS_SCREEN_Y

from actores import MiMono, MiBomba
from colisiones import jugador_choca_bomba
from utilidades import crear_bombas


if __name__ == '__main__':
    # Inicio el motor pilas-engine
    pilas = pilasengine.iniciar(
        ancho=PILAS_SCREEN_X,
        alto=PILAS_SCREEN_Y,
        pantalla_completa=True
    )

    # pilas.definir_pantalla_completa(True)  # Esc / Alt + f

    pilas.actores.vincular(MiBomba)
    pilas.actores.vincular(MiMono)

    mono = pilas.actores.MiMono()
    bombas = pilas.actores.Grupo()

    pilas.colisiones.agregar(mono, bombas, jugador_choca_bomba)
    pilas.tareas.siempre(1, crear_bombas, bombas, pilas.actores.MiBomba)

    pilas.ejecutar()
