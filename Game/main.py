# content from kids can code: http://kidscancode.org/blog/
# append into list https://www.digitalocean.com/community/tutorials/python-add-to-list
# min() https://www.geeksforgeeks.org/python-program-to-find-smallest-number-in-a-list/
# abs() https://www.toppr.com/guides/python-guide/questions/change-positive-negative-python/
# Thank you to Tyson for being a stress ball
# Move according to angle https://stackoverflow.com/questions/46697502/how-to-move-a-sprite-according-to-an-angle-in-pygame/68698440#68698440

'''
Things to Fix:
- Boundries

future plans:
Health Bar
Ammo
Melee
Power-up class
Mob moving randomly and shooting randomly
Spirites
Levels
Bombs
Soul Knight?
Mini Map?
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
from levels import *
from math import *

# Random vars and lists for later use. I should rlly organize this
vec = pg.math.Vector2
shootClock = 0
canShot = True
shootermobs = []

# Background sprites
starterscreen = pg.image.load(r'c:/github/IntroToProgramming/videoGameFall2022/Game/images/StarterScreen.jpg')
insideCastle = pg.image.load(r'c:/github/IntroToProgramming/videoGameFall2022/Game/images/InsideCastle.jpg')

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
# Player class with no parameters because there is only one player unless I wanna do a choose you class thing but thats for later
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # The player sprite
        self.image = pg.image.load(r'c:/github/IntroToProgramming/videoGameFall2022/Game/images/DK T-posing.png').convert_alpha()
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        # Timers for timing things
        self.timer = 0
        self.timer2 = 0
        self.walls = True
        self.face = "right"

    # Controls that when a key is pressed it will check to see what key then depending on the key will move in a direction
    def controls(self):
        global canShot, noHit, superstar
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -10
        if keys[pg.K_d]:
            self.acc.x = 10
        if keys[pg.K_s]:
            self.acc.y = 10
        if keys[pg.K_w]:
            self.acc.y = -10
        if keys[pg.K_c]:
            # When c is pressed then the plyer will call apon/instantiate a bullet thats a little different from the mob bullets
            def throwBullet():
                bullet = Bullet(20, 20, BLUE, "player", self)
                all_sprites.add(bullet)
                all_bullets.add(bullet)
                allBull.append(bullet)
                bullet.fly()
            
            # One of the timers in my player class that takes a global var that gets updated inside the game loop to count the frames
            if canShot == True and len(m) > 0:
                throwBullet()
                canShot = False

        if keys[pg.K_f]:
            # If F is pressed then spawn a wall but don't spawn a wall if the timer is not over
            if self.walls == True:
                wall1 = Platform(self.rect.center[0] + 100, self.rect.top, 50, 100, True)
                all_plats.add(wall1)
                allplats.append(wall1)
                all_sprites.add(wall1)
                self.walls = False

        if keys[pg.K_e]:
            # If you have a super star and you press e then u become invincible
            if superstar > 0 and noHit == False:
                noHit = True
                superstar -= 1
            
    # Update so whenever a frame is going on this runs and constantly updates the class so things like gravity can exist
    def update(self):
        global noHit
        # Gravity that I turned off but am to lazy to delete
        self.acc = vec(0,GRAVITY)
        self.controls()
        self.acc.x += self.vel.x * -0.5
        self.acc.y += self.vel.y * -0.5
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.vel.x < 0 and self.face == "right":
            self.image = pg.transform.flip(self.image, True, False)
            self.face = "left"
        elif self.vel.x > 0 and self.face == "left":
            self.image = pg.transform.flip(self.image, True, False)
            self.face = "right"
        
        # The timer for the walls where if the walls have been placed then add 1 to the timer until the timer has counted 200 frames
        if self.walls == False:
            self.timer2 += 1
            if self.timer2 >= 200:
                self.walls = True
                self.timer2 = 0

        # Same timer as the walls just this one makes the player rainbow and returns the player to its normal sprite afterwards
        if noHit == True:
            self.timer += 1
            self.image.fill((colorbyte(), colorbyte(), colorbyte()))
            if self.timer >= 60:
                noHit = False
                self.timer = 0 
                self.image = pg.image.load(r'c:/github/IntroToProgramming/videoGameFall2022/Game/images/DK T-posing.png').convert_alpha()

# platforms class that have xy cords, if they are a player wall and size
class Platform(Sprite):
    def __init__(self, x, y, w, h, player):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.timer = 0

    def update(self):
        # If this wall has been spawned by a player then it will stay up for 2 seconds before disappering
        if self.player == True:
            self.timer += 1
            if self.timer >= 60:
                self.kill()
                all_plats.remove(self)
                allplats.remove(self)
                self.timer = 0 


# Mob class that have xy cords, size, color, and if is a mover or a shooter
class Mob(Sprite):
    def __init__(self, x, y, w, h, color, move):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.move = move
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.mobframe = 0
        self.mobskip = True
        self.vec = pg.math.Vector2()
        # If the move is not a mover then it is put into the shootermob list
        if move == False:
            shootermobs.append(self)
    
    def shot(self):
        # When a shooter shoots then it will shoot a bullet!!!
        if self.move == False:
            bullet = Bullet(20, 20, RED, "mob", self)
            all_sprites.add(bullet)
            all_bullets.add(bullet)
            allBull.append(bullet)
            bullet.fly()

    def mover(self):
        # Movers always move towards the player
        rise = (player.rect.center[1] - self.rect.center[1])/20
        run = (player.rect.center[0] - self.rect.center[0])/20
        self.vel.x = run
        self.vel.y = rise


        degree = floor(degrees(atan(rise/run)))
        return degree
        # if ((player.rect.center[0] - (self.rect.center[0]))/20) > 20:
        #     self.vel.x = (player.rect.center[0] - (self.rect.center[0]))/20
        # else:
        #     self.vel.x = (player.rect.center[0] - (self.rect.center[0]))/20

        # if ((player.rect.center[1] - (self.rect.center[1]))/20) > 20:
        #     self.vel.y = ((player.rect.center[1] - (self.rect.center[1]))/20)
        # else:
        #     self.vel.y = (player.rect.center[1] - (self.rect.center[1]))/20
        # print(self.vel.x)

            

# Like the player, mob also has a update method so the gravity can be a thing
    def update(self):
        self.acc = vec(0,GRAVITY)
        self.acc.x += self.vel.x * -0.1
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if len(m) > 0:
            if self.move == True:
                if self.mobskip == True:
                    self.mobskip = False
                    self.mobframe = FRAME
                if self.mobskip == False:
                    if FRAME - self.mobframe >= 1:
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
        global HEALTH, SCORE, fakeSCORE, noHit
        if mobhits and noHit == False:
            self.kill()
            m.remove(self)
            if self.move == False:
                shootermobs.remove(self)
            HEALTH -= 1
            fakeSCORE += 1
            if SCORE >= 5:
                SCORE -= 5
            if SCORE < 5:
                SCORE = 0

# Bullet calls that has the same property as everything else
class Bullet(Sprite):
    def __init__(self, w, h, color, who, whatmob):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h),  pg.SRCALPHA)
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
                SCORE += 3
                fakeSCORE += 1

        # for i in range(len(m)):
        if self.who == "mob":
            # for o in range(len(allBull)):
            bullethitsplayer = pg.sprite.spritecollide(self, player0, False)
            global noHit
            if bullethitsplayer and noHit == False:
                HEALTH -= 5
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
            self.vel.x = (playerX - (self.whatmob.rect.center[0]))/20
            self.vel.y = (playerY - (self.whatmob.rect.center[1]))/20
            rise = self.vel.y
            run = self.vel.x
            # self.image = pg.transform.rotate(self.image, floor(degrees(atan(rise/run))))

    
            # If the bullet came from a player
        if self.who == "player":  
            for mob in m: 
            # Grabs the xy distance from the player to the mob then adds them so see what mob is closest
                global mobClosest
                mobX = abs(playerX - (mob.rect.center[0]))
                mobY = abs(playerY - (mob.rect.center[1]))
                bulletXY.append(playerX - (mob.rect.center[0]))
                bulletXY.append(playerY - (mob.rect.center[1]) - 10)
                mob = mobY + mobX
                mobDistance.append(mob)
                mobClosest = min(mobDistance)
            
            for i in range(len(m)):
                if mobClosest == mobDistance[i]:
                    self.vel.x = (bulletXY[(2 * i)]) * -.1
                    self.vel.y = (bulletXY[((2 * i) + 1)]) * -.1
                
class PowerUp(Sprite):
    def __init__(self, what, x, y):
        Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        if what == 'noDamage':
            self.image.fill(BLUE)
        if what == 'health':
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.what = what
        self.pos = x, y
        self.timer = 0
        self.running = False

    def powerup(self):
        global superstar, HEALTH
        if self.what == 'noDamage':
            superstar += 1
        if self.what == 'health':
            HEALTH = HEALTH + 10

    def update(self):
        global superstar
        self.rect.midbottom = self.pos
        hits = pg.sprite.spritecollide(self, player0, False)
        if hits:
            self.powerup()
            self.kill()

class HealthBar(Sprite):
    def __init__(self, W, H, x, y):
        Sprite.__init__(self)
        self.image = pg.Surface((W, H))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.W = W
        self.H = H
        self.pos = x, y
    
    def update(self):
        self.rect.midbottom = self.pos
        player_health = (HEALTH/100)* self.W
        self.image = pg.Surface((player_health, self.H))
        self.image.fill(RED)


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
powerups = pg.sprite.Group()

allplats = []
mobshooters = []
allBull = []
m = []

# instantiate classes
player = Player()

powerup = PowerUp('noDamage', 2*(WIDTH/3), HEIGHT/2)
powerups.add(powerup)
all_sprites.add(powerup)
player_healthbar = HealthBar(600, 30, WIDTH/2, (HEIGHT/50) * 49)
platform = Platform(WIDTH/3.425, (HEIGHT/18) * 17, 600, 38, False)
all_sprites.add(platform)
all_sprites.add(player_healthbar)

def firstlevel():
    m1 = Mob(WIDTH - 300, HEIGHT/3, 40, 40, GREEN, True)
    m2 = Mob(randint(WIDTH/2,WIDTH - 300), randint(330,HEIGHT - 230), 40, 40, WHITE, False)
    m3 = Mob(WIDTH - 300, randint(330,HEIGHT - 230), 40, 40, GREEN, True)
    # List of mobs but the form of the names of the mobs can't be changed so it can not be used to identify certain mobs
    m.append(m1)
    m.append(m2)
    m.append(m3)
    all_sprites.add(m)
    mobs.add(m)

def secondlevel():
    global fakeSCORE
    fakeSCORE = fakeSCORE + 2
    healthpack1 = PowerUp('health',  2*(WIDTH/3), HEIGHT/2)
    powerups.add(healthpack1)
    all_sprites.add(healthpack1)

def thirdlevel():
    superstar1 = PowerUp('noDamage',  2*(WIDTH/3), HEIGHT/2)
    powerups.add(superstar1)
    all_sprites.add(superstar1)


# Adds all bullets put in the allBulls list into sprite groups
all_sprites.add(allBull)
all_bullets.add(allBull)


# add player to all sprites groupad
all_sprites.add(player)
player0.add(player)

# add platform to all sprites group and all platforms groups
# all_sprites.add(plat)
# all_plats.add(plat)
# allplats.append(plat)

# Game loop
running = True
while running:

    # keeps the loop running using clock
    clock.tick(FPS)

    FRAME += 1

    if levelcounter == 1 and level1 == False:
        firstlevel()
        level1 = True
        
    
    if SCORE >= 10 and fakeSCORE == 3 and levelcounter == 2 and level2 == False:
        level2 = True
        secondlevel()

    if SCORE >= 20 and fakeSCORE == 5 and levelcounter == 3 and level3 == False:
        level3 = True
        thirdlevel()

    # For every mob in mob list, check if they collide with a platform and if teleport to the top and set y velocity to 0
    # for i in range(len(m)):
    #     hits = pg.sprite.spritecollide(m[i], all_plats, False)
    #     if hits:
    #         m[i].pos.y =  hits[0].rect.top
    #         m[i].vel.y = 0

    if player.pos.y <= 310:
            player.pos.y = 311
    if player.pos.y >= HEIGHT - 210 :
        player.pos.y = HEIGHT - 220
    
    if len(mobs) != len(m):
        fakeSCORE += 1
        SCORE += 3
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
        if len(m) == 0:
            levelcounter -= 1
    elif player.pos.x > WIDTH:
        player.pos.x = 0
        if len(m) == 0:
            levelcounter += 1
    
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
                            newMob = Mob(randint(WIDTH/2,WIDTH - 300), randint(330,HEIGHT - 230), 40, 40, GREEN, True)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.append(newMob)
                            mobmove = False
                        else:
                            newMob = Mob(randint(WIDTH/2,WIDTH - 300), randint(330, HEIGHT - 230), 40, 40, BLACK, False)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.insert(0, newMob)
                            mobmove = True

    if SCORE >= 10 and SCORE <= 30:
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
                            newMob = Mob(randint(0,WIDTH), randint(330, HEIGHT - 100), 40, 40, GREEN, True)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.append(newMob)
                            mobmove = False
                        else:
                            newMob = Mob(randint(0,WIDTH), randint(330, HEIGHT - 100), 40, 40, BLACK, False)
                            all_sprites.add(newMob)
                            mobs.add(newMob)
                            m.insert(0, newMob)
                            mobmove = True

    # checks if the window is open or close and stops the thing if closed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if HEALTH <= 0:
        player.kill()
        screen.fill(BLACK)
        draw_text("U suck lol", 300, WHITE, WIDTH / 2, HEIGHT / 3)
    else:
        # update all sprites
        all_sprites.update()
        powerups.update()

        # draw the background screen
        screen.fill((0,0,0))
        if levelcounter <= 2 and level1 == True or level2 == True:
            screen.blit(starterscreen, (0, 0))
        if levelcounter >= 3 and level3 == True:
            screen.blit(insideCastle, (0, 0))

        # draw all sprites
        all_sprites.draw(screen)

        # draw text
        draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 75)
        draw_text("HEALTH: " + str(HEALTH), 22, WHITE, WIDTH - (WIDTH / 3), HEIGHT / 75)
        draw_text("FRAME: " + str(FRAME), 22, WHITE, WIDTH / 3, HEIGHT / 75)
        draw_text("SUPERSTAR: " + str(superstar), 22, WHITE, WIDTH / 6, HEIGHT / 75)
        if levelcounter <= 0:
            draw_text("How to play! WASD to move, C to shoot, F for walls, E to use your superstar. Don't die and keep progressing into the castle! (There is only 2 real levels if u can call them levels...)", 22, WHITE, WIDTH / 2, HEIGHT / 5)
                    # If score equals 30 then end game
        # if SCORE >= 30:
        #     player.kill()
        #     screen.fill(BLACK)
        #     draw_text("U WIN", 100, WHITE, WIDTH / 2, HEIGHT / 3)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()