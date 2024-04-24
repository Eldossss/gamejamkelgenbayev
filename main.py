import pygame

import games.tanks.tanks as tanks
import games.sumo.sumo as sumo
import games.sewers.sewers as sewers
import games.match.match as match


class Game:
    def __init__(self):
        pygame.init()
        self.__here = False
        '''
            games that we already played and won
            match unlocks after completing 3, so it is not here

        '''
        self.wins = [False, False, False]
        self.won = False
        self.screen = pygame.display.set_mode((1500, 844))
        self.__loop()


    def __loop(self):
        # loop 1 for initial menus
        self.__load_show_start()
        t = True
        while t:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.menu:
                        if (767, 396) <= pos <= (1156, 578):
                            t = False
        t = True
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.guide, (0, 0))
        pygame.display.flip()

        while t:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    t = False

        self.__load_icons()
        self.__menu()
        while True:
            pygame.display.set_caption('Selection menu')   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        exit()
                    
                    elif event.key == pygame.K_o: # sneaky cheatcode for testing last game :^)
                        self.__here = False
                        match.Match()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ringRect.collidepoint(event.pos) and not self.wins[0]:
                        self.__here = False
                        self.wins[0] = sumo.sumo()

                    elif self.tankRect.collidepoint(event.pos) and not self.wins[1]:
                        self.__here = False
                        self.wins[1] = tanks.tanks()
                        pygame.mixer.quit()

                    elif self.sewerRect.collidepoint(event.pos) and not self.wins[2]:
                        self.__here = False
                        self.wins[2] = sewers.sewers()
                    
                    elif self.pizzaRect.collidepoint(event.pos) and all(self.wins):
                        self.__here = False
                        self.won = match.Match()

            pygame.display.flip()
            print(self.__here)
            if not self.__here:
                self.__menu()
            if self.won:
                break

        winimg = pygame.image.load('bg/win.jpg')
        self.screen.blit(winimg, (0, 0))
        pygame.display.flip()



    def __menu(self):
        self.screen = pygame.display.set_mode((1172, 922))
        pygame.mixer.init()
        bg = pygame.image.load('bg/bg3.png').convert_alpha()

        self.screen.blit(bg, (0, 0))
        self.__draw_icons()
        pygame.display.flip()
        self.__here = True
    
    def __load_icons(self):
        self.pizzaImg = pygame.image.load('bg/pizza.png').convert_alpha()
        self.pizzaImg = pygame.transform.scale(self.pizzaImg, (100, 100))
        self.pizzaRect = self.pizzaImg.get_rect()
        self.pizzaRect.center = (950, 200)

        self.tankImg = pygame.image.load('bg/tank.png').convert_alpha()
        self.tankImg = pygame.transform.scale(self.tankImg, (80, 60))
        self.tankRect = self.tankImg.get_rect()
        self.tankRect.center = (600, 400)


        self.ringImg = pygame.image.load('bg/ring.png').convert_alpha()
        self.ringImg = pygame.transform.scale(self.ringImg, (100, 100))
        self.ringRect = self.ringImg.get_rect()
        self.ringRect.center = (360, 640)


        self.sewerImg = pygame.image.load('bg/sewer.png').convert_alpha()
        self.sewerImg = pygame.transform.scale(self.sewerImg, (100, 50))
        self.sewerRect = self.sewerImg.get_rect()
        self.sewerRect.center = (500, 500)
        
    def __draw_icons(self):
           self.screen.blit(self.pizzaImg, self.pizzaRect)
           self.screen.blit(self.tankImg, self.tankRect)
           self.screen.blit(self.ringImg, self.ringRect)
           self.screen.blit(self.sewerImg, self.sewerRect)

    def __load_show_start(self):
        self.menu = 0
        img = pygame.image.load('bg/start.jpeg').convert_alpha()
        img = pygame.transform.scale(img, (1500, 844))
        self.guide = pygame.image.load('bg/guide.png')
        self.guide = pygame.transform.scale(self.guide, (1500, 844))
        self.screen.blit(img, (0, 0))
        pygame.display.flip()


Game()