import pygame
from random import randint
from math import floor
from game import *

pygame.init()  # inicjacja
resolution = (1280, 720)
window = pygame.display.set_mode(resolution)


def level_one():
    global keys
    run = True
    player = Player()
    background = Background()
    clock = 0
    beams =[
        Beam(0,720,2217,60),
        Beam(200,640,20,100),
        Beam(500,640,30,120)
    ]
    while run:
        clock += pygame.time.Clock().tick(60)/1000        #maks 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # jeśli gracz zamknie okno
                run = False
        keys = pygame.key.get_pressed()  # Tworzymy ruch poprzez strzałki na klawiaturze

        player.tick(keys, beams)
        background.tick(player)
        background.draw(window)

        player.draw(window, background.width)
        for beam in beams:
            beam.draw(window, background.x_cord)

        pygame.display.update()  # odświeżamy obraz

def main():
    run = True
    clock = 0
    background = pygame.image.load('menu.png')
    play_button = button(400, 500, "button.png")

    while run:
        clock += pygame.time.Clock().tick(60)/1000        #maks 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # jeśli gracz zamknie okno
                run = False
        if play_button.tick():
            level_one()

        play_button.tick()

        window.blit(background,(0,0))
        play_button.draw(window)
        pygame.display.update()




if __name__ == "__main__":
    main()