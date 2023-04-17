import pygame

pygame.init()                                  #inicjacja

window = pygame.display.set_mode((1024,768))

x = 0
y = 0
player = pygame.rect.Rect(x, y, 70, 70)        #Tworzenie postaci


run = True
while run:
    pygame.time.Clock().tick(60)     #zwalniamy prędkość postaci(FPS)
    for event in pygame.event.get(): # zwracanie listy zdarzeń wywołanych przez gracza
        if event.type == pygame.QUIT: # jeśli gracz zamknie okienko
            run = False

    keys = pygame.key.get_pressed()    #Tworzymy ruch poprzez strzałki na klawiaturze

    speed = 5

    if keys[pygame.K_RIGHT]:            #strzałka w prawo
        x += speed
    if keys[pygame.K_LEFT]:             #strzałka w lewo
        x -= speed
    if keys[pygame.K_UP]:               #strzałka do góry
        y -= speed
    if keys[pygame.K_DOWN]:             #strzałka w dół
        y += speed

    player = pygame.rect.Rect(x, y, 70, 70)  #odświeżanie położenia postaci

    window.fill((104, 191, 237))      #kolor tła
    pygame.draw.rect(window,(20,200,20), player)   # wstawienie postaci
    pygame.display.update()            #odświeżamy obraz