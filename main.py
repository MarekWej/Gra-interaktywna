

import pygame

pygame.init()  # inicjacja
window = pygame.display.set_mode((1280, 720))

class Player:
    def __init__(self):
        self.x_cord = 0                                 #wpółrzędna x
        self.y_cord = 0                                 #współrzędna y
        self.width = 0                                  #szerokość
        self.hight = 0                                  #wysokość
        self.image = pygame.image.load("postać1.png")

    def tick(self):                                     #wykonuje się raz na powtórznie pętli
        pass
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))

def main():
    run = True
    player = Player()
    while run:
        pygame.time.Clock().tick(60)        #maks 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # jeśli gracz zamknie okno
                run = False
        player.tick()


        window.fill((104, 191, 237))  # kolor tła
        player.draw()
        pygame.display.update()  # odświeżamy obraz

        keys = pygame.key.get_pressed()  # Tworzymy ruch poprzez strzałki na klawiaturze

if __name__ == "__main__":
    main()