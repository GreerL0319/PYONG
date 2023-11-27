import pygame #pip install pygame in shell
#PYGAME DOES NOT WORK IN ONLINE GDB BECAUSE IT HAS TO MAKE AN EXTERNAL WINDOW FOR THE GAME SCREEN!!!!
#YOU HAVE TO RUN THIS FILE
#  ON YOUR COMPUTER
import sys
import math
import random
import time
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
BLUE=(0,0,255)#rgb code for the color blue
RED=(255,0,0)#red
WHITE=(255,255,255)#white
MAGENTA=(255,0,255)#purple
font = pygame.font.Font('freesansbold.ttf', 32)



class Sprite():
    def __init__(self,xpos,color):
        self.xpos=xpos
        self.ypos=DEFAULTY
        self.color=color
      
    def Blit(self,width,height):
        self.sprite=pygame.Rect(self.xpos,self.ypos,width,height)
        pygame.draw.rect(screen,self.color,self.sprite)
        

class Players(Sprite):
    def __init__(self,xpos,color):
        super().__init__(xpos,color)
        self.largepaddle=False
        self.doublepaddle=False
        self.slowed=False
        self.shrunk=False

    def checkIsPowered(self):
        if self.largepaddle:
            self.Blit(20,200)
        if self.shrunk:
            self.Blit(20,50)
        if self.doublepaddle:
            self.Blit(20,100)
            if self.xpos<size.current_w/2:
                self.xpos+=400#left
            if self.xpos>size.current_w/2:
                self.xpos-=400#p2 is on the right so 200 pixels added would be offscreen
            self.Blit(20,100)#blits a second paddle 50 pixels ahead
            #reset xpos
            if self.xpos<size.current_w/2:
                self.xpos-=400#left
            if self.xpos>size.current_w/2:
                self.xpos+=400#p2 is on the right so 200 pixels added would be offscreen

    def moveUp(self):
        if self.slowed:
            self.ypos-=1
        else:
            self.ypos-=10
        if self.ypos<0:#confines players to the screen
            self.ypos=self.ypos=size.current_h-5
        self.checkIsPowered()

    def moveDown(self):
        if self.slowed:
            self.ypos+=1
        else:
            self.ypos+=10
        self.checkIsPowered()
        if self.ypos>size.current_h:  
            self.ypos=0+5 #5pixels up   from the bottom of the screen   
    


class Ball(Sprite):
    def __init__(self,xpos,color):
        super().__init__(xpos,color)
        self.sizeup=False
        self.speedup=False
        self.lasthitter=0
        self.slowed=False
        self.beat=False
        self.dr=10
        random.seed(time.time())
        self.angle=360*random.random()
        print(self.angle)
        while self.angle<180+25 and self.angle>180-25:
            self.angle=360*random.random() #avoids the ball from just aiming at the roof and bouncing
        while self.angle<0+25 and self.angle>360-25:
            self.angle=360*random.random() #avoids the ball from just aiming at the roof and bouncing

        if self.angle<=180:
            self.dx=self.dr*math.cos(self.angle)
            self.dy=self.dr*math.sin(self.angle)
        elif self.angle>180:
            self.dy=self.dr*math.cos(self.angle)
            self.dx=self.dr*math.sin(self.angle)
        
    def ballMovement(self,p1,p2,item):
        self.beat=False
        if self.ypos<0 or self.ypos>size.current_h:#if it hits the wall
            self.dy=-self.dy
            if self.ypos<0:
                self.dy+=.1
            else:
                self.dy-=.1
        itemcollide=pygame.Rect.colliderect(item.sprite,self.sprite)
        p1collide = pygame.Rect.colliderect(p1.sprite,self.sprite)
        p2collide = pygame.Rect.colliderect(p2.sprite,self.sprite)
        if p1collide:
            if self.lasthitter!=1:#this will prevent the sprite from intereacting with the ball several times and causing a loss for the hitter
                self.dx=-self.dx 
                self.dx+=2
                self.lasthitter=1
                if self.beat:
                    self.dx+=2 #if th eplayer times this keypress with the collision then the ball goes even fasters
        if p2collide:
            if self.lasthitter!=2   :#this will prevent the sprite from intereacting with the ball several times and causing a loss for the hitter
                self.dx=-self.dx
                self.dx-=2
                self.lasthitter=2
                if self.beat:
                    self.dx-=2
        if self.beat:#i did not finish adding this mechanic
            self.color=MAGENTA
        if itemcollide:
            if item.obtained==False:
                if self.lasthitter==1:
                    item.getPower(p1,self,p2)
                elif self.lasthitter==2:
                    item.getPower(p2,self,p1)
                itemcollide=False
                self.lasthitter=0
        if self.xpos<0:
            return 2 #player 2 won
        if self.xpos>size.current_w:
            return 1 #player 1 won
        if self.speedup:
            if self.dx<0:
                self.dx=-30
            if self.dx>0:
                self.dx=30
            if self.dy<0:
                self.dy=-30# makes sure it continues in the direction it was heading
            if self.dy>0:
                self.dy=30
        self.xpos+=self.dx #add the new distance to the positions
        self.ypos+=self.dy
        if self.sizeup:
            self.Blit(60,60)
        else:
            self.Blit(20,20)
        return 0


