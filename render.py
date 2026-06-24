import pygame
from dataclasses import replace

from models import GameState, Nave


def obtener_color_asteroide(radio: int) -> tuple:
	"""Retorna color RGB basado en el tamaño del asteroide."""
	# Escalar radio (4-10) a valores RGB
	# Pequeños: más claros, Grandes: más oscuros
	normalized = (radio - 4) / 6  # Normalizar a 0-1
	
	# Crear gradiente: claro → medio → oscuro
	if normalized < 0.5:
		# Gradiente de gris claro a medio
		gray = int(220 - (normalized * 2) * 50)
		return (gray, gray, gray)
	else:
		# Gradiente de gris medio a tonos cálidos
		gray = int(170 - ((normalized - 0.5) * 2) * 50)
		return (gray + 50, gray, gray)


def mover_nave(nave: Nave, estado: GameState) -> Nave:
	"""Actualiza la posición de la nave según las teclas presionadas."""
	teclas = pygame.key.get_pressed()
	
	nueva_x = nave.x
	nueva_y = nave.y
	velocidad = nave.velocidad
	
	# Controles con WASD y Flechas
	# Arriba
	if teclas[pygame.K_w] or teclas[pygame.K_UP]:
		nueva_y -= velocidad
	# Abajo
	if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
		nueva_y += velocidad
	# Izquierda
	if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
		nueva_x -= velocidad
	# Derecha
	if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
		nueva_x += velocidad
	
	# Limitar movimiento dentro de los límites de la pantalla
	nueva_x = max(nave.radio, min(nueva_x, estado.ancho - nave.radio))
	nueva_y = max(nave.radio, min(nueva_y, estado.alto - nave.radio))
	
	return replace(nave, x=nueva_x, y=nueva_y)


def dibujar_estado(superficie, estado: GameState):
	superficie.fill((10, 10, 20))

	for asteroide in estado.asteroides:
		color = obtener_color_asteroide(asteroide.radio)
		pygame.draw.circle(
			superficie,
			color,
			(int(asteroide.x), int(asteroide.y)),
			asteroide.radio,
		)

	# Dibujar nave como triángulo
	nave_x = int(estado.nave.x)
	nave_y = int(estado.nave.y)
	radio = estado.nave.radio
	
	# Vértices del triángulo (punta arriba)
	vertices = [
		(nave_x, nave_y - radio),           # Punta arriba
		(nave_x - radio, nave_y + radio),   # Esquina inferior izquierda
		(nave_x + radio, nave_y + radio)    # Esquina inferior derecha
	]
	
	pygame.draw.polygon(superficie, (80, 180, 255), vertices)

	if estado.game_over:
		fuente = pygame.font.SysFont(None, 48)
		texto = fuente.render("GAME OVER", True, (255, 80, 80))
		rect = texto.get_rect(center=(estado.ancho // 2, estado.alto // 2))
		superficie.blit(texto, rect)


def ejecutar_juego(estado_inicial: GameState, actualizar_estado):
	pygame.init()
	pygame.font.init()

	pantalla = pygame.display.set_mode((estado_inicial.ancho, estado_inicial.alto))
	pygame.display.set_caption("Simulador de Asteroides Paralelo")
	reloj = pygame.time.Clock()

	estado = estado_inicial
	ejecutando = True

	while ejecutando:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				ejecutando = False

		if not estado.game_over:
			# Actualizar posición de la nave según entrada
			nueva_nave = mover_nave(estado.nave, estado)
			estado_con_nave_actualizada = replace(estado, nave=nueva_nave)
			
			# Actualizar asteroides y colisiones
			estado = actualizar_estado(estado_con_nave_actualizada)

		dibujar_estado(pantalla, estado)
		pygame.display.flip()
		reloj.tick(60)

	pygame.quit()
