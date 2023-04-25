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
    pause = False
    pause_image = pygame.font.Font.render(pygame.font.SysFont("", 90), "Pauza", True, (0,0,0))
    player = Player()
    enemys = [Enemy(300,400), Enemy(150,400), Enemy(200,400), Enemy(100,400)]
    background = Background()
    clock = 0
    beams =[
        Beam(0,720,2217,60),
        Beam(200,640,20,100),
        Beam(500,640,30,120)
    ]
    while run:
        delta = pygame.time.Clock().tick(60) / 1000        #maks 60 fps
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # jeśli gracz zamknie okno
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause
        keys = pygame.key.get_pressed()  # Tworzymy ruch poprzez strzałki na klawiaturze

        if pause:
            window.blit(pause_image, (500, 300))
            pygame.display.update()
            continue

        player.tick(keys, beams, delta)
        for enemy in enemys:
            enemy.tick(beams, player)
        background.tick(player)
        background.draw(window)
        player.draw(window, background.width)
        for enemy in enemys:
            enemy.draw(window, background.x_cord)
        for beam in beams:
            beam.draw(window, background.x_cord)

        pygame.display.update()  # odświeżamy obraz

def main():
    run = True
    clock = 0
    background = pygame.image.load('menu.png')
    play_button = button(400, 500, "button.png")
    textinput = TextInput(490,400,300,50, placeholder= "wpisz login")
    #textinput2 = TextInput(300, 100, 150, 40)
    while run:
        clock += pygame.time.Clock().tick(60)/1000        #maks 60 fps
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:                 #jeśli gracz zamknie okno
                run = False
        content = textinput.tick(clock, events)
        #textinput2.tick(events)
        if content is not None:
            print(f"wprowadzona wiadomość: {content}")
        if play_button.tick():
            level_one()

        play_button.tick()

        window.blit(background,(0,0))
        play_button.draw(window)
        textinput.draw(window)
        #textinput2.draw(window)
        pygame.display.update()




if __name__ == "__main__":
    main()