import pygame
import sys
import math
import random
from time import time
from pygame.locals import * #imports the key mappings ie K_UP

pygame.init()
pygame.display.set_caption("PYONG")
size=pygame.display.Info()#returns the size of the current display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock=pygame.time.Clock()
P1POS=100 #x coords will be static for players
P2POS=size.current_w -100 #will need configuration
BPOS=size.current_w/2#starting position for the ball
DEFAULTY=size.current_h/2
P1COLOR=(0,0,255)#rgb code for the color blue
P2COLOR=(255,0,0)#red
BCOLOR=(255,255,255)#white
font = pygame.font.Font('freesansbold.ttf', 32)



class Sprite():
    def __init__(self,xpos,color):
        self.xpos=xpos
        self.ypos=DEFAULTY
        self.color=color

    def getYPos(self):
        return self.ypos
    def getXPos(self):
        return self.xpos
        

class Players(Sprite):
    def __init__(self,xpos,color):
        super().__init__(xpos,color)

    def pBlit(self):
        if self.ypos>size.current_h:#helps stay in screen confinements and allows cool mechanic where player jumps to the other side of the screen
            self.ypos=0
        if self.ypos<0:
            self.ypos=size.current_h
        self.psprite=pygame.Rect(self.xpos,self.ypos,20,100)
        pygame.draw.rect(screen,self.color,self.psprite)

    def moveUp(self):
        self.ypos-=10
        self.pBlit()

    def moveDown(self):
        self.ypos+=10
        self.pBlit()
    
class Ball(Sprite):
    def __init__(self,xpos,color):
        super().__init__(xpos,color)
        self.dr=15
        random.seed(time())
        self.angle=360*random.random()
        if self.angle<=180:
            self.dx=self.dr*math.cos(self.angle)
            self.dy=self.dr*math.sin(self.angle)
        elif self.angle>180:
            self.dy=self.dr*math.cos(self.angle)
            self.dx=self.dr*math.sin(self.angle)
        
    def bBlit(self):
        self.bsprite=pygame.Rect(self.xpos,self.ypos,20,20)
        pygame.draw.rect(screen,self.color,self.bsprite)        
        
    def ballMovement(self,p1,p2):
        if self.ypos<0 or self.ypos>size.current_h:#if it hits the wall
            self.dy=-self.dy

        p1collide = pygame.Rect.colliderect(p1.psprite,self.bsprite)
        p2collide = pygame.Rect.colliderect(p2.psprite,self.bsprite)
        if p2collide or p1collide:
            self.dx=-self.dx
            self.dx+=1 #increase the speed every time its hit
            self.dy+=1
        if self.xpos<0:
            return 2 #player 2 won
        if self.xpos>size.current_w:
            return 1 #player 1 won
        self.xpos+=self.dx
        self.ypos+=self.dy
        self.bBlit()
        return 0

def main():
    score=[0,0]
    while score[0]<10 or score[1]<10:
        p1score=str(score[0])
        p2score=str(score[1])
        strscore="P1: "+p1score+"          P2: "+p2score
        text = font.render(strscore, True, BCOLOR)
        rect=text.get_rect()
        rect.center=(size.current_w/2,200)
        p1=Players(P1POS,P1COLOR)
        p2=Players(P2POS,P2COLOR)
        ball=Ball(BPOS,BCOLOR)
        while True:
            screen.fill((0, 0, 0))  # fills the screen with black to reset the sprites
            screen.blit(text,rect)
            p1.pBlit()
            p2.pBlit()
            ball.bBlit()

            keys = pygame.key.get_pressed()  # Get the state of all keys
            
            # Update movement variables based key presses
            if keys[K_w]:
                p1.moveUp()
            if keys[K_s]:
                p1.moveDown()
            if keys[K_UP]:
                p2.moveUp()
            if keys[K_DOWN]:
                p2.moveDown()
            won=ball.ballMovement(p1,p2)
            if won==1:
                score[0]+=1
                break
            if won==2:
                score[1]+=1
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # updates the screen
            clock.tick(60)  # 60 fps

if __name__=="__main__":
    main()
