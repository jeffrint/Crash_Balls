import pygame, math, random, time
from pygame.locals import *
from random import randint


CLOCKWISE = 'clockwise'
ANTICLOCKWISE = 'anticlockwise'
FORWARD = 'forward'

class Game:

    def __init__(self,game_width,game_height):
        pygame.display.set_caption('Crash Balls')
        pygame.mouse.set_visible(0)
        self.game_width = game_width
        self.game_height = game_height
        self.game_display = pygame.display.set_mode((self.game_width,self.game_height+60))
        self.quit = False
        self.black = (255,255,255)  
        self.intro = True
        self.crash = False
        self.game_display.fill(self.black)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.fps = 75
        self.speed = 6
        self.spawn_count = 150
        self.sound = pygame.mixer.music.load('noise.mp3')
        self.difficulty = 'normal'
        self.explosion = pygame.image.load('crash.png')
        self.background = pygame.image.load('background.png')
        pygame.display.update()



class Player:

    def __init__(self,game):
        self.image = pygame.image.load('player_1.png')
        self.x = game.game_width/2
        self.y = game.game_height/2
        self.angle = 6
        self.direction = None
        self.motion = False
        self.rect_coord = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)
        game.game_display.blit(self.image,(self.x,self.y))

    def rotate_player(self,game):
        
        if self.direction==ANTICLOCKWISE:
            self.angle+=5
        if self.direction==CLOCKWISE:
            self.angle-=5
        if self.motion:
            self.move_player(game)
        new_image = pygame.transform.rotate(self.image,self.angle)
        new_image_center = new_image.get_rect().center
        new_center = (self.rect_coord.center[0]-new_image_center[0],self.rect_coord.center[1]-new_image_center[1])
        game.game_display.blit(new_image,new_center)
        #game.game_display.blit(new_image,(self.x,self.y))

    def move_player(self,game):
        y = math.cos(math.radians(self.angle))*game.speed
        x = math.sin(math.radians(self.angle))*game.speed
        self.rect_coord.top -= round(y)
        self.rect_coord.left -= round(x)



class Balls:
    def __init__(self,game):
        self.speed = 6
        
    def moving_balls(self,game):
        if self.angle>360:
            self.angle= self.angle%360
        if self.angle<0:
            self.angle=360-self.angle%360
        if self.rect.top <=0:
            if 0 < self.angle < 90:
                self.angle = self.angle+90
            elif 270 < self.angle < 360:
                self.angle = self.angle-90
            elif self.angle==0:
                self.angle=180
        if self.rect.bottom >=game.game_height:
            if 90< self.angle<180:
                self.angle=self.angle-90
            elif 180<self.angle<270:
                self.angle=self.angle+90
            elif self.angle==180:
                self.angle=0
        if self.rect.left <=0:
            if 90 < self.angle < 180:
                self.angle+=90
            elif 0 < self.angle < 90:
                self.angle-=90
            elif self.angle==90:
                self.angle=270
        if self.rect.right>=game.game_width:
            if 270 < self.angle < 360:
                self.angle+=90
            elif 180 < self.angle < 270:
                self.angle-=90
            elif self.angle==270:
                self.angle=90
      
        y = math.cos(math.radians(self.angle))*self.speed
        x = math.sin(math.radians(self.angle))*self.speed
        self.rect.top -= round(y)
        self.rect.left -= round(x)
        game.game_display.blit(self.image,(self.rect.left,self.rect.top))

class redBall(Balls):
    def __init__(self,game):
        self.image = pygame.image.load('red_ball.png')
        self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        self.angle = randint(0,360)
        self.x = randint(0,game.game_width-21)
        self.y = randint(0,game.game_height-21)
        self.speed = 3
    def moving_balls(self,game):
        super().moving_balls(game)

class blueBall(Balls):
    def __init__(self,game):
        self.image = pygame.image.load('blue_ball.png')
        self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        self.angle = randint(0,360)
        self.x = randint(0,game.game_width-21)
        self.y = randint(0,game.game_height-21)
        self.speed = 3
    def moving_balls(self,game):
        super().moving_balls(game)

class greenBall(Balls):
    def __init__(self,game):
        self.image = pygame.image.load('green_ball.png')
        self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        self.angle = randint(0,360)
        self.x = randint(0,game.game_width-21)
        self.y = randint(0,game.game_height-21)
        self.speed = 3
    def moving_balls(self,game):
        super().moving_balls(game)


 
        
