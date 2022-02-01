import pygame

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chess')

run = True 
while run:
	pygame.time.Clock().tick(30)

	pygame.display.update()
	
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			run = False 
			break 

		if ev.type == pygame.MOUSEBUTTONUP:
			print('Clicked!')