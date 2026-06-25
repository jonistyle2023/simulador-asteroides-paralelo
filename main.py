import random
from multiprocessing import freeze_support

from models import Asteroide, Nave, GameState
from parallel_engine import update_paralelo
from render import ejecutar_juego


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


def crear_estado(cantidad_asteroides: int, workers: int, modo: str) -> GameState:
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
        frame=0,
        workers=workers,
        modo=modo
    )


if __name__ == "__main__":
    freeze_support()
    estado = crear_estado(5000, 8, "Paralelo")
    ejecutar_juego(estado, update_paralelo)