def display_score(game):
    myfont = pygame.font.SysFont('Segoe UI',20)
    myfont_bold = pygame.font.SysFont('Segoe UI',20,True)
    text_score = myfont.render('SCORE: ',True,(0,0,0))
    text_score_number = myfont.render(str(int(game.score/game.spawn_count)),True,(0,0,0))
    text_highest = myfont.render('HIGHEST SCORE: ', True,(0,0,0))
    text_highest_number = myfont_bold.render('0',True,(0,0,0))
    game.game_display.blit(text_score, (145, 620))
    game.game_display.blit(text_score_number, (220, 620))
    game.game_display.blit(text_highest, (300, 620))
    game.game_display.blit(text_highest_number, (470, 620))


def check_collision(player,balls):
    for ball in balls:
        if player.rect_coord.colliderect(ball.rect):
            return True
    return False
            
def player_crashed(player,game):
    if player.rect_coord.bottom<0 or player.rect_coord.top>game.game_height or player.rect_coord.right<0 or player.rect_coord.left>game.game_width:
        return True
    else:
        return False


pygame.init()
pygame.display.init()
pygame.font.init()


quit = False
while quit==False:
    game = Game(800,600)

    while game.intro==True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit = True
                    game.intro = False
                    game.crash = True
                
                if event.key == K_SPACE:
                    game.intro=False
                
                if event.key==K_DOWN and game.difficulty!="Easy":
                    if game.difficulty=='Hard':
                        game.difficulty='Normal'
                    else:
                        game.difficulty='Easy'

                if event.key==K_UP and game.difficulty!='Hard':
                    if game.difficulty=='Easy':
                        game.difficulty='Normal'
                    else:
                        game.difficulty='Hard'

        if game.difficulty=='Easy':
            game.spawn_count=250

        if game.difficulty=='Normal':
            game.spawn_count=150

        if game.difficulty=='Hard':
            game.spawn_count=50 

        game.game_display.blit(game.background,(0,0))
        text_title = pygame.font.SysFont('Segoe UI',179)
        text_subt = pygame.font.SysFont('Segoe UI',75)
        text_subt2 = pygame.font.SysFont('Segoe UI',25)
        title = text_title.render('Crash Balls',True,(0,0,0),(100,150,255))
        subt1 = text_subt.render('Press "Space" to start',True,(0,0,0))
        subt2 = text_subt2.render('Use arrow keys to change difficulty:',True,(0,0,0),(179,255,0))
        subt3 = text_subt2.render('Difficulty:',True, (199,100,100))
        subt4 = text_subt2.render(game.difficulty,True,(255,0,0),(200,200,255))
        game.game_display.blit(title,(0,0))
        game.game_display.blit(subt1,(75,250))
        game.game_display.blit(subt2,(225,400))
        game.game_display.blit(subt3,(280,450))
        game.game_display.blit(subt4,(375,450))
        pygame.display.update()
           
    player = Player(game)
    red_ball = redBall(game)
    balls = [red_ball]
    display_score(game)
    pygame.display.update()
    count = 0

    while game.crash==False:
        game.score+=1
        game.game_display.blit(game.background,(0,0))
        for ball in balls:
            ball.moving_balls(game)
        for event in pygame.event.get():
                        
            if event.type == QUIT:
                game.crash= True
            if event.type==KEYDOWN:
                if event.key == K_ESCAPE:
                    game.crash = True
                if event.key==K_LEFT:
                    player.direction=ANTICLOCKWISE
                if event.key==K_RIGHT:
                    player.angle-=5
                    player.direction=CLOCKWISE
                if event.key==K_UP:
                    player.motion=True

            if event.type==KEYUP:
                if event.key == K_UP:
                    player.motion=False
                if event.key == K_RIGHT or event.key== K_LEFT:
                    player.direction=None
        player.rotate_player(game)
        
        if count>=game.spawn_count:
            x = randint(1,3)
            if x==1:
                balls.append(redBall(game))
            elif x==2:
                balls.append(blueBall(game))
            elif x==3:
                balls.append(greenBall(game))
            count=0
        count=count+1
        
        
        if check_collision(player,balls) or player_crashed(player,game):
            game.crash=True
            game.game_display.blit(game.explosion,player.rect_coord.topleft)
            pygame.display.update()
            time.sleep(2)
        display_score(game)   
        pygame.display.update()
        game.clock.tick(game.fps)

pygame.display.quit()
    
                
          
            
            

