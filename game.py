import pygame
from random import randint
from math import floor, sqrt, degrees, asin

resolution = (1280, 720)

def degree(x_screen, y_screen, x_mouse, y_mouse):
    x_side = x_screen - x_mouse
    y_side = y_screen - y_mouse
    triangle_long =sqrt(x_side**2 + y_side**2)
    dg = degrees(asin(y_side / triangle_long))
    if x_side > 0:
        dg = -dg
    return dg

def centered_rotate(image, x, y, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center =(x,y)).center)
    return rotated_image, new_rect


class Physic:
    def __init__(self, x, y, width, height,  acc, max_vel):
        self.x_cord = x                                #wpółrzędna x
        self.y_cord = y                                #współrzędna y
        self.hor_velocity = 0                           #prędkość w poziomie
        self.ver_velocity = 0                           #prędkośc w pionie
        self.acc = acc                                  #przyśpiesznie
        self.max_vel = max_vel                          #maksymalna prędkość
        self.width = width  # szerokość
        self.height = height  # wysokość
        self.previous_x = x
        self.previous_y = y
        self.jumping = False                            #czy postać skacze
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.gravity = 0.7

    def physic_tick(self, beams):
        self.ver_velocity += self.gravity
        self.x_cord += self.hor_velocity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height) # odświeżanie hitboxów
        for beam in beams:
            if beam.hitbox.colliderect(self.hitbox):   #cofanie obiektu do miejsca z poprzedniej klatki
                if self.x_cord + self.width >= beam.x_cord + 1 > self.previous_x + self.width:  #kolizja z prawej strony
                    self.x_cord = self.previous_x
                    self.hor_velocity = 0
                if self.x_cord <= beam.x_cord + beam.width - 1 < self.previous_x:  # kolizja z lewej strony
                    self.x_cord = self.previous_x
                    self.hor_velocity = 0
                if self.y_cord + self.height >= beam.y_cord + 1 > self.previous_y + self.height:
                    self.y_cord = self.previous_y
                    self.ver_velocity = 0
                    self.jumping = False
                if self.y_cord <= beam.x_cord + beam.width - 1 < self.previous_y:
                    self.y_cord = self.previous_y
                    self.ver_velocity = 0


        self.previous_x = self.x_cord
        self.previous_y = self.y_cord



class Health:
    def __init__(self, max_health = 100):
        self.health = max_health
        self.max_health = max_health                #ilość punktów życia
        self.alive = True                           #czy postać żyje
        self.last_damage = 0                        #czas od ostatnich obrażenień


    def health_tick(self, deal_tm):
        self.last_damage += deal_tm

    def dealt_damage(self, damage, hit_speed):
        if  self.last_damage > hit_speed:
            self.health -= damage
            self.last_damage = 0
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def draw_health(self, window, x, y, max_width, height):
        percent_width = self.health / self.max_health
        width = round(max_width * percent_width)
        if self.health > 30:
            color = (30, 255, 30)
        else:
            color = (255,30,30)
        pygame.draw.rect(window, (30,30,30), (x, y, max_width, height))
        pygame.draw.rect(window,color, (x, y, width, height))

class button:
    def __init__(self, x_cord, y_cord, file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f'button.png')
        self.hovered_button_image = pygame.image.load(f'button_start.png')
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height()) # hitbox przycisku "start"

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hovered_button_image,(self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image,(self.x_cord, self.y_cord))

