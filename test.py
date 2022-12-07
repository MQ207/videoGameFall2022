import pygame

pygame.init()
width = 1200
height = 600
window = pygame.display.set_mode((width,height))
bg_img = pygame.image.load('c:/github/IntroToProgramming/videoGameFall2022/Game/images/StarterScreen.jpg')
bg_img = pygame.transform.scale(bg_img,(width,height))
 

i = 0
 
runing = True
while runing:
    window.fill((0,0,0))
    window.blit(bg_img,(i,0))
    window.blit(bg_img,(width+i,0))
    if (i==-width):
        window.blit(bg_img,(width+i,0))
        i=0
    i-=.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    pygame.display.update()
pygame.quit()