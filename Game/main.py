# content from kids can code: http://kidscancode.org/blog/
# append into list https://www.digitalocean.com/community/tutorials/python-add-to-list
# min() https://www.geeksforgeeks.org/python-program-to-find-smallest-number-in-a-list/
# abs() https://www.toppr.com/guides/python-guide/questions/change-positive-negative-python/
# Thank you to Tyson for being a stress ball

'''
future plans:
Power-up class
Mob moving randomly and shooting randomly
Spirites
Levels
Different types of mobs
 - Moves towards and pathes towards the player
 - Shooter Imma shoot u

Rlly far future plans:
Different guns
animations
Menu: pause and start
Level selector
Particals
NPC's and money
Move outside the window so like more space
In-game transactions
'''

# import libraries and modules
# from platform import platform
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from settings import *

vec = pg.math.Vector2
shootClock = 0
canShot = True
shootermobs = []

# Function that draws text (Don't know to much about it since it was a copy and paste inclass)
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# Function that gets a random number that it in the color wheel so I can get a random color for the mobs
def colorbyte():
    return random.randint(0,255)

# Classes
# Player class with the ability to have size, color, being a rectangle but to the computer, and movement
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    # Controls that when a key is pressed it will check to see what key then depending on the key will move in a direction
    def controls(self):
        global canShot
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_c]:
            def throwBullet():
                bullet = Bullet(20, 20, RED, "player", self)
                all_sprites.add(bullet)
                all_bullets.add(bullet)
                allBull.append(bullet)
                bullet.fly()
            
            if canShot == True:
                throwBullet()
                canShot = False

    # Jump but only when touching a platform
    def jump(self):
        hits = pg.sprite.spritecollide(self, all_plats, False)
        if hits:
            self.vel.y = -20
            
    # Update so whenever a frame is going on this runs and constantly updates the class so things like gravity can exist
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms class that have xy cords, size, and color
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Mob class that have xy cords, size, and color
class Mob(Sprite):
    def __init__(self, x, y, w, h, color, move):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.move = move
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = x, y
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.mobframe = 0
        self.mobskip = True
        if move == False:
            shootermobs.append(self)
    
    def shot(self):
        if self.move == False:
            bullet = Bullet(20, 20, RED, "mob", self)
            all_sprites.add(bullet)
            all_bullets.add(bullet)
            allBull.append(bullet)
            bullet.fly()

    def mover(self):
            self.vel.x = (player.rect.center[0] - (self.rect.center[0]))/20
            self.vel.y = (player.rect.center[1] - (self.rect.center[1]))/20

# Like the player, mob also has a update method so the gravity can be a thing
    def update(self):
        self.acc = vec(0,GRAVITY)
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if len(m) > 0:
            if self.move == True:
                if self.mobskip == True:
                    self.mobskip = False
                    self.mobframe = FRAME
                if self.mobskip == False:
                    if FRAME - self.mobframe >= 5:
                        self.mobskip = True
                        self.mover()
            if self.move == False:
                if self.mobskip == True:
                    self.mobskip = False
                    self.mobframe = FRAME
                if self.mobskip == False:
                    if FRAME - self.mobframe >= 20:
                        self.mobskip = True
                        self.shot()
        
        mobhits = pg.sprite.spritecollide(self, player0, False)
        global HEALTH, SCORE, fakeSCORE
        if mobhits:
            self.kill()
            m.remove(self)
            if self.move == False:
                shootermobs.remove(self)
            HEALTH -= 1
            fakeSCORE += 1
            if SCORE != 0:
                SCORE -= 1