class TextInput:
    def __init__(self,x , y, width, height, maxlen = -1, placeholder = ""):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Field", 63)
        self.text = ""
        self.font_image = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
        self.placeholder = placeholder
        self.placeholder_img = pygame.font.Font.render(self.font,  placeholder, True, (100,100,100))
        self.maxlen = maxlen
        self.isactive = False
        self.cursor = pygame.rect.Rect(self.x_cord + 5, self.y_cord + 5, 2, 40)
        self.cursor_visibility = True

    def tick(self, clock, events):
        for event in events:
            if event.type == pygame.KEYDOWN:                    #jeżeli jakiś klawisz zostanie naciśnięty
                if event.key == pygame.K_RETURN:                #jeżeli enter zostanie naciśnięty
                    return self.text
                elif event.key == pygame.K_BACKSPACE:           #jeżeli backspace zostanie naciśnięty
                    self.text = self.text[: -1]                 #usuwa ostatni krok
                elif len(self.text) < self.maxlen or self.maxlen == -1:
                    if self.isactive and event.unicode.isprintable():
                        self.text += event.unicode

                self.font_image = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
                text_x = self.font_image.get_width()
                self.cursor = pygame.rect.Rect(self.x_cord + 5 + text_x, self.y_cord + 5, 2, 40)

        if round(clock) % 2 == 0:
            self.cursor_visibility = True
        else:
            self.cursor_visibility = False


        if pygame.mouse.get_pressed(3)[0]:                      #jeśli zostanie naciśnięty lewy przycisk myszy
            if pygame.rect.Rect(self.x_cord, self.y_cord, self.width,
                                self.height). collidepoint(pygame.mouse.get_pos()):
                self.isactive = True
            else:
                self.isactive = False
    def draw(self, window):
        pygame.draw.rect(window, (4 ,207, 222),
                         (self.x_cord -4, self.y_cord -4, self.width +8,self.height +8),
                         border_radius= 45)
        pygame.draw.rect(window, (255, 255, 255),
                         (self.x_cord, self.y_cord, self.width, self.height),
                         border_radius=45)
        if self.text:

            window.blit(self.font_image, (self.x_cord + 5, self.y_cord + 5))
        else:
            window.blit(self.placeholder_img, (self.x_cord + 5, self.y_cord + 5))

        if self.cursor_visibility:
            pygame.draw.rect(window, (90,90,90), self.cursor)

class Bullet(Physic):
    def __init__(self, gun, speed, damage, x_side, y_side):
        super().__init__(gun.x_cord, gun.y_cord, 3 ,2 ,0 ,speed)
        self.gravity = 0.1
        c_side = sqrt(x_side**2 + y_side**2)
        step = c_side/speed
        x_speed = x_side / step
        y_speed = y_side / step
        self.hor_velocity = x_speed
        self.ver_velocity = y_speed
        self.damage = damage
        self.clock = 0
        self.exists = 1
    def tick(self, beams, delta, mobs):
        self.physic_tick(beams)
        self.clock += delta
        if self.clock > 1:
            self.exists = False
        for mob in mobs:
            if mob.hitbox.colliderect(self.hitbox):
                mob.dealt_damage(self.damage, 0)
                self.exists = False


    def draw(self,window, world_x):
        pygame.draw.rect(window,(242,0,20),(self.x_cord + world_x, self.y_cord, 5, 3))


class Weapon:
    def __init__(self, speed, damage):
        self.x_cord = 0
        self.y_cord = 0
        self.speed = speed
        self.damage = damage
        self.bullets = []
        self.image = pygame.image.load("ak47.png")
        self.x_screen = 0
        self.x_world = 0
        self.clock = 1
    def shoot(self):
        if self.clock > 0.1:
            self.clock = 0
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x_side = x_mouse - self.x_screen - self.x_world
            y_side = y_mouse - self.y_cord
            self.bullets.append(Bullet(self, self.speed, self.damage, x_side, y_side))

    def tick(self, beams, player, delta, mobs):
        self.clock += delta
        self.x_cord = player.x_cord
        self.y_cord = player.y_cord
        for bullet in self.bullets:
            bullet.tick(beams, delta, mobs)
            if not bullet.exists:
                self.bullets.remove(bullet)

    def draw(self, window, x_screen, world_x):
        self.x_screen = x_screen
        self.x_world = 0
        for bullet in self.bullets:
            bullet.draw(window, world_x)
        angle = degree(x_screen + world_x, self.y_cord, *pygame.mouse.get_pos())
        if pygame.mouse.get_pos()[0] - x_screen - world_x < 0:
            image = pygame.transform.flip(self.image, True, False)
        else:
            image = self.image
        to_blit = centered_rotate(image, x_screen + world_x + 30, self.y_cord + 35 ,angle)
        window.blit(*to_blit)



