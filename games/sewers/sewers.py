import pygame
import random
import time
import os

def sewers():
    FPS=90

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BLOCK_HEIGHT = 50

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load(pathto('lair.webp'))
    background_image = pygame.transform.scale(background_image,(SCREEN_WIDTH, SCREEN_HEIGHT) )

    pygame.display.set_caption("Препятствия")
    font = pygame.font.Font(None, 70)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load(pathto('turtle.png'))
            self.image = pygame.transform.scale(self.image, (80, 100))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - self.rect.height)  # Старт на земле
            self.on_ground = True  # Проверка, находится ли игрок на земле
            self.on_ceiling = False  # Проверка, находится ли игрок на потолке
            self.target_y = self.rect.y  # Целевая позиция по оси y

        def animate_movement(self):
            # Плавное перемещение по оси y с увеличенной скоростью

            if self.rect.y != self.target_y:
                if self.rect.y < self.target_y:  # Если нужно двигаться вниз
                    self.rect.y += 10 
                else:  # Если нужно двигаться вверх
                    self.rect.y -= 10  

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.on_ground and self.rect.y == self.target_y:
                self.image = pygame.transform.rotate(self.image, 180)
                self.image = pygame.transform.flip(self.image, True, False)
                self.on_ground = False
                self.on_ceiling = True
                self.target_y = 0
            elif keys[pygame.K_DOWN] and self.on_ceiling and self.rect.y == self.target_y:
                self.image = pygame.transform.rotate(self.image, 180)
                self.image = pygame.transform.flip(self.image, True, False)
                self.on_ceiling = False
                self.on_ground = True
                self.target_y = SCREEN_HEIGHT - self.rect.height

            self.animate_movement()

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, length, pos):
            super().__init__()
            self.image = pygame.image.load(pathto('shred.png'))
            self.image = pygame.transform.scale(self.image, (120, 300))
            self.rect = self.image.get_rect()

            if pos:  # If obstacle is at the top
                self.rect.topleft = (SCREEN_WIDTH, 0)
                self.image = pygame.transform.rotate(self.image, 180) 
            else:  # If obstacle is at the bottom
                self.rect.bottomleft = (SCREEN_WIDTH, SCREEN_HEIGHT)

            self.vel_x = -5

        def update(self):
            self.rect.x += self.vel_x
            if self.rect.right < 0:
                self.kill()
      
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    #pizza = Pizza()
    #all_sprites.add(pizza)
    #pizzas = pygame.sprite.Group()
    #pizzas.add(pizza)

    score = 0
    game_over = False
    q = False
    running = True
    clock = pygame.time.Clock()
    spawn_counter = 0
    while running:
        screen.blit(background_image, (0, 0))
        if q:
            time.sleep(5)
            return True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                score = 0
                game_over = False
                obstacles.empty()  # Clear the obstacles

        if not game_over:
            spawn_counter += 1
            if spawn_counter >= 60:
                spawn_counter = 0
                y_pos = random.choice([0, SCREEN_HEIGHT - BLOCK_HEIGHT])  # Выбор места появления препятствия
                length = random.randint(150, 250)  # Генерируем случайную длину препятствия
                obstacle = Obstacle(length, random.randint(0, 1))
                obstacles.add(obstacle)
                all_sprites.add(obstacle)

            all_sprites.update()

            hits = pygame.sprite.spritecollide(player, obstacles, False)
            if hits:
                game_over = True
                for obstacle in obstacles:
                    if hasattr(obstacle, 'passed'):
                        delattr(obstacle, 'passed')
            else:
                # Проверка, прошел ли игрок мимо препятствия
                for obstacle in obstacles:
                    if obstacle.rect.right < player.rect.left and not hasattr(obstacle, 'passed'):
                        score += 1
                        setattr(obstacle, 'passed', True)

        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            game_over = True
            for obstacle in obstacles:
                if hasattr(obstacle, 'passed'):
                    delattr(obstacle, 'passed')
    
        # Check collision with pizza
        #hits = pygame.sprite.spritecollide(player, pizzas, True)
        '''if hits:
            FPS+=10
            time.sleep(5)
            FPS-=10'''

        '''# Create new pizza if there are no collisions with obstacles
        if not any(pygame.sprite.spritecollide(pizza, obstacles, False) for pizza in pizzas):
            if len(pizzas) == 0:
              pizza = Pizza()
              all_sprites.add(pizza)
              pizzas.add(pizza)'''

    
        if score >= 30:
            #game_over_text = font.render("CONGRATULATIONS, YOU WIN", True, WHITE)
            #game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            win_image = pygame.image.load(pathto('congrats.png'))
            win_image = pygame.transform.scale(win_image, (900, 180))
            win_image_rect = win_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_image, win_image_rect)
            q = True

        all_sprites.draw(screen)

        if game_over:
            game_over = pygame.image.load(pathto('gameover.png'))
            game_over = pygame.transform.scale(game_over, (600, 120))
            game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over, game_over_rect)
            restart = pygame.image.load(pathto('tryagain.png'))
            restart = pygame.transform.scale(restart, (600, 120))
            restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80 ))
            screen.blit(restart, restart_rect)
            return False
        
        pygame.display.flip()
        clock.tick(FPS)

def pathto(f):
    return os.path.join(os.getcwd(), 'games', 'sewers', 'sprites', f)
    