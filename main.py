import pygame
import os 
import time 
import random 
from pygame import color
from base64 import main



pygame.font.init()

WIDTH, HEIGHT = 750, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceInvadersGame")


#load images
#enemy
RED_GROMFLOMITE_SHIP =pygame.transform.scale(  pygame.image.load(os.path.join("among","red_gromflomite.png")), (80,80))
GREEN_GROMFLOMITE_SHIP =pygame.transform.scale(  pygame.image.load(os.path.join("among","green_gromflomite.png")), (80,80))
BLUE_GROMFLOMITE_SHIP = pygame.transform.scale( pygame.image.load(os.path.join("among","blue_gromflomite.png")), (80,80))
#playerplayer
RICK_MORTY_SHIP =pygame.transform.scale( pygame.image.load(os.path.join("among","player_ship.png")), (100,100))
#lasers
RED_LASER =pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER =pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER =pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER =pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")), (WIDTH,HEIGHT))
#making the main menu animation
M1 =pygame.transform.scale(pygame.image.load(os.path.join("images","1.png")), (WIDTH,HEIGHT))
M2 =pygame.transform.scale(pygame.image.load(os.path.join("images","2.png")), (WIDTH,HEIGHT))
M3 =pygame.transform.scale(pygame.image.load(os.path.join("images","3.png")), (WIDTH,HEIGHT))
M4 =pygame.transform.scale(pygame.image.load(os.path.join("images","4.png")), (WIDTH,HEIGHT))
M5 =pygame.transform.scale(pygame.image.load(os.path.join("images","5.png")), (WIDTH,HEIGHT))
M6 =pygame.transform.scale(pygame.image.load(os.path.join("images","6.png")), (WIDTH,HEIGHT))
M7 =pygame.transform.scale(pygame.image.load(os.path.join("images","7.png")), (WIDTH,HEIGHT))
M8 =pygame.transform.scale(pygame.image.load(os.path.join("images","8.png")), (WIDTH,HEIGHT))
M9 =pygame.transform.scale(pygame.image.load(os.path.join("images","9.png")), (WIDTH,HEIGHT))
M10 =pygame.transform.scale(pygame.image.load(os.path.join("images","10.png")), (WIDTH,HEIGHT))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = RICK_MORTY_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health 

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_GROMFLOMITE_SHIP, RED_LASER),
                "green": (GREEN_GROMFLOMITE_SHIP, GREEN_LASER),
                "blue": (BLUE_GROMFLOMITE_SHIP, BLUE_LASER)
             }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move (self, vel):
        self.y += vel



def main():
    run = True 
    FPS = 60
    level = 0
    lives = 5

    main_font = pygame.font.SysFont("cosmic sans", 50)
    lost_font = pygame.font.SysFont("cosmic sans", 50)

    enemies =[]
    wave_lenght = 5
    enemy_vel = 1

    player_vel = 5
    
    player= Player(100, 550)

    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1,(255,255,255))
        level_label = main_font.render(f"Level :{level}", 1, (255,255,255))

        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() -10, 10))

        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost :/",1 ,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost: 
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy =Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel >0 : 
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: 
            player.x += player_vel
        if keys[pygame.K_UP] and player.y -player_vel > 0: 
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT: 
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        
def main_menu():
    run = True
    ck = pygame.time.Clock()
    while run:
        ck.tick(3)
        WIN.blit(M1, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M2, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M3, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M4, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M5, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M6, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M7, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M8, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M9, (0,0))
        pygame.display.update()
        ck.tick(3)
        WIN.blit(M10, (0,0))
        pygame.display.update()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()

