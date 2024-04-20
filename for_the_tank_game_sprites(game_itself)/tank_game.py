import pygame
import os
from random import randint

pygame.init()
background_image = pygame.image.load("background1.jpg")
bonus_img = pygame.image.load("bonus_star.png")
bang_img = pygame.image.load("kunai.png")
background_image = pygame.transform.scale(background_image, (800, 600))
TILE = 32
WIDTH, HEIGHT = 800, 600
FPS = 60
start_song = pygame.mixer.music.load("level_start.mp3")
pygame.mixer.music.play()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
imgBangs = [
    pygame.image.load('bang1.png'),
    pygame.image.load('bang2.png'),
    pygame.image.load('bang3.png'),
]
imgBrick = pygame.image.load('drawka.jpg')

class UI:
    def __init__(self):
        self.blue_kills = 0
        self.red_kills = 0
        self.blue_kill_text = fontUI.render(str(self.blue_kills), 1, (0, 0, 255))
        self.red_kill_text = fontUI.render(str(self.red_kills), 1, (255, 0, 0))

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1
        window.blit(self.blue_kill_text, (WIDTH - 150, 10))
        window.blit(self.red_kill_text, (WIDTH - 80, 10))

    def update_kills(self, player_color):
        if player_color == 'blue':
            self.red_kills += 1
            self.red_kill_text = fontUI.render(str(self.red_kills), 1, (255, 0, 0))
        elif player_color == 'red':
            self.blue_kills += 1
            self.blue_kill_text = fontUI.render(str(self.blue_kills), 1, (0, 0, 255))


class Tank:
    def __init__(self, color, px, py, direct, keyList, images):
        objects.append(self)
        self.type = 'tank'
        self.active = True
        self.respawn_time = 0
        self.color = color
        self.shotSound = pygame.mixer.Sound("shot.wav")
        self.dead = pygame.mixer.Sound("dead.wav")
        self.images = images
        self.image = self.images[direct]
        self.rect = self.image.get_rect()
        self.rect.topleft = (px, py)
        self.direct = direct
        self.moveSpeed = 4
        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
        self.shotTimer = 0
        self.shotDelay = 30
        self.bulletSpeed = 8
        self.bulletDamage = 1
        self.hp = 5

    def update(self):
        if not self.active:
            if self.respawn_time <= 0:
                self.rect.topleft = (100, 275) if self.color == 'blue' else (650, 275)
                self.active = True
                self.hp = 5
                self.respawn_time = 0
            else:
                self.respawn_time -= 1
        else:
            oldX, oldY = self.rect.topleft
            if keys[self.keyLEFT] and self.rect.left > 0:
                self.rect.x -= self.moveSpeed
                self.direct = 3
            elif keys[self.keyRIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.moveSpeed
                self.direct = 1
            elif keys[self.keyUP] and self.rect.top > 0:
                self.rect.y -= self.moveSpeed
                self.direct = 0
            elif keys[self.keyDOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.moveSpeed
                self.direct = 2
            for obj in objects:
                if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                    self.rect.topleft = oldX, oldY
            if keys[self.keySHOT] and self.shotTimer == 0:
                self.shotSound.play()
                dx = DIRECTS[self.direct][0] * self.bulletSpeed
                dy = DIRECTS[self.direct][1] * self.bulletSpeed
                BangBullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
                self.shotTimer = self.shotDelay
            if self.shotTimer > 0:
                self.shotTimer -= 1

    def draw(self):
        if self.active:
            self.image = self.images[self.direct]
            window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            self.dead.play()
            self.active = False
            self.respawn_time = 0  # Устанавливаем время возрождения на 0, чтобы танк сразу появлялся после смерти
            ui.update_kills(self.color)

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break

    def draw(self):
        pygame.draw.circle(window, 'purple', (self.px, self.py), 2)

class BangBullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break

    def draw(self):
        window.blit(bang_img, (self.px, self.py))

class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.1
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value

        if self.hp <= 0:
            objects.remove(self)

objects = []
bullets = []

blue_tank_images = [
    pygame.image.load('blue_tank_up.png'),
    pygame.image.load('blue_tank_right.png'),
    pygame.image.load('blue_tank_down.png'),
    pygame.image.load('blue_tank_left.png')
]

red_tank_images = [
    pygame.image.load('red_tank_up.png'),
    pygame.image.load('red_tank_right.png'),
    pygame.image.load('red_tank_down.png'),
    pygame.image.load('red_tank_left.png')
]

Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), blue_tank_images)
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER), red_tank_images)

ui = UI()

for _ in range(50):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True
        if not fined:
            break
    Block(x, y, TILE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()
    for bullet in bullets:
        bullet.update()
    for obj in objects:
        obj.update()
    ui.update()

    window.blit(background_image, (0, 0))
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    ui.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()