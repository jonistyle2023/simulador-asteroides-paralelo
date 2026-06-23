import time
from multiprocessing import cpu_count, freeze_support

from main import crear_estado
from physics import update_secuencial
from parallel_engine import update_paralelo


def medir_fps(nombre, funcion_update, cantidad_entidades, frames=120):
    state = crear_estado(cantidad_entidades)

    inicio = time.perf_counter()

    for _ in range(frames):
        state = funcion_update(state)

    fin = time.perf_counter()

    tiempo_total = fin - inicio
    fps = frames / tiempo_total

    print(nombre, "-", cantidad_entidades, "entidades:", round(fps, 2), "FPS")


def ejecutar_benchmark():
    print("Nucleos detectados:", cpu_count())
    print("Workers configurados:", cpu_count())
    print("--------------------------------")

    for cantidad in (1000, 3000, 5000):
        medir_fps("Secuencial", update_secuencial, cantidad)
        medir_fps("Paralelo", update_paralelo, cantidad)
        print("--------------------------------")


if __name__ == "__main__":
    freeze_support()
    ejecutar_benchmark()