# Bullet calls that has the same property as everything else
class Bullet(Sprite):
    def __init__(self, w, h, color, who, whatmob):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.whatmob = whatmob
        self.image.fill(color)
        self.who = who
        self.rect = self.image.get_rect()
        if who == "player":
            self.pos = (player.rect.center[0], player.rect.center[1])
            self.rect.x = player.rect.center[0] - 10
            self.rect.y = player.rect.center[1] - 10
        if who == "mob":
            # for i in range(len(shootermobs)):
            #     self.pos = (shootermobs[i].rect.center[0], shootermobs[i].rect.center[1])
            #     self.rect.x = shootermobs[i].rect.center[0] - 10
            #     self.rect.y = shootermobs[i].rect.center[1] - 10
            self.pos = (whatmob.rect.center[0], whatmob.rect.center[1])
            self.rect.x = whatmob.rect.center[0] - 10
            self.rect.y = whatmob.rect.center[1] - 10
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.frame = 0
        self.skip = True

    
    # Also has a update but without gravity
    def update(self):
        global HEALTH, SCORE, fakeSCORE
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.pos[0] < 0:
            self.kill()
        elif self.pos[0] > WIDTH:
            self.kill()
        elif self.pos[1] < 0:
            self.kill()
        elif self.pos[1] > HEIGHT:
            self.kill()

        # For all bullets in the list, check to see if it has hit a mob and if so then add to the score and delete the mob
        if self.who == "player":
            bullethitsmob = pg.sprite.spritecollide(self, mobs, True)
            if bullethitsmob:
                if len(m) > 0:
                    m.remove(bullethitsmob[0])
                if len(mobshooters) > 0:
                    shootermobs.remove(bullethitsmob[0])
                SCORE += 5
                fakeSCORE += 1

        # for i in range(len(m)):
        if self.who == "mob":
            # for o in range(len(allBull)):
            bullethitsplayer = pg.sprite.spritecollide(self, player0, False)
            if bullethitsplayer:
                HEALTH -= 1
                if SCORE != 0:
                    SCORE -= 1
                self.kill()

        if self.skip == True:
            self.skip = False
            self.frame = FRAME
        if self.skip == False:
            if FRAME - self.frame >= 50:
                self.skip = True
                self.kill()

    # Fly really just gets the cords of all mobs on screen then compares to know which to shoot at
    def fly(self):
        # Gets the players cords
        playerX = player.rect.center[0]
        playerY = player.rect.center[1]

        # Empty list for later use
        mobDistance = []
        bulletXY = []

        if self.who == "mob":
            # for i in range(len(shootermobs)):
            self.vel.x = (playerX - (self.whatmob.rect.center[0]))/10
            self.vel.y = (playerY - (self.whatmob.rect.center[1]))/10

            # For each mob in the mob list, find the distance from the player then put it in the list from earlier
        for mob in m:
            if self.who == "player":   
                mobX = abs(playerX - (mob.rect.center[0]))
                mobY = abs(playerY - (mob.rect.center[1]))
                bulletXY.append(playerX - (mob.rect.center[0]))
                bulletXY.append(playerY - (mob.rect.center[1]) - 10)
                mob = mobY + mobX
                mobDistance.append(mob)

                # Finds the closest mob and based off which one it is it will find the slope then shoots at it
                mobClosest = min(mobDistance)
                if mobClosest == mobDistance[0]:
                    self.vel.x = (bulletXY[0]) * -.1
                    self.vel.y = (bulletXY[1]) * -.1
                elif mobClosest == mobDistance[1]:
                    self.vel.x = (bulletXY[2]) * -.1
                    self.vel.y = (bulletXY[3]) * -.1
                elif mobClosest == mobDistance[2]:
                    self.vel.x = (bulletXY[4]) * -.1
                    self.vel.y = (bulletXY[5]) * -.1
                elif mobClosest == mobDistance[3]:
                    self.vel.x = (bulletXY[6]) * -.1
                    self.vel.y = (bulletXY[7]) * -.1
                elif mobClosest == mobDistance[4]:
                    self.vel.x = (bulletXY[8]) * -.1
                    self.vel.y = (bulletXY[9]) * -.1

class PowerUp(Sprite):
    def __init__(self, color):
        Sprite.__init__(self)
        self.color = color
        self.image.fill(color)
        self.image = pg.Surface((20, 20))
        self.rect = self.image.get_rect()

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create sprite groups so we can check for collisions and draw it in
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
all_bullets = pg.sprite.Group()
player0 = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(0, HEIGHT - 125, WIDTH, 60)
plat2 = Platform(280, (HEIGHT / 2) + 180, 200, 35)
m1 = Mob(randint(0,WIDTH), randint(100,HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), True)
m2 = Mob(randint(0,WIDTH), randint(100,HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), False)
m3 = Mob(randint(0,WIDTH), randint(100,HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), True)


# Adds all bullets put in the allBulls list into sprite groups
allBull = []
all_sprites.add(allBull)
all_bullets.add(allBull)

# add mobs in sprite group
m = [m1, m2, m3]
mobshooters = []
# List of mobs but the form of the names of the mobs can't be changed so it can not be used to identify certain mobs
all_sprites.add(m)
mobs.add(m)

# add player to all sprites groupad
all_sprites.add(player)
player0.add(player)

# add platform to all sprites group and all platforms groups
all_sprites.add(plat, plat2)
all_plats.add(plat, plat2)
allplats = []
allplats.append(plat)
allplats.append(plat2)

