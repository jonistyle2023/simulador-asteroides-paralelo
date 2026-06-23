from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Asteroide:
    x: float
    y: float
    vx: float
    vy: float
    radio: int


@dataclass(frozen=True)
class Nave:
    x: float
    y: float
    velocidad: float
    radio: int


@dataclass(frozen=True)
class GameState:
    nave: Nave
    asteroides: Tuple[Asteroide, ...]
    ancho: int
    alto: int
    game_over: bool
    frame: int