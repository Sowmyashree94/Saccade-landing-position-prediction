import pygame as pg
import sys
import random
import time
from win32api import GetSystemMetrics
import math
import numpy as np

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
screen_color = (0,0,0)
dot_color = (255,0,0)
line_color = (244,220,66)
radius = 30
thickness = 30
length_direction = 80

try:
    f = open(r'D:\g_truth.txt','w')
except Exception as e:
    print("file exception ",e)
points = [(offset,offset), (max_x,max_y), (max_x, offset), (offset, max_y), (mid_x, mid_y), (offset, mid_y), (mid_x, offset), (mid_x, max_y), (max_x, mid_y)]
print(points)


def arrowline_end_point(a,b, c,d):
    alpha = length_direction/math.sqrt(math.pow((c-a),2)+math.pow((d-b),2) )
    x = c +alpha*(a - c)
    y = d +alpha*(b - d)
    return int(x),int(y)
    
def draw_arrow(screen, colour, start, end):
    radius_1 = 8
    rot_val = 120
    pg.draw.line(screen,colour,start,end,4)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pg.draw.polygon(screen, colour, ((end[0]+radius_1*math.sin(math.radians(rotation)), end[1]+radius_1*math.cos(math.radians(rotation))), (end[0]+radius_1*math.sin(math.radians(rotation-rot_val)), end[1]+radius_1*math.cos(math.radians(rotation-rot_val))), (end[0]+radius_1*math.sin(math.radians(rotation+rot_val)), end[1]+radius_1*math.cos(math.radians(rotation+rot_val)))))
   

x1, y1 = random.choice(points)
pg.mouse.set_visible(False)
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
            pg.draw.circle(screen, dot_color, (x1, y1), radius, thickness)
            (new_x, new_y) = arrowline_end_point(x,y,x1,y1)
            draw_arrow(screen, line_color, (x1,y1),(new_x, new_y))
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
