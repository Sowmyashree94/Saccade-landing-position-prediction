import pygame as pg
import sys
import random
import time
from win32api import GetSystemMetrics
# from copy import deepcopy

timee = time.time()
pg.init()
offset = 50
screen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
mid_x = int(screen_resolution[0]/2)
mid_y = int(screen_resolution[1]/2)
max_x = screen_resolution[0] - offset
max_y = screen_resolution[1] - offset


screen = pg.display.set_mode(screen_resolution, pg.FULLSCREEN)
#pg.display.toggle_fullscreen()
screen_color = (255,255,255)
dot_color = (255,0,0)
old_dot_color = (200,200,0)
line_color = (0,10,10)
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
            pg.quit()
            sys.exit()

        screen.fill(screen_color)
        x,y = random.choice(points)
        while((x1,y1) == (x,y)):
            print("same")
            x,y = random.choice(points)
        try:
            pg.draw.circle(screen, old_dot_color, (x1, y1), radius, thickness)
            pg.draw.lines(screen, line_color, False, [(x1,y1), (((x+x1)/2),((y+y1)/2))], 3)
            pg.display.update()
            pg.time.delay(500)
            screen.fill(screen_color)
            
            x1,y1 = (x,y)
        except Exception as e:
            print("Exception here",e)
        f.writelines(str(x)+ " " + str(y)+ "\n")
        print("dots", str(x),str(y))
        pg.draw.circle(screen, dot_color, (x, y), radius, thickness)
        pg.display.update()
        pg.time.delay(3000)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                print ("Key press")
                try:
                    f.close()
                except Exception as e:
                    print("File close exception ",e)
                pg.quit()
                sys.exit()
    except Exception as e:
        f.close()
        print("Exception ",e)
        pg.quit()
        sys.exit()
