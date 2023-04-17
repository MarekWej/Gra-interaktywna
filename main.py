import pygame

pygame.init() # inicjacja

window = pygame.display.set_mode((800,600))

run = True
while run:
        for event in pygame.event.get(): # zwracanie listy zdarzeń wywołanych przez gracza
            if event.type == pygame.QUIT: # jeśli gracz zamknie okienko
                run = False

        window.fill((104, 191, 237))      #kolor tła
        pygame.display.update()            #