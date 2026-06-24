import pygame

from models import GameState


def dibujar_estado(superficie, estado: GameState):
	superficie.fill((10, 10, 20))

	for asteroide in estado.asteroides:
		pygame.draw.circle(
			superficie,
			(200, 200, 200),
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
			estado = actualizar_estado(estado)

		dibujar_estado(pantalla, estado)
		pygame.display.flip()
		reloj.tick(60)

	pygame.quit()
