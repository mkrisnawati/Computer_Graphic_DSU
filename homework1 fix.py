#insert library pygame and numpy
import pygame
from pygame.locals import *
from sys import exit
import numpy as np

#setting image
background_image_filename = 'image/curve_pattern.png'
sprite_image_filename = 'image/icon_speech.png'

#looping setting display and make the dots
if __name__ == '__main__':
    pygame.init()
    #display size is width 1000, height 800 
    screen = pygame.display.set_mode((1000, 800))
    screen.fill((255, 255, 255))
    #and title project is (name - student ID - HW 1)
    pygame.display.set_caption("Krisnawati Melisa - 20245056 - Homework 1")
    clock = pygame.time.Clock()

    #define fonts
    font = pygame.font.SysFont("arialblack", 40)

    #define colours dark brown for title project
    TEXT_COL = (153,101,21)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    draw_text("Krisnawati Melisa_20245056_Homework 1", font, TEXT_COL, 30, 100)
    
    loop = True
    press = False

    x1,y1, x2, y2 = 0, 0, 0, 0
    clickCount = 0
    while loop:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

        #looping setting for every mouse click for the drawing
            px, py = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, (0, 0, 255), (px-5, py-5, 10, 10))
                if clickCount < 1:
                    x1 = px
                    y1 = py
                elif clickCount > 1:
                    x2 = px
                    y2 = py
                    pygame.draw.line(screen, (0, 255, 0), (x1, y1), (x2, y2))
                    x1 = px
                    y1 = py
                clickCount += 1

            if event.type == pygame.MOUSEBUTTONUP:
                press == False
            pygame.display.update()
            clock.tick(1000)
        except Exception as e:
            print(e)
            pygame.quit()

    pygame.quit()