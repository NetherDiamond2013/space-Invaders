import pygame
import random
from pygame import mixer

class Enemy():
    def __init__(self):
        self.destroy()
        # self.good_bye=False
        self.enemyImg =pygame.image.load("ufo.png")
        self.enemyX_change = 1.2

    def enemy(self):
        if(not self.good_bye):
            screen.blit(self.enemyImg, (self.enemyX,self.enemyY))

    def destroy(self):
        self.good_bye=True
        self.enemyX = random.randint(40,760)
        self.enemyY = random.randint(1,50)

    def back_from_the_dead(self):
        self.good_bye=False

pygame.init()
screen=pygame.display.set_mode((800,600))

mixer.music.load("background.wav")
mixer.music.play(-1)
bang_sound =mixer.Sound("laser.wav")
kablam_sound =mixer.Sound("explosion.wav")
background=pygame.image.load("space background.png")

level=1
enemys_amount=1

playerImg =pygame.image.load("battleship.png")
playerX=380
playerY=450
playerX_change=0
hp=3
def player():
    screen.blit(playerImg, (playerX,playerY))

bossImg =pygame.image.load("boss alien.png")
bossX=380
bossY=10
bossX_change=0
bhp=13
battle=0
win=0
time=200
def boss():
    screen.blit(bossImg, (bossX,bossY))
def revive():
    num=random.randint(0,7)
    enemy_list[num].back_from_the_dead()


score=0
font=pygame.font.Font("freesansbold.ttf",58)
def show_score():
    score_obj=font.render("Score:"+str(score)+", level:"+str(level),True,(0,0,254))
    screen.blit(score_obj, (10,10))


speed=1
enemy1 = Enemy()
enemy1.back_from_the_dead()
enemy2 = Enemy()
enemy3 = Enemy()
enemy4 = Enemy()
enemy5 = Enemy()
enemy6 = Enemy()
enemy7 = Enemy()
enemy8 = Enemy()
enemy_list = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8]

boomImg =pygame.image.load("missile (1).png")
boomX=380
boomY=50
boomY_change=9.5
fire=0
def boom():
    screen.blit(boomImg, (boomX,boomY))

def isHit(enemyX, enemyY, boomX, boomY):
    if ( (boomY - enemyY) <= 40 ):
        if ( (boomX - enemyX) <= 40 ):
            distance = ( (boomX - enemyX-16)**2 + (boomY - enemyY-16)**2 )**(1/2)
            if (distance < 40):
                return True
    return False
def isHitB(enemyX, enemyY, boomX, boomY):
    if ( (boomY - enemyY) <= 40 ):
        if ( (boomX - enemyX) <= 40 ):
            distance = ( (boomX - enemyX-16)**2 + (boomY - enemyY-16)**2 )**(1/2)
            if (distance < 40):
                return True
    return False

running=True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change=1.2
            if event.key == pygame.K_LEFT:
                playerX_change=-1.2
            if event.key == pygame.K_SPACE:
                if (not fire):
                    fire=1
                    boomX,boomY=playerX+24,playerY
                    bang_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change=0

    show_score()

    playerX+=playerX_change
    if playerX<=0:
        playerX = 0
    elif playerX>=736:
        playerX = 736

    temp=level
    if temp>8:
        temp=8
    for i in range(0,temp):
        if(not enemy_list[i].good_bye):
            enemy_list[i].enemyX+=enemy_list[i].enemyX_change*speed
            if enemy_list[i].enemyX<=0:
                enemy_list[i].enemyX_change *= -1
                enemy_list[i].enemyY+=40
            elif enemy_list[i].enemyX>=768:
                enemy_list[i].enemyX_change *= -1
                enemy_list[i].enemyY+=40
            enemy_list[i].enemy()
            if (fire):
                if isHit(enemy_list[i].enemyX, enemy_list[i].enemyY, boomX, boomY):
                    enemy_list[i].destroy()
                    score+=1
                    enemys_amount-=1
                    fire=False
                    kablam_sound.play()
            if isHit(enemy_list[i].enemyX, enemy_list[i].enemyY, playerX, playerY):
                enemy_list[i].destroy()
                enemys_amount-=1
                kablam_sound.play()
                hp-=1


    if enemys_amount==0:
        level+=1

        if level>=9:
            battle=1
            enemys_amount=-1
        else:
            enemys_amount=level
            for i in range(0,level):
                enemy_list[i].back_from_the_dead()
    if battle:
        time -=1
        bhp_obj=font.render("bhp:"+str(bhp),True,(0,0,254))
        screen.blit(bhp_obj, (550,10))
        boss()
        if time==0:
            revive()
            time=200
        if (fire):
            if isHitB(bossX, bossY, boomX, boomY):
                bhp -=1
                speed *=1.2
                fire=False
                kablam_sound.play()
                if bhp==0:
                    while running:
                        screen.fill((0,0,0))
                        screen.blit(background,(0,0))
                        score_obj=font.render("good job you are the winner. Score:"+str(score),True,(0,0,254))
                        screen.blit(score_obj, (10,350))
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running=0


    if (fire):
        boom()
        boomY-=boomY_change
        if boomY<=0:
            fire=0

    if hp==0:
        while running:
            screen.fill((0,0,0))
            screen.blit(background,(0,0))
            score_obj=font.render("lol you dead\nScore:"+str(score),True,(0,0,254))
            screen.blit(score_obj, (250,350))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=0
    player()

    pygame.display.update()
