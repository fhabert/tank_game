import pygame 
import time
import random

pygame.init()
 
window = pygame.display.set_mode((600, 483))
pygame.display.set_caption('Tank')
playground = pygame.image.load('images/bg.jpg')
player = pygame.image.load('images/tank.png')
player2 = pygame.image.load('images/ennemi.png')
soucoupe = pygame.image.load('images/ovni.png')
manche = pygame.image.load('images/tir_manche.png')
myfont = pygame.font.Font(pygame.font.get_default_font(), 50)
myfont_life = pygame.font.Font(pygame.font.get_default_font(), 40)

pl_width = player.get_width()
pl_height = player.get_height()

class Game():
    def __init__(self):
        self.x_left = 0
        self.x_right = 600
        self.turn_move = 0
        self.moving = True
        self.ennemi_moving = False

    def draw_game(self):
        window.blit(playground, (0,0))
        window.blit(player, (my_tank.posx, my_tank.posy))
        window.blit(player2, (ennemi.posx, ennemi.posy))
        window.blit(soucoupe, (300, 40))
        my_tank.hitbox = [my_tank.posx, my_tank.posy, pl_width, pl_height]
        ennemi.hitbox = [ennemi.posx, ennemi.posy, pl_width, pl_height]
        if bullets != []:
            item = bullets[-1]
            item.force -= 0.0005
            if item.author == "player": 
                if item.force < 0:
                    item.posy -= item.force * 0.8
                    item.posx -= item.force * 0.4
                else:
                    item.posy -= item.force * my_tank.angle
                    item.posx += item.force
            else:
                if item.force < 0:
                    item.posy -= item.force * 0.8
                    item.posx += item.force * 0.4
                else:
                    item.posy -= item.force * ennemi.angle
                    item.posx -= item.force
            item.posy -= item.force * 0.1
            item.draw_bomb()
            if item.posx > game.x_right or item.posy > field.hitbox[1]:
                bullets.pop()
                self.ennemi_moving = True
                self.moving = True
            elif (item.posx > ennemi.hitbox[0] and item.posx < ennemi.hitbox[0] + ennemi.hitbox[2]) and (item.posy > ennemi.hitbox[1] and item.posy < ennemi.hitbox[1] + ennemi.hitbox[3]):
                self.draw_hit(item.author)
                ennemi.life -= 1
                if ennemi.life == 0:
                    self.draw_game_over(ennemi)
                self.ennemi_moving = True
            elif (item.posx > my_tank.hitbox[0] and item.posx < my_tank.hitbox[0] + my_tank.hitbox[2]) and (item.posy > my_tank.hitbox[1] and item.posy < my_tank.hitbox[1] + my_tank.hitbox[3]):
                self.draw_hit(item.author)
                self.moving = True
                my_tank.life -= 1
                if my_tank.life == 0:
                    self.draw_game_over(my_tank)
                self.ennemi_moving = True
        else: 
            if self.turn_move == 0:
                points = get_trajectory(my_tank, 0.49)
            # else:
            #     points = get_trajectory(ennemi, 0.49)
                draw_trajectory(points, 2)
            if self.turn_move == 1 and self.ennemi_moving:
                ennemi.move_random()
                self.ennemi_moving = False
        ennemi.draw_life()
        my_tank.draw_life()
        pygame.display.update()
    
    def draw_hit(self, author):
        text = { "player": "Hit!!", "ennemi": "Bro.." }
        text_surface = myfont.render(text[author], True, (255,255,255))
        window.blit(text_surface, (window.get_width() / 2 - len(text[author]) * 6, 10))
        pygame.display.update()
        time.sleep(1)
        bullets.pop()

    def draw_game_over(self, object):
        text = { "player": "You're dead..",
                 "ennemi": "You win!!" }
        if object.name == "player":
            text_surface = myfont.render(text["player"], True, (255,255,255))
            window.blit(text_surface, (window.get_width() / 2 - len(text["player"]) * 6, 40))
        else:
            text_surface = myfont.render(text["ennemi"], True, (255,255,255))
            window.blit(text_surface, (window.get_width() / 2 - len(text["ennemi"]) * 6, 40))
        pygame.display.update()
        time.sleep(1)
        ennemi.life = 3
        my_tank.life = 2

