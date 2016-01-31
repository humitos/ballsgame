import json
import redis
import random
import pilasengine

from config import PILAS_SCREEN_X, PILAS_SCREEN_Y


class MiMono(pilasengine.actores.Mono):
    def iniciar(self):
        # TODO: remove this, it's just for debugging purposes
        self.aprender('arrastrable')

        self.startx = 0
        self.starty = 0

        self.choques = 0

        # Comunicacion por Redis
        self.queue = redis.Redis()

        # FIXME: this nickname should come from the 'iniciar' method
        self.nickname = 'humitos'

    def actualizar(self):
        self.actualizar_x()
        self.actualizar_y()

    def actualizar_x(self):
        # lpop is non-blocking
        data = self.queue.lpop(self.nickname)
        if data is None:
            return

        # README: the data comes into JSON string
        data = json.loads(data)['data']

        if data['type'] == 'startx':
            startx = data['value']
            if startx is not None:
                # print('startx:', startx)
                self.startx = self.x  # int(startx)

        if data['type'] == 'distx':
            distx = data['value']
            if distx is not None:
                # print('distx:', distx)
                self.x = self.startx + int(distx)

    def actualizar_y(self):
        # lpop is non-blocking
        data = self.queue.lpop(self.nickname)
        if data is None:
            return

        # README: the data comes into JSON string
        data = json.loads(data)['data']

        if data['type'] == 'starty':
            starty = data['value']
            if starty is not None:
                # print('starty:', starty)
                self.starty = self.y  # int(starty)

        if data['type'] == 'disty':
            disty = data['value']
            if disty is not None:
                # print('disty:', disty)
                self.y = self.starty - int(disty)


class MiBomba(pilasengine.actores.Bomba):

    def iniciar(self):
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

    def actualizar(self):
        self.x += self.aceleracion_x
        self.y += self.aceleracion_y
