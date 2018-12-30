import pygame as pg
import numpy as np
import time
import sys
from win32api import GetSystemMetrics
import asyncio

class display_dot_EyeX:
    def __init__(self, fps):
        print("initialized")
        self.res=[GetSystemMetrics(0), GetSystemMetrics(1)]
        self.fps = fps
        
        #pygame settings
        self.screen = pg.display.set_mode(self.res, pg.FULLSCREEN)
        self.screen_color = (220,220,220)
        self.dot_color = (255,0,0)
        self.radius = 10
        self.thickness = 10
       
        
    def display_dots(self, coord):
        self.screen.fill(self.screen_color)
#        print("coordinates : ",int(coord[0]), int(coord[1]))
        pg.draw.circle(self.screen, self.dot_color, (int(coord[0]), int(coord[1])), self.radius, self.thickness)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                print("Key press event")
                pg.quit()
                print("pg quit")
                # print(asyncio.get_event_loop())
                # loop = asyncio.get_event_loop()
 #               loop.stop()
                # loop.close()
#                 return False
                sys.exit()
        
        
    def display_coord(self, coord):
 #       for i in range(self.coordinates.shape[0]):
 #           for j in range(self.coordinates.shape[1]):
 #               print(self.disp_coord[i][j])
        coord = [float(coord.split()[0]),float(coord.split()[1])]
        self.display_dots(coord)
#        print ("check in display dot ",check)
#        if check == False:
#            print("time to quit")
#            return check
        time.sleep(1/self.fps)
#        return check
            
    def quit_pg(self):
        pg.quit()
#pos = pygame.mouse.get_pos()
#    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
    
#def main():
#    dd = display_dot([1366,768], 60)
#    dd.display_coord()  
        
#if __name__ == "__main__":
#        main()