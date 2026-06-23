from dataclasses import replace
from multiprocessing import Pool, cpu_count
from typing import Tuple

from models import Asteroide, GameState
from physics import mover_asteroide, hay_colision


def dividir_entidades(asteroides: Tuple[Asteroide, ...], partes: int):
    tamano = max(1, len(asteroides) // partes)

    return tuple(
        asteroides[i:i + tamano]
        for i in range(0, len(asteroides), tamano)
    )


def procesar_segmento(argumentos):
    segmento, ancho, alto = argumentos

    return tuple(
        mover_asteroide(ast, ancho, alto)
        for ast in segmento
    )


def update_paralelo(state: GameState, workers: int = None) -> GameState:
    cantidad_workers = workers or cpu_count()

    segmentos = dividir_entidades(state.asteroides, cantidad_workers)

    argumentos = tuple(
        (segmento, state.ancho, state.alto)
        for segmento in segmentos
    )

    with Pool(processes=cantidad_workers) as pool:
        resultados = pool.map(procesar_segmento, argumentos)

    nuevos_asteroides = tuple(
        ast
        for segmento in resultados
        for ast in segmento
    )

    nuevo_estado = replace(
        state,
        asteroides=nuevos_asteroides,
        frame=state.frame + 1
    )

    return replace(
        nuevo_estado,
        game_over=hay_colision(nuevo_estado)
    )