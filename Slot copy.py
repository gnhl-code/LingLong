
import pygame
import random
import time
pygame.init()


"""
CREATE NUMBERS IN SLOT, REFERENCE CO PILOT,
ADD KANJI LETTERS JACKPOT WITH IF CONDITION, 
ADD MUSIC AND REFIN
"""


height = 800
width = 800
gray = (128,128,128)
red = (250,71,74)
white = (255,255,255)
gold = (249,165,4)
clock = pygame.time.Clock()
running = True

screen = pygame.display.set_mode((height,width))


rainbow_colors = [
    pygame.Color("red"),
    pygame.Color("orange"),
    pygame.Color("yellow"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("indigo"),
    pygame.Color("violet"),
]


class spin():
    def __init__(self,x,y,h,w, slot):
        self.rect = pygame.Rect(x,y,h,w)
        self.clicked = False
        self.spinning = False
        self.slot = slot
    
    def draw(self,surf,col,text,font,tc):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.slot.spun(screen)
                #self.slot[1].spun(slot.rect)
                #self.slot[2].spun(slot.rect)
                print("click")
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        pygame.draw.rect(surf,col,self.rect)
        text_surf = font.render(text,True,tc)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

class slot():
    def __init__(self, x,y,h,w):
        self.rect = pygame.Rect(x,y,h,w)
        self.num = [1,2,3,4,5,6,7,8,9,10]
        self.stat = True
        self.duration = 5 
        self.stime = time.time()
        self.lupdate = 0 
        self.current = ""
        self.color_index = 0
        self.animation_speed = 0.1
        self.stat = False       

    def draw(self,surf,col):
        pygame.draw.rect(surf,col,self.rect)
        #text_surf = font.render(str(self.num),True,tc)
        #text_rect = text_surf.get_rect(center=self.rect.center)
        #surf.blit(text_surf, text_rect)
    def spun(self,surf):
        ctime = time.time()
        etime = ctime - self.stime
        self.color = rainbow_colors[self.color_index]
        if etime >= self.duration:
            self.stat = True
        if self.stat == False:
                if ctime - self.lupdate >0.5:
                    self.current = random.choice(str(self.num))
                    self.lupdate = ctime
                text_surf = font.render(self.current,True, self.color)
                text_rect = text_surf.get_rect(center=self.rect.center)
                surf.blit(text_surf, text_rect)
            #self.color_index = (self.color_index + 1) % len(rainbow_colors)
            #time.sleep(self.animation_speed)

font = pygame.font.Font(None, 36)

slot1 = slot(100,200,150,300)
slot2 = slot(300,200,150,300)
slot3 = slot(500,200,150,300)
spin1 = spin(300,550,150,50, slot1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    spin1.draw(screen,red,"SPIN",font,white)
    slot1.draw(screen,gray)
    slot2.draw(screen,gray)
    slot3.draw(screen,gray)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()