# Game loop
running = True
while running:

    # keeps the loop running using clock
    clock.tick(FPS)

    FRAME += 1

    # For every mob in mob list, check if they collide with a platform and if teleport to the top and set y velocity to 0
    for i in range(len(m)):
        hits = pg.sprite.spritecollide(m[i], all_plats, False)
        if hits:
            m[i].pos.y =  hits[0].rect.top
            m[i].vel.y = 0
    
    # check if player collide with a platform and if teleport to the top and set y velocity to 0
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        player.pos.y = hits[0].rect.top
        player.vel.y = 0
    
    # if player hits a mob then get one point and deletes the mob but im prolly gonna change it to deal damage
    # for i in range(len(m)):
    #     mobhits = pg.sprite.spritecollide(player, mobs, True)
    #     if mobhits:
    #         m.remove(mobhits[0])
    #         shootermobs.remove(mobhits[0])
    #         HEALTH -= 1
    #         fakeSCORE += 1
    #         if SCORE != 0:
    #             SCORE -= 1

    if len(mobs) != len(m):
        fakeSCORE += 1
        SCORE += 1
        m.pop()
    
    for i in range(len(allplats)):
        bullethitWall = pg.sprite.spritecollide(allplats[i], all_bullets, True)
        if bullethitWall:
            allBull.remove(bullethitWall[0])    
            all_bullets.remove(bullethitWall[0])

    for i in range(len(allBull)):
        if allBull[0].pos[0] <= 0:
            allBull.remove(allBull[0])       
        elif allBull[0].pos[0] >= WIDTH:
            allBull.remove(allBull[0])
        elif allBull[0].pos[1] <= 0:
            allBull.remove(allBull[0])
        elif allBull[0].pos[1] >= HEIGHT:
            allBull.remove(allBull[0])

    if player.pos.x < 0:
        player.pos.x = WIDTH
    elif player.pos.x > WIDTH:
        player.pos.x = 0
    
    for i in range(len(m)):
        if m[i].pos[0] < 0:
            m[i].pos[0] = WIDTH
        elif m[i].pos[0] > WIDTH:
            m[i].pos[0] = 0

    if canShot == False:
        shootClock += 1
    if shootClock == 5:
        canShot = True
        shootClock = 0

    if SCORE >= 10 and fakeSCORE == 3:
        if allplats[1] == plat2:
            allplats.pop(1)
            plat2.kill()
            plat3 = Platform(560, (HEIGHT / 2) + 180, 200, 35)
            all_sprites.add(plat3)
            all_plats.add(plat3)
            allplats.append(plat3)
            fakeSCORE = fakeSCORE + 2
    
    if SCORE <= 9:
        mobmove = True
        if fakeSCORE >= 3: 
            if skip == True:
                skip = False
                frame = FRAME
            if skip == False:
                if FRAME - frame == 15:
                    fakeSCORE = 0
                    skip = True
                    for i in range(3):
                        if mobmove == True:
                            newMob = Mob(randint(0,WIDTH), randint(100, HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), True)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.append(newMob)
                            mobmove = False
                        else:
                            newMob = Mob(randint(0,WIDTH), randint(100, HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), False)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.insert(0, newMob)
                            mobmove = True

    if SCORE <= 20 and SCORE >= 10:
        mobmove = True
        if fakeSCORE >= 5:
            if skip == True:
                skip = False
                frame = FRAME
            if skip == False:
                if FRAME - frame == 15:
                    fakeSCORE = 0
                    skip = True
                    for i in range(5):
                        if mobmove == True:
                            newMob = Mob(randint(0,WIDTH), randint(100, HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), True)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.append(newMob)
                            mobmove = False
                        else:
                            newMob = Mob(randint(0,WIDTH), randint(100, HEIGHT - 100), 40, 40, (colorbyte(),colorbyte(),colorbyte()), False)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.insert(0, newMob)
                            mobmove = True

    # checks if the window is open or close and stops the thing if closed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        # Checks if something is pressed and what it is
        if event.type == pg.KEYDOWN:

            # When space is pressed then jump()
            if event.key == pg.K_SPACE:
                player.jump()

    if HEALTH <= 0:
        player.kill()
        screen.fill(BLACK)
        draw_text("U suck lol", 300, WHITE, WIDTH / 2, HEIGHT / 3)
    else:
        # update all sprites
        all_sprites.update()

        # draw the background screen
        screen.fill(BLACK)
            # draw all sprites
        all_sprites.draw(screen)
        # draw text
        draw_text("Get to 30 points to win!", 20, BLACK, WIDTH / 2, HEIGHT - 110)
        draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
        draw_text("HEALTH: " + str(HEALTH), 22, WHITE, WIDTH - (WIDTH / 3), HEIGHT / 24)
        draw_text("FRAME: " + str(FRAME), 22, WHITE, WIDTH / 3, HEIGHT / 24)
                    # If score equals 30 then end game
        if SCORE >= 30:
            player.kill()
            screen.fill(BLACK)
            draw_text("U WIN", 100, WHITE, WIDTH / 2, HEIGHT / 3)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()