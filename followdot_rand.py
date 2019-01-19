import pygame as pg
import sys
import random
import time
from win32api import GetSystemMetrics
import math
import numpy as np

timee = time.time()
pg.init()
offset = 10
# screen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
# mid_x = int(screen_resolution[0]/2)
# mid_y = int(screen_resolution[1]/2)
# max_x = screen_resolution[0] - offset
# max_y = screen_resolution[1] - offset

res = [GetSystemMetrics(0), GetSystemMetrics(1)]
screen = pg.display.set_mode(res, pg.FULLSCREEN)
screen_color = (0,0,0)
dot_color = (255,0,0)
line_color = (244,220,66)
radius = 15
thickness = 15
length_direction = 30
arrow_line_thickness = 2

try:
    f = open(r'D:\g_truth.txt','w')
except Exception as e:
    print("file exception ",e)
# points = [(offset,offset), (max_x,max_y), (max_x, offset), (offset, max_y), (mid_x, mid_y), (offset, mid_y), (mid_x, offset), (mid_x, max_y), (max_x, mid_y)]
# print(points)


def arrowline_end_point(a,b, c,d):
    alpha = length_direction/math.sqrt(math.pow((c-a),2)+math.pow((d-b),2) )
    temp_x = c +alpha*(a - c)
    temp_y = d +alpha*(b - d)
    return int(temp_x),int(temp_y)
    
    
def draw_arrow(screen, colour, start, end):
    radius_1 = 8
    rot_val = 120
    pg.draw.line(screen,colour,start,end,arrow_line_thickness)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pg.draw.polygon(screen, colour, ((end[0]+radius_1*math.sin(math.radians(rotation)), end[1]+radius_1*math.cos(math.radians(rotation))), (end[0]+radius_1*math.sin(math.radians(rotation-rot_val)), end[1]+radius_1*math.cos(math.radians(rotation-rot_val))), (end[0]+radius_1*math.sin(math.radians(rotation+rot_val)), end[1]+radius_1*math.cos(math.radians(rotation+rot_val)))))
   

   
def rand_point_gen():
    temp_rand1 = [random.uniform(0,1), random.uniform(0,1)]
    p1 = np.multiply(res,temp_rand1)
    p1 = p1.astype(int)
    # temp = (np.add(p1,[radius, radius]))
    # while ((temp[0] == end_point[0]) or (temp[1] == end_point[1])):
        # print("equal")
        # p1 = np.multiply(res,temp_rand1)
        # p1 = p1.astype(int)
        # temp = (np.add(p1,[radius, radius]))
    print(p1)
    return p1

   
def threshold():
    # max = np.subtract(res, off_val)
    mid = np.divide(res , 2)
    mid = mid.astype(int)
    thresh_dist = np.linalg.norm(mid - off_val)
    return thresh_dist


    
off_val = [offset, offset]   
end_point = np.subtract(res , off_val)
thresh = threshold()

p1 = rand_point_gen()
pg.mouse.set_visible(False)
while (1):
    try:
        if time.time() - timee > 60:
            f.close()
            pg.quit()
            sys.exit()

        screen.fill(screen_color)
        p = rand_point_gen()
        dist = np.linalg.norm(p1 - p)
        
        while (dist <= thresh):
            print("less than threshold")
            p = rand_point_gen()
            dist = np.linalg.norm(p1 - p)

        try:
            pg.draw.circle(screen, dot_color, (p1[0], p1[1]), radius, thickness)
            (new_x, new_y) = arrowline_end_point(p[0],p[1],p1[0],p1[1])
            draw_arrow(screen, line_color, (p1[0],p1[1]),(new_x, new_y))
            pg.display.update()
            pg.time.delay(500)
            screen.fill(screen_color)
            p1 = p
        except Exception as e:
            print("Exception here",e)
        f.writelines(str(p[0])+ " " + str(p[1])+ "\n")
        pg.draw.circle(screen, dot_color, (p[0], p[1]), radius, thickness)
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
