import pygame
import sys
import random

pygame.init()
offset = 50
screen_resolution = (1920, 1080)
mid_x = int(screen_resolution[0]/2)
mid_y = int(screen_resolution[1]/2)
max_x = screen_resolution[0] - offset
max_y = screen_resolution[1] - offset
 

screen = pygame.display.set_mode(screen_resolution, pygame.FULLSCREEN)
#pygame.display.toggle_fullscreen()
screen_color = (255,255,255)
dot_color = (255,0,0)
radius = 15
thickness = 15

points = [(offset,offset), (max_x,max_y), (max_x, offset), (offset, max_y), (mid_x, mid_y), (offset, mid_y), (mid_x, offset), (mid_x, max_y), (max_x, mid_y)]
print(points)
#for mode in pygame.display.list_modes():
#	print(mode)
i = 0
while (1):
	
	try:    
		screen.fill(screen_color)
		x,y = random.choice(points)
		#x, y = points[i]		
		#print (x,y)		
		pygame.draw.circle(screen, dot_color, (x, y), radius, thickness)
		pygame.display.update()
		pygame.time.delay(3000)
		#i += 1
		#if i == len(points):
		#	i = 0
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				print ("Key press")				
				pygame.quit()
	except Exception as e:
		pygame.quit()		
		
