import pygame
from random import randint

pygame.init()  # inicjacja
window = pygame.display.set_mode((1280, 720))


class Physic:
    def __init__(self, x, y, width, height,  acc, max_vel):
        self.x_cord = x                                #wpółrzędna x
        self.y_cord = y                                #współrzędna y
        self.hor_velocity = 0                           #prędkość w poziomie
        self.ver_velocity = 0                           #prędkośc w pionie
        self.acc = acc                                  #przyśpiesznie
        self.max_vel = max_vel                          #maksymalna prędkość
        self.width = width  # szerokość
        self.hight = height  # wysokość
        self.previous_x = x
        self.previous_y = y
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.hight)

    def physic_tick(self, beams):
        self.ver_velocity += 0.7
        self.x_cord += self.hor_velocity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.hight) # odświeżanie hitboxów
        for beam in beams:
            if beam.hitbox.colliderect(self.hitbox):   #cofanie obiektu do miejsca z poprzedniej klatki
                #self.x_cord = self.previous_x
                self.y_cord = self.previous_y
                self.ver_velocity = 0

        self.previous_x = self.x_cord
        self.previous_y = self.y_cord
class Player(Physic):
    def __init__(self):
        self.image = pygame.image.load("john.png")
        width = self.image.get_width()                                 #szerokość
        hight = self.image.get_height()                                  #wysokość
        super().__init__(0, 450, width, hight,  0.5, 5)



    def tick(self, keys, beams):                                   #wykonuje się raz na powtórznie pętli
        self.physic_tick(beams)
        if keys[pygame.K_a] and self.hor_velocity > self.max_vel * -1:
            self.hor_velocity -= self.acc
        if keys[pygame.K_d] and self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.hor_velocity > 0:
                self.hor_velocity -= self.acc
            elif self.hor_velocity < 0:
                self.hor_velocity += self.acc

    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))


class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self, window):
        pygame.draw.rect(window, (128,128,128), self.hitbox)

'''class Cash:
    def __init__(self):
        self.x_cord = randint(0,1280)
        self.y_cord = randint(0,720)
        self.image = pygame.image.load("banknot.png")
        self.width = self.image.get_width()  # szerokość
        self.hight = self.image.get_height() # wysokość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.hight)

    def tick(self):
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.hight)

    def draw(self):
        window.blit(self.image,(self.x_cord,self.y_cord))'''


def main():
    global keys
    run = True
    player = Player()
    clock = 0
    background = pygame.image.load("tło.png")
    beams =[
        Beam(7,563,1200,60)
    ]
    while run:
        clock += pygame.time.Clock().tick(60)/1000        #maks 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # jeśli gracz zamknie okno
                run = False
        keys = pygame.key.get_pressed()  # Tworzymy ruch poprzez strzałki na klawiaturze

        player.tick(keys, beams)



        window.blit(background, (0, 0))         # kolor tła
        player.draw()
        for beam in beams:
            beam.draw(window)

        pygame.display.update()  # odświeżamy obraz




if __name__ == "__main__":
    main()