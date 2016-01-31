import redis
import random
import pilasengine

from config import PILAS_SCREEN_X, PILAS_SCREEN_Y


class MiMono(pilasengine.actores.Mono):
    def iniciar(self):
        # self.aprender('arrastrable')
        self.startx = 0
        self.starty = 0

        self.choques = 0

        # Comunicacion por Redis
        self.r = redis.Redis()

    def actualizar(self):
        self.actualizar_x()
        self.actualizar_y()

    def actualizar_x(self):
        # lpop is non-blocking
        startx = self.r.lpop('startx')
        distx = self.r.lpop('distx')

        if startx is not None:
            # print('startx:', startx)
            self.startx = self.x  # int(startx)

        if distx is not None:
            # print('distx:', distx)
            self.x = self.startx + int(distx)

    def actualizar_y(self):
        # lpop is non-blocking
        starty = self.r.lpop('starty')
        disty = self.r.lpop('disty')

        if starty is not None:
            # print('starty:', starty)
            self.starty = self.y  # int(starty)

        if disty is not None:
            # print('disty:', disty)
            self.y = self.starty - int(disty)


class MiBomba(pilasengine.actores.Bomba):

    def iniciar(self):
        #self.escena = pilas.escenas.Normal()

        # defino la posicion inicial
        x_signo = random.choice([1, -1])
        y_signo = random.choice([1, -1])

        self.x = x_signo * PILAS_SCREEN_X / 2 + x_signo * self.ancho / 2
        self.x += random.randint(-PILAS_SCREEN_X / 2, PILAS_SCREEN_X / 2)

        self.y = y_signo * PILAS_SCREEN_Y / 2 + y_signo * self.alto / 2
        self.y += random.randint(-PILAS_SCREEN_Y / 2, PILAS_SCREEN_Y / 2)

        # defino la aceleracion
        if self.x > 0:
            self.aceleracion_x = random.randint(-5, 0)
        if self.x < 0:
            self.aceleracion_x = random.randint(0, 5)

        if self.y > 0:
            self.aceleracion_y = random.randint(-5, 0)
        if self.y < 0:
            self.aceleracion_y = random.randint(0, 5)

        if self.aceleracion_y == 0 and self.aceleracion_x == 0:
            self.aceleracion_y = random.randint(0, 5)

        # print(self.aceleracion_x, self.aceleracion_y)
        # print(self.x, self.y)

        # self.x = self.y = 0
        # pilas.utils.interpolar(self, 'x', x_signo * PILAS_SCREEN_X / 2 + x_signo * self.ancho / 2, 5)
        # pilas.utils.interpolar(self, 'y', y_signo * PILAS_SCREEN_Y / 2 + y_signo * self.ancho / 2, 5)

    def actualizar(self):
        self.x += self.aceleracion_x
        self.y += self.aceleracion_y