class Player(Physic, Health):
    def __init__(self):
        self.stand_right_img = pygame.image.load("john.png")
        self.stand_left_img = pygame.transform.flip(pygame.image.load("john.png"), True, False)          #odwracanie postaci
        width = self.stand_right_img.get_width()                                                         #szerokość
        height = self.stand_right_img.get_height()                                                       #wysokość
        Health.__init__(self, 100)
        Physic.__init__(self,0, 450, width, height,  0.5, 5)
        self.jump_right_img = pygame.image.load('jump.png')                                              #skok
        self.jump_left_img = pygame.transform.flip(pygame.image.load('jump.png'), True, False)
        self.walk_right_img = [pygame.image.load(f'walk/klatka0{x}.png') for x in range(1, 7)]
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'walk/klatka0{x}.png'), True, False) for x in range(1, 7)]
        self.walk_index = 0
        self.direction = 1

        self.weapon = Weapon(20,20)



    def tick(self, keys, beams, delta_tm ,mobs):                                                                        #wykonuje się raz na powtórznie pętli
        self.physic_tick(beams)
        self.health_tick(delta_tm)
        self.weapon.tick(beams,self, delta_tm, mobs)
        if not self.alive:
            return
        if pygame.mouse.get_pressed(3)[0]: #jeśli gracz wciśnie lewy przycisk
            self.weapon.shoot()
        if keys[pygame.K_a] and self.hor_velocity > self.max_vel * -1:
            self.hor_velocity -= self.acc
        if keys[pygame.K_d] and self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc
        if keys[pygame.K_SPACE] and self.jumping is False:
            self.ver_velocity -= 15
            self.jumping = True
        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.hor_velocity > 0:
                self.hor_velocity -= self.acc
            elif self.hor_velocity < 0:
                self.hor_velocity += self.acc

    def draw(self, window, background):
        if background.width - resolution[0] / 2 > self.x_cord >= resolution[0] / 2:
            x_screen = resolution[0] / 2
        elif self.x_cord >= background.width - resolution[0] / 2 :
            x_screen = self.x_cord - background.width + resolution[0]
        else:
            x_screen = self.x_cord

        self.draw_health(window, x_screen, self. y_cord - 15, self.width, 10)


        if self.jumping:
            if self.direction == 0:
                window.blit(self.jump_left_img, (x_screen, self.y_cord))
            elif self.direction == 1:
                window.blit(self.jump_right_img, (x_screen, self.y_cord))
        elif self.hor_velocity != 0:
            if self.direction == 0:
                window.blit(self.walk_left_img[floor(self.walk_index)], (x_screen, self.y_cord))
            elif self.direction == 1:
                window.blit(self.walk_right_img[floor(self.walk_index)], (x_screen, self.y_cord))
            self.walk_index += 1
            if self.walk_index > 5:
                self.walk_index = 0
        else:
            if self.direction == 0:
                window.blit(self.stand_left_img,(x_screen, self.y_cord))
            elif self.direction == 1:
                window.blit(self.stand_right_img, (x_screen, self.y_cord))
        self.weapon.draw(window, self.x_cord, background.x_cord)







class Enemy(Physic, Health):
    def __init__(self, x , y):
        self.image = pygame.image.load('Edgar2.png')
        width, height = self.image.get_size()
        Physic.__init__(self,x, y, width, height, 1, 3)
        Health.__init__(self, 75)
        self.gravity = 0.2

    def go_left(self):
        if -self.hor_velocity < self.max_vel:
            self.hor_velocity -= self.acc

    def go_right(self):
        if self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc

    def go_up(self):
        if -self.ver_velocity < self.max_vel:
            self.ver_velocity -= self.gravity + self.acc


    def tick(self, beams, player, delta):
        self.physic_tick(beams)
        self.health_tick(delta)
        if self.hitbox.colliderect(player.hitbox):
            player.dealt_damage(10, 0.5)                #10 zadanych obrażeń w ciągu 0.5 sek
        if not self.hitbox.colliderect(player.hitbox):
            if self.y_cord > player.y_cord + 15:
                self.go_up()
            if self.x_cord > player.x_cord:
                self.go_left()
            elif self.x_cord < player.x_cord:
                self.go_right()
            if abs(self.x_cord - player.x_cord) > 40:
                helphitbox = pygame.rect.Rect(self.x_cord - 15, self.y_cord + 20, self.width + 30, self.height -25 )
                for beam in beams:
                    if helphitbox.colliderect(beam.hitbox):
                        self.go_up()
            if randint(0, 30) == 15:
                self.go_up()


    def draw(self, window, world_x):
        window.blit(self.image, (self.x_cord + world_x, self.y_cord))
        self.draw_health(window, self.x_cord, self.y_cord - 15, self.width, 10)





class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self, window , background_x):
        pygame.draw.rect(window, (128, 128, 128), (self.x_cord + background_x, self.y_cord, self.width, self.height))

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
class Background:
    def __init__(self):
        self.x_cord = 0
        self.y_cord = 0
        self.image = pygame.image.load('scrolling.png')
        self.width = self.image.get_width()

    def tick(self,player):
        if self.width - resolution[0] / 2 > player.x_cord >= resolution[0] / 2:
            self.x_cord -= player.hor_velocity
        elif player.x_cord >= self.width - resolution[0] / 2:
            self.x_cord = - self.width + resolution[0]
        else:
            self.x_cord = 0

    def draw(self, window):
        window.blit(self.image, (self.x_cord, self.y_cord))