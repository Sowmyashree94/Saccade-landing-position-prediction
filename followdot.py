import pygame
import sys
import random
import time
from win32api import GetSystemMetrics
# from copy import deepcopy

timee = time.time()
pygame.init()
offset = 50
screen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
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
try:
    f = open(r'D:\g_truth.txt','w')
except Exception as e:
    print("file exception ",e)
points = [(offset,offset), (max_x,max_y), (max_x, offset), (offset, max_y), (mid_x, mid_y), (offset, mid_y), (mid_x, offset), (mid_x, max_y), (max_x, mid_y)]
print(points)


# i = 0
x1, y1 = random.choice(points)
while (1):

    try:
        if time.time() - timee > 60:
            f.close()
            pygame.quit()
            sys.exit()

        screen.fill(screen_color)
        x,y = random.choice(points)
        while((x1,y1) == (x,y)):
            print("same")
            x,y = random.choice(points)
        try:
            x1,y1 = (x,y)
        except Exception as e:
            print("Exception here",e)
        f.writelines(str(x)+ " " + str(y)+ "\n")
        print("dots", str(x),str(y))
        pygame.draw.circle(screen, dot_color, (x, y), radius, thickness)
        pygame.display.update()
        pygame.time.delay(3000)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print ("Key press")
                try:
                    f.close()
                except Exception as e:
                    print("File close exception ",e)
                pygame.quit()
                sys.exit()
    except Exception as e:
        f.close()
        print("Exception ",e)
        pygame.quit()
        sys.exit()
