from dataclasses import replace
from models import Asteroide, GameState

def mover_asteroide(asteroide: Asteroide, ancho: int, alto: int)-> Asteroide:
    nuevo_x = asteroide.x + asteroide.vx
    nuevo_y = asteroide.y + asteroide.vy
    
    if nuevo_x < 0:
        nuevo_x = ancho
    elif nuevo_x > ancho:
        nuevo_x = 0

    if nuevo_y < 0:
        nuevo_y = alto
    elif nuevo_y > alto:
        nuevo_y = 0
        
    return replace(
        asteroide,         
        x=nuevo_x,
        y=nuevo_y
    )

def update_secuencial(state: GameState) -> GameState:
    nuevos_asteroides = tuple(
        mover_asteroide(ast, state.ancho, state.alto)
        for ast in state.asteroides
    )

    return replace(
        state,
        asteroides=nuevos_asteroides,
        frame=state.frame +1
    )