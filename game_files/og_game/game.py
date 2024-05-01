
import pygame
import sys
from pygame.constants import K_BACKSPACE, K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import os
import random
from itertools import islice
import math
pygame.display.set_caption("project plane")
projecticon=pygame.image.load("Planes/F22/F22-Facing-Forward.png")
pygame.display.set_icon(projecticon)
replitbad=False
timer_m=0

timer_s=0

pygame.font.init()

if not replitbad:

    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)
highscore=0
experience=1

accel=1
settingspreference=open("settings-containing.csv","r").read().splitlines()
movement=[[],[],[],[]]
skip=False
for line,text in enumerate(settingspreference):
    if line>=4:
        continue
    Skip=False
    for words in range(len(text)):
        if text[words] == ",":
            skip=False
            continue

        if text[words] == "-" and text[words+1] == "1":
            movement[line].append(-1)
            skip=True
        if text[words] == "d" and text[words+1] == "i":
            movement[line].append("di")
            skip=True
        if text[words]=="i":
            skip=False
        if not skip:

            movement[line].append(int(text[words]) if text[words]=="1" else f"{text[words]}")
pushback=2
x,y=int(settingspreference[len(settingspreference)-pushback-1]),int(settingspreference[len(settingspreference)-pushback])
overall_sound=float(settingspreference[len(settingspreference)-1])



moveup,moveleft,movedown,moveright=movement[0],movement[1],movement[2],movement[3]
collection=[("F2F",7,3,500),("F4U",6,5,750),("F22",2,10,1000),("beaufighter",1,10,1000)]#0= plane,1= fire rate, 2= speed, 3= health
enemycollection=[("Bi-Enemy",5,None),("tempest",7,None),("harrier",10,None)]
bosscollection=[("beaufighter",10,1)] # 0= plane, 1= speed 
abilities=[("Propeller-Dispresion"),("Missile-Barrage"),("High-Calibre"),("Accelerated-Shot"),("Advanced-Airframe"),("The-Fat-Man")]
abilitydescription=["The propeller seems to be malfunctioning,^ wind is disperssing all over now!",
                    "The plane is now capable of holding Aim-9s,^ it does takes a while to reload",
                    "High calibre rounds pierce through the enemy,^ causing enemies to explode!",
                    "The cannon fires at a higher rate^",
                    "The mechanical structure of the plane has increased^",
                    "The Fat Man^"]

pause=False

screen = pygame.display.set_mode((x, y),pygame.RESIZABLE)

clock = pygame.time.Clock()
tick=0

