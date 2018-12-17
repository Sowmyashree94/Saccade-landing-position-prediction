import pygame
import sys
import random
from subprocess import Popen, PIPE, STDOUT
import time
from copy import deepcopy

timee = time.time()
pygame.init()
offset = 50
record_time = 62


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
f = open(r"C:\Users\Niteesh\Desktop\g_truth.txt",'w')
points = [(offset,offset), (max_x,max_y), (max_x, offset), (offset, max_y), (mid_x, mid_y), (offset, mid_y), (mid_x, offset), (mid_x, max_y), (max_x, mid_y)]
print(points)
p = random.choice(points)
pygame.mouse.set_visible(False)
while (1):
	
	try:
		if time.time() - timee > record_time:
				pygame.quit()
				f.close()
				sys.exit()
		screen.fill(screen_color)
		p1 = random.choice(points)
		while(p == p1):
 				p1 = random.choice(points)
 				print("I am here ",p1,p)
 				
		p = p1		
		f.writelines(str(p[0])+ "|" + str(p[1])+ "\n")
		pygame.draw.circle(screen, dot_color, p, radius, thickness)
		pygame.display.update()
		pygame.time.delay(3000)

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				print ("Key press")				
				pygame.quit()
				f.close()
				sys.exit()
	except Exception as e:
		print(e)
		pygame.quit()