class Tank():
    def __init__(self, posx, posy, angle, name, life):
        self.posx = posx
        self.posy = posy
        self.angle = angle
        self.name = name
        self.hitbox = [self.posx, self.posy, pl_width, pl_height]
        self.bullet_tank = []
        self.life = life
    
    def drawhitbox(self):
        pygame.draw.rect(window, (255,255,255), pygame.Rect(self.hitbox[0], self.hitbox[1],
                        self.hitbox[2], self.hitbox[3]), 2)

    def launch_missile(self, bullets):
        if self.name == "player":
            x_bomb = self.posx + pl_width + 10
            author = "player"
        else:
            x_bomb = self.posx
            author = "ennemi"
        bomb = Bomb(x_bomb, self.posy, author)
        bullets.append(bomb)

    def draw_life(self):
        text = { "Life": str(self.life) }
        if self.name == "player":
            text_surface = myfont_life.render(f"Your life: {text['Life']}", True, (255,255,255))
            window.blit(text_surface, (10, 10))
        else:
            text_surface = myfont_life.render(text['Life'], True, (255,255,255))
            window.blit(text_surface, (550 - len(str(text['Life'])), 10))

    def move_random(self):
        nb_rand = random.randint(0, 100)
        posx = self.posx
        speed = 0.001
        if posx - nb_rand > window.get_width() / 2:
            for _ in range(100000): 
                self.posx -= speed
        else:
            for _ in range(100000): 
                self.posx += speed

class Bomb():
    def __init__(self, posx, posy, author):
        self.posx = posx
        self.posy = posy
        self.author = author
        self.color = (255,255,255)
        self.mass = 0.05
        self.acceleration = 9.8
        self.force = self.mass * self.acceleration    

    def draw_bomb(self):
        pygame.draw.circle(window, self.color, ((self.posx), (self.posy)), 10)

class Terrain():
    def __init__(self):
        self.hitbox = [0, window.get_height() / 2 + 80, window.get_width(), window.get_height() / 2 - 80]

def get_trajectory(my_tank, force):
    points = []
    if game.turn_move == 0:
        posx = my_tank.hitbox[0] + my_tank.hitbox[2]
    else:
        posx = my_tank.hitbox[0]
    posy = my_tank.hitbox[1]
    start_posy = posy + 0.5
    while posy < start_posy:
        force -= 0.0005
        if force < 0:
            posy -= force * 0.8
            if game.turn_move == 0:
                posx -= force * 0.4
            else:
                posx += force * 0.4
        else:
            if game.turn_move == 0:
                posy -= force * my_tank.angle
                posx += force
            else:
                posy -= force * ennemi.angle
                posx -= force
        points.append((posx, posy))
    return points

def draw_trajectory(points, radius):
    for i in range(len(points)):
        if i % 50 == 0:
            pygame.draw.circle(window, (255,255,255), (points[i][0], points[i][1]), radius)
    

bullets = []
angle_options = [0.1, 0.8, 1.5]
game = Game()
my_tank = Tank(100, 280, angle_options[0], "player", 2)
ennemi = Tank(450, 280, angle_options[0], "ennemi", 3)
field = Terrain()
position_options = [0.1, 0.3, 0.4, 0.8, 0.9]

run = True
counter = 0
angle_bool = 0


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and (my_tank.posx + player.get_width()) < game.x_right / 2 and game.moving:
        my_tank.posx += 0.2
    elif keys[pygame.K_LEFT] and my_tank.posx > game.x_left and game.moving:
        my_tank.posx -= 0.1
    elif keys[pygame.K_SPACE] and game.turn_move == 0:
        my_tank.launch_missile(bullets)
        game.turn_move = 1
        factor = random.randint(0, len(position_options) - 1)
        ennemi.angle = position_options[factor]

    if keys[pygame.K_TAB] and game.turn_move == 1:
        ennemi.launch_missile(bullets)
        game.moving = False
        game.turn_move = 0

    if bullets == []:
        shoot = 0

    if pygame.key.get_pressed()[pygame.K_UP] and event.type == pygame.KEYDOWN and counter == 0:
        counter = 1
        my_tank.angle = angle_options[counter]
        pygame.time.delay(160)
    elif pygame.key.get_pressed()[pygame.K_UP] and event.type == pygame.KEYDOWN and counter == 1:
        counter = 2
        my_tank.angle = angle_options[counter]
        pygame.time.delay(160)
    elif pygame.key.get_pressed()[pygame.K_DOWN] and event.type == pygame.KEYDOWN and counter == 2:
        counter = 1
        my_tank.angle = angle_options[counter]
        pygame.time.delay(160)
    elif pygame.key.get_pressed()[pygame.K_DOWN] and event.type == pygame.KEYDOWN and counter == 1:
        counter = 0
        my_tank.angle = angle_options[counter]
        pygame.time.delay(160)
        
    game.draw_game()

pygame.quit()
