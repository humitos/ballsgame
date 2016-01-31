def jugador_choca_bomba(jugador, bomba):
    jugador.gritar()
    jugador.choques += 1

    # texto = pilas.actores.TextoInferior(
    #     texto='Puntaje: {}'.format(jugador.choques))

    bomba.explotar()
