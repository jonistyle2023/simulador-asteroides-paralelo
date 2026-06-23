import random
from multiprocessing import freeze_support

from models import Asteroide, Nave, GameState


def crear_asteroides(cantidad: int, ancho: int, alto: int):
    return tuple(
        Asteroide(
            x=random.randint(0, ancho),
            y=random.randint(0, alto),
            vx=random.uniform(-2, 2),
            vy=random.uniform(-2, 2),
            radio=random.randint(4, 10)
        )
        for _ in range(cantidad)
    )


def crear_estado(cantidad_asteroides: int) -> GameState:
    ancho = 900
    alto = 600

    return GameState(
        nave=Nave(
            x=ancho / 2,
            y=alto / 2,
            velocidad=5,
            radio=15
        ),
        asteroides=crear_asteroides(cantidad_asteroides, ancho, alto),
        ancho=ancho,
        alto=alto,
        game_over=False,
        frame=0
    )


if __name__ == "__main__":
    freeze_support()
    estado = crear_estado(1000)
    print("Estado inicial creado:", estado.frame)