class paused:
    def __init__(self) -> None:
        self.sfont=pygame.font.SysFont("arialblack",100,bold=False)
        self.paused_text_behind=self.sfont.render("PAUSED",True,(0,0,0))
        self.paused_text=self.sfont.render("PAUSED",True,(255,255,255))
        self.score=self.sfont.render(f"score:{highscore}",True,(255,255,255))
    def draw(self):
        abilityselection.update_location()
        self.sfont=pygame.font.SysFont("arialblack",screen.get_height()//7,bold=False)
        self.paused_text_behind=self.sfont.render("PAUSED",True,(0,0,0))
        self.paused_text=self.sfont.render("PAUSED",True,(255,255,255))
        self.score=self.sfont.render(f"score:{highscore}",True,(255,255,255))
        if not abilityselection.real:
            screen.blit(self.score,(abilityselection.bigbox.centerx-self.score.get_width()//2,abilityselection.bigbox.y))
            screen.blit(self.paused_text,(abilityselection.bigbox.centerx-self.paused_text.get_width()//2,abilityselection.bigbox.y+self.score.get_height()))
            #screen.blit(self.paused_text_behind,(abilityselection.bigbox.centerx-self.paused_text.get_width()//2-5,abilityselection.bigbox.centery-self.paused_text.get_height()//2))


cloudsonscreen=[]
class cloud:
    def __init__(self,y,least,most) -> None:
        self.cloud=pygame.image.load(f"Clouds/cloud-{random.randint(least,most)}.png")
        self.cloud_positionx=0-self.cloud.get_width()
        self.cloud_positiony=y


    def update(self):

        self.cloud_positionx=1+self.cloud_positionx


        screen.blit(self.cloud,(self.cloud_positionx,self.cloud_positiony))

    def nuked(self):
        pass

    def get_x(self):
        return True if self.cloud_positionx<screen.get_width() else False

fade=[0,166,201]
nuke_tint=[224, 151, 16]
def backdrop(tick,nuke):
    global fade,nuke_tint
    tick+=1
    if not nuke:
        screen.fill((0, 166, 201))
        fade=[0,166,201]
    else:
        if fade[0]<nuke_tint[0]:
            fade[0]+=3
        if fade[1]>nuke_tint[1]:
            fade[1]-=1
        if fade[2]>nuke_tint[2]:
            fade[2]-=1

        screen.fill((fade[0],fade[1],fade[2]))
    if tick%50==0:
        cloudsonscreen.append(cloud(random.randint(0,screen.get_height()),1,2))
    if tick%500==0:
        cloudsonscreen.append(cloud(random.randint(0,screen.get_height()),3,4))
    for theclouds in cloudsonscreen:
        if theclouds.get_x():
            theclouds.update()

        else:
            cloudsonscreen.pop(cloudsonscreen.index(theclouds))

        if nuke:
            theclouds.nuked()

class fatmannuke:
    def __init__(self,xx,yy,sideveloc):
        self.nuke_image=pygame.image.load("abilities/The-Fat-Man.gif")
        self.rect=self.nuke_image.get_rect()
        self.nuke_image=pygame.transform.scale_by(self.nuke_image,2)
        self.rect.center=xx,yy
        self.velocity=-1
        self.sidevel=sideveloc//2
        self.ticker=0

    def update(self):
        self.ticker+=1
        self.velocity+=1 if self.ticker%10==0 else 0 
        self.rect.centery+=self.velocity
        self.rect.centerx+=self.sidevel
        screen.blit(self.nuke_image,(self.rect.centerx,self.rect.centery))
    def explode(self):
        pass



class propeller_dispersion:
    def __init__(self,xx,yy):
        self.frame=pygame.image.load("prop/propeller-0.png")
        self.rect=self.frame.get_rect()
        self.frameon=0
        self.rect.center=xx,yy
        self.x,self.y=xx-10,yy
        self.rect=self.rect.inflate(self.frame.get_width()*3,self.frame.get_height()*3)
    def image_get(self):
        if tick%6==0:
            self.frameon=self.frameon+1 if self.frameon+1<9 else 0
        self.frame=pygame.image.load(f"prop/propeller-{self.frameon}.png")
        self.frame=pygame.transform.scale_by(self.frame,4)
        screen.blit(self.frame,(self.rect.x,self.rect.y))

        self.rect.x=firstplane.rect.x-self.frame.get_width()//4
        self.rect.y=firstplane.rect.y-self.frame.get_height()//4











class abilitywheel:
    def __init__(self):
        self.sfont = pygame.font.SysFont("arialblack", 30, bold=False)
        self.collectedabilities=[]
        self.slots=4
        self.canget=[]
        self.cangetability=[]
        self.justabilitynames=[]
        self.selecting=False
        self.real=False
        self.bigbox=pygame.Rect(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)
        self.textbox=pygame.Rect(self.bigbox.x*2,self.bigbox.y*2,self.bigbox.x//2,self.bigbox.y//2)
        self.evolve=False
        self.advancedairframe=False
        self.highcalibre=False
        self.AccelteratedShot=False
        self.missilebarrage=False
        self.propeller=False
        self.thefatman=False
        self.got=[]
    def update_location(self):
        if self.real==False:
            self.cangetability=[]
            self.canget=[]
            self.justabilitynames=[]
        self.bigbox.update(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)
        self.textbox.update(self.bigbox.x*2,self.bigbox.y*2,self.bigbox.x//2,self.bigbox.y//2)

    def advanced(self):
        return self.advancedairframe

    def abilitymaker(self):
        for abilities in self.collectedabilities:
            if abilities=="Advanced-Airframe":
                self.advancedairframe=True
            if abilities=="High-Calibre":
                self.highcalibre=True
            if abilities=="Accelerated-Shot":
                self.AccelteratedShot=True
            if abilities=="Missile-Barrage":
                self.missilebarrage=True
            if abilities =="Propeller-Dispresion":
                self.propeller=True
            if abilities == "The-Fat-Man":
                self.thefatman=True

    def randomthree(self):
        self.selecting=True
        self.real=True
        l=0
        self.cangetability=[]
        self.canget=[]
        self.justabilitynames=[]
        if (len(abilities) - len(self.collectedabilities))==0:
            self.evolve=True

        if not self.evolve:
            while len(self.cangetability) < 3 if (len(abilities) - len(self.collectedabilities))>3 else len(self.cangetability)<(len(abilities) - len(self.collectedabilities)):

                e=random.randint(0,len(abilities)-1)

                while abilities[e] in self.justabilitynames or abilities[e] in self.collectedabilities:
                    e=random.randint(0,len(abilities)-1)
                text=self.sfont.render(f"{abilities[e]}",True,(255,255,255))
                self.canget.append(button((self.bigbox.x+self.bigbox.x//2)-text.get_width()/2,(self.bigbox.y+self.bigbox.y//3)+self.bigbox.y//2*l,text))
                self.cangetability.append((abilities[e],e))
                self.justabilitynames.append(abilities[e])
                l+=1
        if self.evolve:
            self.canget.append(button(self.bigbox.x,(self.bigbox.y+self.bigbox.y//3)+self.bigbox.y//2*l,self.sfont.render("You can evolve!",True,(255,255,255))))
            self.cangetability.append("You-can-evolve!")






    def abilityscreen(self):
        abilityselection.update_location()
        pygame.draw.rect(screen,(0, 195, 237),self.bigbox)

        for number,l in enumerate(self.canget):
            self.textbox=pygame.Rect(self.bigbox.x*2,self.bigbox.y+5,self.bigbox.x-5,self.bigbox.y*2-20)
            l.check(lambda:l.select_ability(self.cangetability[number][0],self.collectedabilities,abilityselection.flip()))
            l.text(self.cangetability[number][0],(self.bigbox.x*2.25,self.bigbox.y+self.bigbox.y//10),self.cangetability[number][1],self.textbox,(True if self.cangetability[0]=="You-can-evolve!" else False))




    def stillgetting(self): return self.selecting

    def flip(self): 
        self.selecting=False
        self.real=False



abilityselection=abilitywheel()






running=True

bullets=pygame.sprite.Group()
class bullet(pygame.sprite.Sprite):
    def __init__(self,group,x,y,facing,aim,boss):
        global tick
        self.selected="Bullet"
        if abilityselection.highcalibre:
            self.selected="High"
        if aim:
            self.selected="aim"

        self.bullet=pygame.image.load("Bullet_Sprite/Bullet.png") # the bullet

        self.bulletspawnx,self.bulletspawny=x,y # where the bullet spawns
        self.vertical=0
        self.diagonal=0
        self.facing=facing
        self.degreeofbullet=0
        self.velocity=1
        self.boss=boss
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((self.bullet.get_width(),self.bullet.get_height()))

        self.rect=self.image.get_rect()

        self.rect.center=x,y

        if not boss:
            if facing == 270:
                self.diagonal=-1
            self.bullet=pygame.image.load(f"Bullet_Sprite/{self.selected}-Facing-Left.png")
            if facing == -270:
                self.diagonal=1
                self.bullet=pygame.image.load(f"Bullet_Sprite/{self.selected}-Facing-Right.png")
            if facing==360:
                self.vertical=-1
                self.bullet=pygame.image.load(f"Bullet_Sprite/{self.selected}.png")
            if facing == -180:
                self.vertical=1
                self.bullet=pygame.image.load(f"Bullet_Sprite/{self.selected}-Facing-Down.png")
        else:
            '''This works for getting the angle from the two points, use this equation if wanting to give the plane full 360 movement'''
            self.degreeofbullet=math.degrees(math.atan2(firstplane.rect.centery-self.rect.centery,firstplane.rect.centerx-self.rect.centerx))-90
            supertester=math.degrees(math.atan2(pygame.mouse.get_pos()[1]-self.rect.centery,pygame.mouse.get_pos()[0]-self.rect.centerx))-90
            self.degreeofbullet=abs(self.degreeofbullet) if self.degreeofbullet<=0 else -abs(self.degreeofbullet)
            supertester=abs(supertester) if supertester<=0 else -abs(supertester)
            self.bullet=pygame.transform.rotate(pygame.transform.flip(self.bullet,False,True),self.degreeofbullet)

            #180 UP, 0 DOWN
            #90 RIGHT, -90 LEFT

            range=[0.9,1,1.1,1.2,1.3]
            self.diagonal=math.cos(math.radians(self.degreeofbullet))*self.velocity
            self.vertical=math.sqrt(math.pow(self.velocity,2) - math.pow(self.diagonal,2))

            self.diagonal=-abs(random.choice(range[0:2])+self.diagonal if self.degreeofbullet>180 else 1-self.diagonal) if self.degreeofbullet>180 or self.degreeofbullet<0 else (1-self.diagonal if self.degreeofbullet<90 else abs(1+self.diagonal))
            self.vertical=-abs(random.choice(range[1:3])-(self.vertical)) if self.degreeofbullet>90 else random.choice(range[2:4])-self.vertical


        self.group=group


    def x(self):

        return True if 0<self.rect.x<screen.get_width() else False
    def y(self):

        return True if 0<self.rect.y<screen.get_height() else False



    def bullet_update(self):
        velocity=15
        if self.selected=="High" and not self.boss:
            velocity=7
        if not abilityselection.selecting:
            self.rect.x,self.rect.y=self.rect.x+(self.diagonal*velocity),self.rect.y+(self.vertical*velocity)
        screen.blit(self.bullet,(self.rect.x,self.rect.y))
    def bullet_collide(self,enemy_count):

        if enemy_count.rect.colliderect(self.rect):
            if self.selected=="Bullet":
                enemy_count.damage(10)
            if self.selected=="High":
                enemy_count.damage(20)
            if self.selected=="aim":
                enemy_count.damage(30)




    def bullet_get_rect(self):
        return self.rect

class button:
    def __init__(self,x,y,content):
        self.there=False
        self.content=content
        self.x,self.y=x,y
        self.rect=pygame.Rect((self.x,self.y), (content.get_width() if content.get_width()>100 else 100,content.get_height()))
        if not replitbad:
            self.hover=pygame.mixer.Sound("sound/click.wav")
            self.hover.set_volume(overall_sound)
            self.selected=pygame.mixer.Sound("sound/selectabil.wav")
            self.selected.set_volume(overall_sound)
        self.hoveronce=False
        self.hovertick=0
    def text(self,ability,bigbox,anumber,textbox,evolve):

            self.rect=pygame.Rect((self.x,self.y), (self.content.get_width() if self.content.get_width()>100 else 100,self.content.get_height()))

            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(screen,(0, 195, 237),self.rect)
                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not replitbad:
                    self.hover.play()

                self.hovertick+=1
                if ability:
                    e=pygame.image.load(f"abilities/{ability}.gif")

                    text=pygame.font.SysFont("arialblack",abilityselection.bigbox.w//40)
                    ability_image=pygame.transform.scale_by(e,abilityselection.bigbox.w//(e.get_width()*4))


                    toptext=""
                    bottomtext=""
                    if not evolve:
                        for numbers,letters in enumerate(abilitydescription[anumber]):

                            if letters=="^":


                                toptext=abilitydescription[anumber][:numbers]
                                bottomtext=abilitydescription[anumber][numbers+1:]

                    dave=text.render(f"{toptext}",True,(255,255,255))
                    pygame.draw.rect(screen,(0,137,167),textbox)
                    screen.blit(dave,(textbox[0],bigbox[1]+ability_image.get_height()+30))
                    screen.blit(text.render(f"{bottomtext}",True,(255,255,255)),(textbox[0],bigbox[1]+ability_image.get_height()+dave.get_height()+30))
                    screen.blit(ability_image,bigbox)
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(screen,(0,137,167),self.rect)
            else:
                self.hoveronce=False
                self.hovertick=0
                pygame.draw.rect(screen,(0, 173, 212),self.rect)

            if pygame.display.get_init():
                screen.blit(self.content,self.rect)

    def check(self,objective):
        global mouse
        mouse=pygame.mouse.get_pos()
        #update it hopefully
        self.rect=pygame.Rect((self.x,self.y), (self.content.get_width() if self.content.get_width()>100 else 100,self.content.get_height()))
        #
        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if not replitbad:
                        self.selected.play()
                    pygame.draw.rect(screen,(0,137,167),self.rect)


                    objective()
    def returnmm(self):
        pygame.display.quit()
        os.system("python main.py")
        sys.exit()

    def select_ability(self,ability,gottenability,select):
        select

        gottenability.append(ability)




class death:
    def __init__(self):
        global highsore

        self.boarder=pygame.Rect(x//4,y//4,x//2,y//2)

        self.move=False
        self.sfont = pygame.font.SysFont("arialblack", 100, bold=False)
        self.death_back=self.sfont.render("YOU DIED",True,(0,0,0))
        self.death_forward=self.sfont.render("YOU DIED",True,(255,0,0))
        self.high=self.sfont.render(f"score:{highscore}",True,(255,255,255))
        self.mainmenu=self.sfont.render("main menu",True,(255,255,255))

        self.menu=button(self.boarder.centerx-self.mainmenu.get_width()//2,y//2+self.boarder.y,self.mainmenu)
    def message(self):
        self.boarder.update(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)
        pygame.draw.rect(screen,(0,130,149),self.boarder)
        screen.blit(self.death_back,(self.boarder.centerx-self.death_back.get_width()//2,self.boarder.centery/2))
        screen.blit(self.death_forward,(self.boarder.centerx+5-self.death_back.get_width()//2,self.boarder.centery/2))

        self.menu.text(None,None,None,None,None)
        screen.blit(self.high,(self.boarder.centerx-self.high.get_width()//2,self.boarder.centery))
        self.menu.check(lambda: self.menu.returnmm())
ded=death()


bulletlist=[]
bulletlistboss=[]
listofenimies=[]
listoftempests=[]
listofboss=[]

playerplanes=pygame.sprite.GroupSingle()
class player(pygame.sprite.Sprite):
    def __init__(self,group,xx,yy,collection):


        '''THE LEVELING SYSTEM WORKS :D YIPEEE'''
        '''to be used for later when developing leveling system'''
        self.level=1
        self.nextlevel=50
        ''''''
        self.collection=collection


        self.selected=0


        self.firerate=self.collection[self.selected][1]
        self.highcalibreselected=False
        self.accel=False


        self.playerplane=pygame.image.load(f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png")#Planes/F22/project-plane-icon.png
        self.maxx=self.collection[self.selected][2]
        self.least=-abs(self.maxx)
        self.planetick=0
        self.missiletick=0
        self.missilefirerate=200
        self.bulletlist=bulletlist

        self.health=self.collection[self.selected][3] if  not abilityselection.advanced() else self.collection[self.selected][3]*1.1

        self.sfont = pygame.font.SysFont("arialblack", 30, bold=False)


        if not replitbad:
            self.shoot=pygame.mixer.Sound("sound/hitHurt.wav")
            self.shoot.set_volume(overall_sound)
            self.death_sound=pygame.mixer.Sound("sound/DEATH.wav")
            self.death_sound.set_volume(overall_sound)
        self.iterative=0

        self.facing=360

        self.angle=[(360,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png"),(270,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Left.png"),(-180,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Down.png"),(-270,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Right.png")]
        self.constantx,self.constanty=0,0

        self.group=group
        pygame.sprite.Sprite.__init__(self)
        self.x,self.y=xx,yy
        self.touching_edge=False
        self.touching_edgey=False



        self.image=pygame.Surface((projecticon.get_width(),projecticon.get_height()))

        self.rect=self.image.get_rect()
        self.rect.center=xx,yy


    def damage(self,damagetook):

            self.health-=damagetook
    def evolver(self):
        self.selected+=1 if self.selected+1<len(self.collection) else 0
        abilityselection.collectedabilities=[]
        abilityselection.AccelteratedShot=False
        abilityselection.evolve=False
        abilityselection.highcalibre=False
        abilityselection.missilebarrage=False
        abilityselection.propeller=False
        abilityselection.thefatman=False
        abilityselection.advancedairframe=False

        self.firerate=self.collection[self.selected][1]

        self.health=self.collection[self.selected][3] if  not abilityselection.advanced() else self.collection[self.selected][3]*1.1

        self.angle=[(360,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png"),(270,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Left.png"),(-180,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Down.png"),(-270,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Right.png")]
        self.playerplane=pygame.image.load(f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png")#Planes/F22/project-plane-icon.png
        self.maxx=self.collection[self.selected][2]



    def healthbar(self):
        global experience
        experience=experience
        self.health=self.health

        if experience>=self.nextlevel:
            self.nextlevel=self.nextlevel*1.5 if self.nextlevel<10000 else self.nextlevel*1.1

            '''make soft cap'''

            self.level+=1
            experience=0

            abilityselection.randomthree()
            self.health=self.collection[self.selected][3] if not abilityselection.advanced() else self.collection[self.selected][3]*1.1

        blackbox_experience=pygame.Rect(10,2,screen.get_width()-16,24)
        experience_rectangle=pygame.Rect(12,4,(experience/self.nextlevel)*screen.get_width(),20)

        blackbox=pygame.Rect(10,6+blackbox_experience.h,self.health+6,20)
        redbox=pygame.Rect(13,7+blackbox_experience.h,self.health,17)
        pygame.draw.rect(screen,(0,0,0),blackbox_experience)
        pygame.draw.rect(screen,(0, 206, 209),experience_rectangle)

        pygame.draw.rect(screen,(0,0,0),blackbox)
        pygame.draw.rect(screen,(255,0,0),redbox)

    def getrecter(self):
        return self.rect

    def view(self): # The looking aspect, even though we have calculations going on in this bit :D
        if abilityselection.evolve:
            abilityselection.evolve=False
            firstplane.evolver()
        if abilityselection.highcalibre and not self.highcalibreselected:
            self.firerate+=5
            self.highcalibreselected=True
        if abilityselection.AccelteratedShot and not self.accel:
            self.firerate-=1
            self.accel=True



        firstplane.healthbar()
        x,y=screen.get_width(),screen.get_height()




        if self.rect.y+self.constanty>0 and self.rect.y+self.constanty+self.image.get_height()<y and not abilityselection.stillgetting():
            self.rect.y+=self.constanty
            self.touching_edgey=False
        else:
            self.touching_edgey=True
            self.constanty=0


        if self.rect.x+self.constantx>0 and self.rect.x+self.constantx+self.image.get_width()<x and not abilityselection.stillgetting():
            self.rect.x+=self.constantx
            self.touching_edge=False
        else:
            self.touching_edge=True
            self.constantx=0 # sets back to 0 for QOL


        #The actual viewing bit of the view subclass
        '''for it to update and draw we need these two, along with the group that it is in, which will be a single group since we only want one player'''
        self.group.update()
        #self.group.draw(screen) # DRAWS BLACK BOX AROUND PLANE
        screen.blit(self.playerplane,(self.rect.x,self.rect.y)) #DRAWS PLANE

        e=self.missiletick%self.missilefirerate==0 and abilityselection.missilebarrage
        if (pygame.key.get_pressed()[K_SPACE] and self.planetick%self.firerate==0 )and not(self.missiletick%self.missilefirerate==0 and abilityselection.missilebarrage):
            if not replitbad:
                self.shoot.play()

            self.bulletlist.append(bullet(bullets,self.rect.x+self.playerplane.get_width()//2 -10 if self.selected==1 else self.rect.x+self.playerplane.get_width()//2,self.rect.y+self.playerplane.get_height()//2 - 10 if self.selected == 1 else self.rect.y+self.playerplane.get_height()//2,self.facing,False,False))
            if self.selected==1:
                if not replitbad:
                    self.shoot.play()
                self.bulletlist.append(bullet(bullets,self.rect.x+self.playerplane.get_width()//2 +10,self.rect.y+self.playerplane.get_height()//2 +10,self.facing,False,False))


        if e:
            self.missilefirerate=self.missilefirerate+1 if self.missilefirerate<=205 else 200
            self.bulletlist.append(bullet(bullets,random.randint(self.rect.x,self.rect.x+self.playerplane.get_width()//2 -10 )if self.selected==1 else random.randint(self.rect.x,self.rect.x+self.playerplane.get_width()//2),random.randint(self.rect.y,self.rect.y+self.playerplane.get_height()//2 - 10) if self.selected == 1 else random.randint(self.rect.y,self.rect.y+self.playerplane.get_height()//2),self.facing,True,False))
        if pygame.key.get_pressed()[K_SPACE]:
            self.planetick+=1



        else:
            self.planetick=0
        self.missiletick+=1



        if self.health<=0:
            if self.iterative==0:
                if not replitbad:
                    self.death_sound.play()
                self.iterative+=1
            ded.message()








        ''''''



    def mover(self,move,event):
        global x,y

        #self.angle=[(360,f"Planes/{self.collection[self.selected]}/{self.collection[self.selected]}-Facing-Forward.png"),(270,f"Planes/{self.collection[self.selected]}/{self.collection[self.selected]}-Facing-Left.png"),(-180,f"Planes/{self.collection[self.selected]}/{self.collection[self.selected]}-Facing-Down.png"),(-270,f"Planes/{self.collection[self.selected]}/{self.collection[self.selected]}-Facing-Right.png")]
        #we change skin, will only be when level up but I am making it change because I want to seeeeeeeeee

        if event.type == pygame.KEYDOWN or pygame.key.get_pressed():

            for number,keys in enumerate(move):
                if self.health<1:
                    continue
                if pygame.key.get_pressed()[pygame.key.key_code(keys[0])]:
                        if self.facing!=self.angle[number][0]:
                            #self.facing-self.angle[number]
                            self.playerplane=pygame.image.load(self.angle[number][1])
                            self.facing=self.angle[number][0]

                        if keys[2]=="u": # if player is moving vertical
                            self.constanty+=keys[1] if self.least-1<=self.constanty+keys[1] and self.constanty+keys[1] <= self.maxx else 0

                        else: # if player is moving diagonal
                            self.constantx+=keys[1] if self.least-1<=self.constantx+keys[1] and self.constantx+keys[1] <= self.maxx else 0


    def positionx(self):
        return self.x
    def positiony(self):
        return self.y



firstplane=player(playerplanes,x//2,y//2,collection)
playerplanes.add(firstplane)
propel=propeller_dispersion(firstplane.x,firstplane.y)




enemies=pygame.sprite.Group()
class enemy(pygame.sprite.Sprite):
    def __init__(self,group,xx,yy,collection,health,selected,xpgain,firewait):
        self.collection=collection
        self.x,self.y=xx,yy

        self.constantx,self.constanty=0,0
        self.firewait=0
        if firewait:
            self.firewait=firewait
        self.planetick=0
        self.burst=False
        self.burst_tick=0
        self.group=group


        self.health=health
        self.healthmax=health
        self.selected=selected
        self.xpgain=xpgain
        self.maxx=2
        self.least=-abs(self.maxx)
        self.firerate=self.collection[self.selected][1]

        if len(self.collection[self.selected])>=2:
            self.max=self.collection[self.selected][2]
        self.enemy_sprite=pygame.image.load(f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png")


        self.facing=360
        self.facingindex=0
        #I hate that this is the solution to rotating the plane        
        self.angle=[(360,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png"),(270,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Left.png"),(-180,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Down.png"),(-270,f"Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Right.png")]

        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.Surface((self.enemy_sprite.get_width(),self.enemy_sprite.get_height()))

        self.rect=self.image.get_rect()
        self.rect.center=xx,yy

    def view(self):



        self.group.update()

        screen.blit(self.enemy_sprite,(self.x,self.y))
        if self.collection is bosscollection:
            self.health=self.health

            healthbarr_backdrop=pygame.Rect(14,screen.get_height()-26,screen.get_width()-30,22)
            pygame.draw.rect(screen,(0,0,0),(healthbarr_backdrop))
            healthbarr=pygame.Rect(15,screen.get_height()-25,(self.health/self.healthmax)*healthbarr_backdrop.width,20)

            pygame.draw.rect(screen,(255,0,0),(healthbarr))

    def damage(self,damage_taken):
        self.health-=damage_taken





    def health_get(self):

        return True if int(self.health)>0 else False

    def getposx(self):
        return True if 0-self.enemy_sprite.get_width()<self.rect.x<screen.get_width() else False

    def getposy(self):
        return True if 0-self.enemy_sprite.get_height()<self.rect.y<screen.get_height() else False
    def get_plane(self):
        return self.collection[self.selected]

    def move_plane(self):

        if not abilityselection.stillgetting():
            self.rect.x=self.rect.x+self.constantx
            self.rect.y=self.rect.y+self.constanty
            self.x=self.rect.x
            self.y=self.rect.y



        if self.facing!=self.angle[self.facingindex][0]:

                self.enemy_sprite=pygame.image.load(self.angle[self.facingindex][1])
                self.facing=self.angle[self.facingindex][0]


        if firstplane.rect.center[0] >= self.x+self.constantx and self.constantx<=self.maxx:
            self.constantx+=0.05
        elif firstplane.rect.center[0] <= self.x+self.constantx and self.constantx>=self.least:
            self.constantx-=0.05
        if firstplane.rect.center[1] >= self.y+self.constanty and self.constanty<=self.maxx:
            self.constanty+=0.05
        elif firstplane.rect.center[1] <= self.y+self.constanty and self.constanty>=self.least:

            self.constanty-=0.05
        self.planetick+=1

        if self.constantx<0 and self.constantx<self.constanty:
            self.facingindex=1


        if self.constanty<0 and self.constanty<self.constantx:
            self.facingindex=0



        if self.constantx>0 and self.constantx>self.constanty:

            self.facingindex=3

        if self.constanty>0 and self.constanty>self.constantx:

            self.facingindex=2








        if not abilityselection.stillgetting():
            self.x+=self.constantx
            self.y+=self.constanty


        if self.rect.colliderect(firstplane.rect):
            firstplane.damage(10)

    def beaufighter_movement(self):
        #pygame.draw.circle(screen,(0,0,0),(screen.get_width()//2,screen.get_height()//2),screen.get_height()//3)
        '''boss make boss path around the player and shoot''' 
        if tick%self.firewait==0:
            self.burst=True
            self.burst_tick=tick
        if self.burst_tick+self.firerate*5>=tick and tick%self.firerate==0:
            bulletlistboss.append(bullet(bulletlistboss,self.rect.centerx,self.rect.centery,self.facing,False,True))
        else:
            self.burst=False





class round:
    def __init__(self):
        global highscore,experience

        self.round_count=1
        self.count=1
        self.max_enemiesonscreen=100

        #self.enemy_plane=enemy(enemies,100,100,enemycollection)
        self.selected=[0,0]
        self.listofspawnsx=[(1,screen.get_width()+200)]
        self.listexplosion=[]
        self.listofnuke=[]
        self.nuke_detonation=False
        self.timesince_detonation=0
        self.detonation_timer=300

        self.tick=0
        self.score=0

        self.budget=0
        self.sfont = pygame.font.SysFont("arialblack", 30, bold=False)
        self.score_text=self.sfont.render(f"{highscore}",True,(255,255,255))
        self.timer=self.sfont.render(f"{timer_m}:{timer_s}",True,(255,255,255))

        self.explosion=pygame.image.load("Bullet_Sprite/explosion.png")
        self.explosionradius=self.explosion.get_rect()
        self.explosionradius[2]+=1000
        self.explosionradius[3]+=1000
        self.bossalive=False


        if not replitbad:

            self.dead_enemy_sound=pygame.mixer.Sound("sound/dead_enemy.wav")
            self.dead_enemy_sound.set_volume(overall_sound)
    def enemyorbossupdate(self,list):
        global highscore,experience
        for enemycountter in islice(list,0,self.max_enemiesonscreen):
            if enemycountter.health_get():
                if enemycountter.getposx() and enemycountter.getposy():
                    enemycountter.view()
                if not abilityselection.stillgetting() and list==listofenimies:
                    enemycountter.move_plane()
                elif enemycountter.collection[enemycountter.selected][0]=="beaufighter":
                    enemycountter.move_plane()
                    enemycountter.beaufighter_movement()

                if abilityselection.propeller and propel.rect.colliderect(enemycountter):
                    enemycountter.damage(10)


            else:
                list.pop(list.index(enemycountter))
                screen.blit(self.explosion,(enemycountter.x,enemycountter.y))
                #if abilityselection.highcalibre:

                self.listexplosion.append((enemycountter.x,enemycountter.y,self.tick+5))
                self.explosionradius.x,self.explosionradius.y=enemycountter.x,enemycountter.y


                if not replitbad:
                    self.dead_enemy_sound.play()
                highscore+=10
                experience+=enemycountter.xpgain if not firstplane.selected<=3 else enemycountter.xpgain*6
        for explosions in self.listexplosion:

            if self.tick<=explosions[2]:
                screen.blit(self.explosion,(explosions[0],explosions[1]))

            else:
                self.listexplosion.pop(self.listexplosion.index(explosions))
    def update(self):

        self.listofspawnsx=[(1,screen.get_width()+200)]
        self.listofspawnsy=[(-10,screen.get_height()+200)]
        self.score_text=self.sfont.render(f"{highscore}",True,(255,255,255))
        self.timer=self.sfont.render(f"{timer_m}:{timer_s}",True,(255,255,255))
        screen.blit(self.score_text,(screen.get_width()//2-self.score_text.get_width()//2,60))
        screen.blit(self.timer,(screen.get_width()//2-self.timer.get_width()//2,60+self.score_text.get_height()))
        if self.round_count!=self.count:
            self.round_count+=1
            self.budget=self.round_count

            while self.budget>0:
                x=0
                y=0
                tempest_x=0
                tempest_y=0

                you_are_my_special=False
                sideortopside=random.randint(0,1)
                if sideortopside==0:
                    x=random.choice(self.listofspawnsx[0])-100
                    y=screen.get_height()//2+(random.randint(-screen.get_height()//2,screen.get_height()//2))
                if sideortopside==1:
                    x=screen.get_width()//2+(random.randint(-screen.get_width()//2,screen.get_width()//2))
                    y=random.choice(self.listofspawnsy[0])-100
                if self.round_count==10: # beaufighter boss
                    self.budget=0
                    listofenimies.clear()
                    listofboss.append(enemy(enemies,screen.get_width()//4,screen.get_height()//4,bosscollection,10000,0,0,500)) # group,xx,yy,collection,health,selected,xpgain,firewait
                    self.bossalive=True
                if self.budget%30==0 and not self.bossalive: # harrier
                    listofenimies.append((enemy(enemies,x-100,y,enemycollection,1500,2,50,None)))
                    you_are_my_special=True
                if self.budget%10==0 and not self.bossalive: # tempest 
                    self.budget-=30


                    if sideortopside==0:
                        tempest_x=random.choice(self.listofspawnsx[0])-100
                        tempest_y=screen.get_height()//2+(random.randint(-screen.get_height()//2,screen.get_height()//2))
                    if sideortopside==1:
                        tempest_x=screen.get_width()//2+(random.randint(-screen.get_width()//2,screen.get_width()//2))
                        tempest_y=random.choice(self.listofspawnsy[0])-100
                    listofenimies.append((enemy(enemies,tempest_x-100,tempest_y,enemycollection,500,1,20,None)))
                    you_are_my_special=True
                    self.budget-=10
                if self.budget!=0 and not you_are_my_special: #biplane

                    listofenimies.append((enemy(enemies,x-100,y,enemycollection,130,0,10,None)))
                    self.budget-=1

        for nuke in self.listofnuke:
            if nuke.rect.y < screen.get_height():
                nuke.update()
            else:
                nuke.explode()
                self.listofnuke.pop(self.listofnuke.index(nuke))
                self.timesince_detonation=tick
                self.nuke_detonation=True
                listofenimies.clear()


        if self.timesince_detonation+self.detonation_timer< tick:
                self.nuke_detonation=False

        for bullet in bulletlist:

            if bullet.x() and bullet.y():

                bullet.bullet_update()
                for l in islice(listofenimies,0,self.max_enemiesonscreen):
                    bullet.bullet_collide(l)
                if listofboss:
                    for boss in listofboss:
                        bullet.bullet_collide(boss)


            else:
                bulletlist.pop(bulletlist.index(bullet))
        for bullet in bulletlistboss:
            if bullet.x() and bullet.y():
                bullet.bullet_update()
                bullet.bullet_collide(firstplane)

            else:
                bulletlistboss.pop(bulletlistboss.index(bullet))

        Round.enemyorbossupdate(listofenimies)
        Round.enemyorbossupdate(listofboss)

        if len(listofboss)==0:

            self.bossalive=False
        if self.tick%1500==0 and abilityselection.thefatman:
            self.listofnuke.append(fatmannuke(firstplane.rect.x,firstplane.rect.y,firstplane.constantx))
        if len(listofboss)==0 and not listofenimies or len(listofboss)==0 and self.tick%100==0:
            self.count+= 1
        if not abilityselection.stillgetting():
            self.tick+=1








Round=round()
p=paused()
while running:
    backdrop(tick,Round.nuke_detonation)
    tick+=1

    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            if abilityselection.real==False:
                abilityselection.selecting=True if abilityselection.selecting is False else False
                pause=True if pause is False else False



        if not abilityselection.stillgetting():
            firstplane.mover(movement,event)












    # has to be outside of loop so it can path, I say path loosely

    Round.update()
    firstplane.view()
    if abilityselection.propeller:
        propel.image_get()
    if abilityselection.stillgetting():
         abilityselection.abilityscreen()


    abilityselection.abilitymaker()


    if pause:
        p.draw()
    if tick%60==0:
        if timer_s==60:

            timer_s=0

            timer_m+=1



        timer_s+=1

    clock.tick(60)
    pygame.display.update()

'''
1.The battle bus
2. boss AI

'''