class PowerUp(Sprite):
    def __init__(self,color):
        super().__init__(0,color)
        self.obtained=False
        self.sprite=pygame.Rect(self.xpos,self.ypos,0,0)#initialize
        self.width=P2POS-P1POS-20
        self.xpos=self.width*random.random()+P1POS
        self.ypos=size.current_h*random.random()+10
        self.status=""

    def getPower(self,player,ball,victim):
        self.color=(0,0,0)#blits black at the pixel location to remove it
        self.Blit(40,40)
        self.obtained=True
        self.color=MAGENTA #change stored color back to magenta
        self.power=random.randint(0,5)
        if self.power==0:
            player.largepaddle=True
            self.status="LARGE PADDLE"
        elif self.power==1:
            player.doublepaddle=True
            self.status="DOUBLE PADDLE"
        elif self.power==2:
            victim.slowed=True
            self.status="ZA WARUDO"
        elif self.power==3:
            ball.sizeup=True 
            self.status="BIG OLE BALL"
        elif self.power==4: 
            ball.speedup=True
            self.status="GOODBYE"
        elif self.power==5:
            victim.shrunk=True
            self.status="SHRUNK"



def screenprint(string,x,y,color=WHITE):
    text=font.render(string,True,color)
    rect=text.get_rect()
    rect.topleft=(x,y)
    screen.blit(text,rect)
    return (text,rect)

def startup():
    screen.fill((0, 0, 0))  # fills the screen with black to reset the sprites
    screenprint("WECOME TO PYONG",size.current_w/2,200)
    screenprint("PONG WITH A TWIST",size.current_w/2,300)
    screenprint("PRESS SPACE TO CONTINUE",size.current_w/2,700)
    screenprint("PLAYER 1:",100,100)
    screenprint("UP=W",100,200)
    screenprint("DOWN=S",100,300)
    screenprint("PLAYER 2:",100,500)
    screenprint("UP=UP_ARROW",100,600)
    screenprint("DOWN=DOWN_ARROW",100,700)

    pygame.display.flip() #update the screen
    notspace=True
    while notspace:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                notspace= False
            pygame.time.delay(50)  # add a small delay to reduce CPU usage


def gameover(winner):
    screen.fill((0,0,0))
    screenprint("GAMEOVER",size.current_w/2,100)
    screenprint("PLAYER "+str(winner)+" WON!",size.current_w/2,200)
    screenprint("PRESS SPACE TO PLAY AGAIN",100,700)
    pygame.display.flip()
    notspace=True
    while notspace:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                notspace=False
                main()
            elif event.type==pygame.QUIT or event.type==pygame.KEYDOWN:#if any button is pressed other than space
                pygame.quit()
                sys.exit()
def main():
    score=[0,0]
    won=0
    while score[0]<10 and score[1]<10:
        if won==1:
                score[0]+=1
                if score[0]>=10:
                    break
        if won==2:
                score[1]+=1
                if score[1]>=10:
                    break
        won=0
        scorerect=(text,rect)=screenprint("P1: "+str(score[0])+"          P2: "+str(score[1]),size.current_w/2,200)
        p1=Players(P1POS,BLUE)
        p2=Players(P2POS,RED)
        ball=Ball(BPOS,WHITE)
        item=PowerUp(MAGENTA)
        while True:
            screen.fill((0, 0, 0))  # fills the screen with black to reset the sprites
            screen.blit(scorerect[0],scorerect[1])
            screenprint(item.status,size.current_w/2,size.current_h/2,MAGENTA)
            p1.Blit(20,100)
            p1.checkIsPowered()
            p2.Blit(20,100)
            p2.checkIsPowered()
            if ball.sizeup==True:
                ball.Blit(60,60)
            else:
                ball.Blit(20,20)
            if not item.obtained:
                item.Blit(40,40)
            keys = pygame.key.get_pressed()  # Get the state of all keys
            
            # Update movement variables based key presses
            if keys[K_d]: #tapping when the ball hits will spike the ball
                p1.beat=True
            if keys[K_LEFT]:
                p2.beat=True
            if keys[K_w]:
                p1.moveUp()
            if keys[K_s]:
                p1.moveDown()
            if keys[K_UP]:
                p2.moveUp()
            if keys[K_DOWN]:
                p2.moveDown()
           
            won=ball.ballMovement(p1,p2,item)
            if won:
                time.sleep(.5)
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # updates the screen
            clock.tick(60)  # 60 fps
    gameover(won)

if __name__=="__main__":
    startup()
    main()
