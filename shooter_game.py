#Создай собственный Шутер!

from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_press = key.get_pressed()
        if key_press[K_d] and self.rect.x < width-80:
            self.rect.x += self.speed
        if key_press[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.centery, 5, 20, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > 460:
            self.rect.y = 0
            self.rect.x = randint(0, 700)
            missed += 1
        
class Bullet(GameSprite):
    def update(self):   
        self.rect.y -= self.speed


#backround
window = display.set_mode((700, 500))
display.set_caption('shooter')
background = transform.scale(image.load("galaxy.jpg"), (800, 500))

#счет
score = 0
missed = 0

font.init()
font1 = font.Font(None, 40)
font2 = font.Font(None, 70)

#window
width = 700
height = 500

#логика
clock = time.Clock()
FPS = 70
game = True
finish = False

#music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#sprite
player = Player('rocket.png',350,430,5, 65, 65)
enemy1 = Enemy('ufo.png',randint(0, 700), 0, randint(1, 2), 80, 65)
enemy2 = Enemy('ufo.png',randint(0, 700), 0, randint(1, 2), 80 , 65)
enemy3 = Enemy('ufo.png',randint(0, 700), 0, randint(1, 2), 80, 65)
enemy4 = Enemy('ufo.png',randint(0, 700), 0, randint(1, 2), 80, 65)
enemy5 = Enemy('ufo.png',randint(0, 700), 0, randint(1, 2), 80, 65)

bullets = sprite.Group()

monsters = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)

#цикл 
while game:

    for e in event.get():
        if e.type == QUIT:
          game = False
    
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if finish != True:

        soccer = font1.render('Счет:' + str(score), True, (255, 250, 250))
        misser = font1.render('Пропущено:' + str(missed), True, (255, 250, 250))

        win = font2.render('YOU WIN!', True, (255, 215, 0))
        lose = font2.render('YOU LOSE!', True, (180, 0, 0))

        window.blit(background,(0,0))
        window.blit(soccer, (10, 0))
        window.blit(misser, (10, 30))

        player.update()
        player.reset()

        bullets.update()
        bullets.draw(window)

        monsters.update()
        monsters.draw(window)

        if sprite.spritecollide(player, monsters, False):
           finish = True
           window.blit(lose, (200, 200))

        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for collide in collides:
            enemy = Enemy('ufo.png',randint(0, 700), 0, randint(1, 3), 80, 65)
            monsters.add(enemy)
            score+=1
        if score == 10:
            finish = True
            window.blit(win, (200, 200))
        if missed==10:
           finish = True
           window.blit(lose, (200, 200))


    clock.tick(FPS)
    display.update()