
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
collection=[("F2F",7,3,500,500),("F4U",6,4,750,200),("F22",2,5,1000,200),("F35",6,4,1100,200),("beaufighter",1,10000,1000,200)]#0= plane,1= fire rate, 2= speed, 3= health, 4= missile firerate
enemycollection=[("Bi-Enemy",5,None),("tempest",7,None),("harrier",10,None)]
bosscollection=[("beaufighter",10,1)] # 0= plane, 1= speed 
abilities=[("Propeller-Dispresion"),("Missile-Barrage"),("High-Calibre"),("Accelerated-Shot"),("Advanced-Airframe"),("The-Fat-Man"),("EMP"),("Shotgun"),("coin-madness"),("The-kiss-of-life")]
abilitydescription=["The propeller seems to be malfunctioning,^ wind is disperssing all over now!",
                    "The plane is now capable of holding Aim-9s,^ it does takes a while to reload",
                    "High calibre rounds pierce through the enemy,^ causing enemies to explode!",
                    "The cannon fires at a higher rate^",
                    "The mechanical structure of the plane has increased^",
                    "The Fat Man^",
                     "A burst of electromagnetic radiation,^ stopping enemies in their tracks, looks rather alien.",
                     "Why hasn't anyone thought of putting^ a shotgun on a plane yet!",
                     "A 10% increase in coin gain,^ nice!",
                     "restore plane with 75% health upon death,^ something strange happens though"]

pause=False

screen = pygame.display.set_mode((x, y),pygame.RESIZABLE)

clock = pygame.time.Clock()
tick=0

from paused_menu import paused
cloudsonscreen=[]
from shop_contain_list import shop_class
shop_contain=shop_class()




class propeller_dispersion:
    def __init__(self,xx,yy):
        self.frame=pygame.image.load("prop/propeller-0.png")
        self.rect=self.frame.get_rect()
        self.frameon=0
        self.rect.center=xx,yy
        self.x,self.y=xx-10,yy
        self.rect=self.rect.inflate(self.frame.get_width()*3,self.frame.get_height()*3)
        self.cooldown=True
    def image_get(self):
        if tick%6==0:
            self.frameon=self.frameon+1 if self.frameon+1<9 else 0
        self.frame=pygame.image.load(f"prop/propeller-{self.frameon}.png")

        self.frame=pygame.transform.scale_by(self.frame,4)
        screen.blit(self.frame,(self.rect.x,self.rect.y))

        self.rect.x=firstplane.rect.x-self.frame.get_width()//4
        self.rect.y=firstplane.rect.y-self.frame.get_height()//4

class emp:
    def __init__(self,xx,yy,facing):
        self.frame=pygame.image.load("emp_sprite_sheeet/Lightning-0.png")
        self.empblast_frame=pygame.image.load("emp_sprite_sheeet/emp-blast-0.png")
        self.shoot=pygame.image.load("emp_sprite_sheeet/EMP_SHOOT.png")
        self.explosion_radius=pygame.image.load("emp_sprite_sheeet/emp-blast-5.png").get_rect().scale_by(2)
        self.rect=self.frame.get_rect()
        self.frameon=0
        self.empframeon=0
        self.rect.center=xx,yy
        self.explosion_radius.center=xx,yy
        self.explosion=False
        self.zero_count=0
        self.diagonal=0
        self.vertical=0
        self.kill=False
        if facing == 270: # left
                self.diagonal=-1
                self.shoot=pygame.transform.rotate(self.shoot,90)
        if facing == -270: # right
                self.diagonal=1
                self.shoot=pygame.transform.rotate(self.shoot,-90)

        if facing==360: # up
                self.vertical=-1

        if facing == -180: # down
                self.vertical=1#
                self.shoot=pygame.transform.rotate(self.shoot,180)



        self.rect.x,self.rect.y=xx-self.frame.get_width()//2,yy-self.frame.get_height()//2
        self.explosion_radius.x,self.explosion_radius.y=xx-self.explosion_radius.w//2,yy-self.explosion_radius.h//2
    def image_get(self):
        if self.explosion:
            self.vertical,self.diagonal=0,0

        if self.zero_count>=5:

            self.kill=True
        if tick%7==0 and self.explosion:
            self.frameon=self.frameon+1 if self.frameon+1<6 else 0
            self.zero_count+=1
        if self.explosion:
            self.empblast_frame=pygame.image.load(f"emp_sprite_sheeet/emp-blast-{self.frameon}.png")
            self.frame=pygame.image.load(f"emp_sprite_sheeet/Lightning-{self.frameon}.png")
            self.empblast_frame=pygame.transform.scale_by(self.empblast_frame,1.24)
            oneonscreen=self.empblast_frame

        else:
            self.rect.x+=self.diagonal*3
            self.rect.y+=self.vertical*3
            self.explosion_radius.x=self.rect.x
            self.explosion_radius.y=self.rect.y
            oneonscreen=self.shoot




        screen.blit(oneonscreen,(self.rect.x,self.rect.y))
        #pygame.draw.rect(screen,(255,255,255),self.explosion_radius)
        #pygame.draw.rect(screen,(255,255,255),self.rect)

class shotgun_shoot:
    def __init__(self,xx,yy,facing) -> None:
        self.frameon=0
        self.frame=pygame.image.load(f"shotgun_sprite_sheet/shotgun_shot-{self.frameon}.png")
        self.frame=pygame.transform.scale_by(self.frame,2)
        self.diagonal,self.vertical=0,0
        self.facing=facing
        
        self.reset_count=0
        if facing == 270: # left
                self.diagonal=-1
                self.frame=pygame.transform.rotate(self.frame,90)
        if facing == -270: # right
                self.diagonal=1
                self.frame=pygame.transform.rotate(self.frame,-90)

        if facing==360: # up
                self.vertical=-1

        if facing == -180: # down
                self.vertical=1#
                self.frame=pygame.transform.rotate(self.frame,180)
        self.rect=self.frame.get_rect()
        self.rect.centerx,self.rect.centery=xx+(self.diagonal*100),yy+(self.vertical*100)

    def image_get(self):
        screen.blit(self.frame,(self.rect.centerx,self.rect.centery))
        if tick%4==0:
            self.frameon=self.frameon+1 if self.frameon+1<6 else 0
            self.reset_count+=1 if self.frameon==0 else 0
        print(self.reset_count)
        self.frame=pygame.image.load(f"shotgun_sprite_sheet/shotgun_shot-{self.frameon}.png")
        if self.facing == 270: # left
                self.diagonal=-1
                self.frame=pygame.transform.rotate(self.frame,90)
        if self.facing == -270: # right
                self.diagonal=1
                self.frame=pygame.transform.rotate(self.frame,-90)

        if self.facing==360: # up
                self.vertical=-1

        if self.facing == -180: # down
                self.vertical=1#
                self.frame=pygame.transform.rotate(self.frame,180)
        self.frame=pygame.transform.scale_by(self.frame,2)
















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
        self.emp=False
        self.kissoflife=False
        self.shotgun=False
        self.coinmad=False
        self.got=[]
    def update_location(self):
        if not self.real:
            self.cangetability=[]
            self.canget=[]
            self.justabilitynames=[]
        self.bigbox.update(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)
        self.textbox.update(self.bigbox.x*2,self.bigbox.y*2,self.bigbox.x//2,self.bigbox.y//2)

    def advanced(self):
        return self.advancedairframe

    def abilitymaker(self):
        for abilities in self.collectedabilities:
            self.advancedairframe=abilities=="Advanced-Airframe"
            self.highcalibre=abilities=="High-Calibre"
            self.AccelteratedShot=abilities=="Accelerated-Shot" 
            self.missilebarrage=abilities=="Missile-Barrage" 
            self.propeller=abilities =="Propeller-Dispresion" 
            self.thefatman=abilities == "The-Fat-Man"
            self.emp=abilities == "EMP"
            self.kissoflife = abilities == "The-kiss-of-life"
            self.shotgun= abilities == "Shotgun"
            self.coinmad= abilities == "coin-madness"
                

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

                self.canget.append(button_game((self.bigbox.x+self.bigbox.x//2)-text.get_width()/2,(self.bigbox.y+self.bigbox.y//3)+self.bigbox.y//2*l,text,replitbad,overall_sound,screen,abilityselection,abilitydescription))
                self.cangetability.append((abilities[e],e))
                self.justabilitynames.append(abilities[e])
                l+=1



        if self.evolve:
            self.canget.append(button_game((self.bigbox.x+self.bigbox.x//2)-self.sfont.render("You can evolve!",True,(255,255,255)).get_width()/2,(self.bigbox.y+self.bigbox.y//3)+self.bigbox.y//2*l,self.sfont.render("You can evolve!",True,(255,255,255)),replitbad,overall_sound,screen,abilityselection,abilitydescription))
            self.cangetability.append("You-can-evolve!")






    def abilityscreen(self):

        abilityselection.update_location()

        pygame.draw.rect(screen,(0, 195, 237),self.bigbox)


        for number,l in enumerate(self.canget):

            self.textbox=pygame.Rect(self.bigbox.x*2,self.bigbox.y+5,self.bigbox.x-5,self.bigbox.y*2-20)
            l.check(lambda: l.select_ability(self.cangetability[number][0],self.collectedabilities,abilityselection.flip()))
            l.text(self.cangetability[number][0],(self.bigbox.x*2.25,self.bigbox.y+self.bigbox.y//10),self.cangetability[number][1],self.textbox,(True if self.cangetability[0]=="You-can-evolve!" else False))

    def reset(self):
        self.AccelteratedShot=False
        self.evolve=False
        self.highcalibre=False
        self.missilebarrage=False
        self.propeller=False
        self.thefatman=False
        self.advancedairframe=False
        self.emp=False
        self.kissoflife=False
        self.shotgun=False
        self.coinmad=False

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

        self.bullet_image=pygame.image.load(f"Bullet_Sprite/{self.selected}.png") # the bullet
        if boss:
            self.bullet_image=pygame.image.load("Bullet_Sprite/Bullet.png")
        self.bulletspawnx,self.bulletspawny=x,y # where the bullet spawns
        self.vertical=0
        self.diagonal=0
        self.facing=facing
        self.degreeofbullet=0
        self.velocity=1
        self.boss=boss
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((self.bullet_image.get_width(),self.bullet_image.get_height()))

        self.rect=self.image.get_rect()

        self.rect.center=x,y


        if( not boss ) and not shop_contain.bullet_upgrade:
            if facing == 270:
                self.diagonal=-1
            self.bullet_image=pygame.image.load(f"Bullet_Sprite/{self.selected}-Facing-Left.png")
            if facing == -270:
                self.diagonal=1
                self.bullet_image=pygame.image.load(f"Bullet_Sprite/{self.selected}-Facing-Right.png")
            if facing==360:
                self.vertical=-1
                self.bullet_image=pygame.image.load(f"Bullet_Sprite/{self.selected}.png")
            if facing == -180:
                self.vertical=1
                self.bullet_image=pygame.image.load(f"Bullet_Sprite/{self.selected}-Facing-Down.png")
        else:
            place=0
            if boss:
                placex=firstplane.rect.centerx
                placey=firstplane.rect.centery
            else:
                placex=pygame.mouse.get_pos()[0]
                placey=pygame.mouse.get_pos()[1]
            '''This works for getting the angle from the two points, use this equation if wanting to give the plane full 360 movement'''
            self.degreeofbullet=math.degrees(math.atan2(placey-self.rect.centery,placex-self.rect.centerx))-90
            supertester=math.degrees(math.atan2(pygame.mouse.get_pos()[1]-self.rect.centery,pygame.mouse.get_pos()[0]-self.rect.centerx))-90
            self.degreeofbullet=abs(self.degreeofbullet) if self.degreeofbullet<=0 else -abs(self.degreeofbullet)
            supertester=abs(supertester) if supertester<=0 else -abs(supertester)
            self.bullet_image=pygame.transform.rotate(pygame.transform.flip(self.bullet_image,False,True),self.degreeofbullet)

            #180 UP, 0 DOWN
            #90 RIGHT, -90 LEFT

            range=[0.9,1,1.1,1.2,1.3]
            self.diagonal=math.cos(math.radians(self.degreeofbullet))* math.pow(self.velocity,10)
            self.vertical=math.sqrt(math.pow(self.velocity,2) - math.pow(self.diagonal,2))

            self.diagonal=-abs((1)+self.diagonal if self.degreeofbullet>=180 else 1-self.diagonal) if self.degreeofbullet>=180 or self.degreeofbullet<=0 else (1-self.diagonal if self.degreeofbullet<=90 else abs(1+self.diagonal))
            self.vertical=-abs((1)-(self.vertical)) if self.degreeofbullet>=100 else (random.choice(range[2:4]) if boss else 1)-self.vertical






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
        screen.blit(self.bullet_image,(self.rect.x,self.rect.y))
    def bullet_collide(self,enemy_count):

        if enemy_count.rect.colliderect(self.rect):
            if self.selected=="Bullet":
                enemy_count.damage(10)
            if self.selected=="High":
                enemy_count.damage(20)
            if self.selected=="aim":   
                enemy_count.damage(30 if not abilityselection.highcalibre else 50)




    def bullet_get_rect(self):
        return self.rect

from button_gamee import button_game




from dead_menu import death
ded=death(highscore,screen,replitbad,overall_sound,abilityselection,abilitydescription)


bulletlist=[]
bulletlistboss=[]
emplist=[]
shotgunlist=[]
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
        self.missilefirerate=self.collection[self.selected][4]
        self.bulletlist=bulletlist
        self.emplist=emplist
        self.shotgunlist=shotgunlist
        self.emp_tick=0

        self.health=self.collection[self.selected][3] if  not abilityselection.advanced() else self.collection[self.selected][3]*1.1

        self.sfont = pygame.font.SysFont("arialblack", 30, bold=False)


        if not replitbad:
            self.shoot=pygame.mixer.Sound("sound/hitHurt.wav")
            self.shoot.set_volume(overall_sound)
            self.death_sound=pygame.mixer.Sound("sound/DEATH.wav")
            self.death_sound.set_volume(overall_sound)
        self.iterative=0

        self.facing=360
        self.facing_opposite=-180

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

        self.revive_count=0
        self.revive_tick=0
        self.revive_cap=1


    def damage(self,damagetook):

            self.health-=damagetook
    def evolver(self):
        self.selected+=1 if self.selected+1<len(self.collection) else 0
        abilityselection.collectedabilities=[]
        abilityselection.reset()

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
            self.revive_tick=0

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
        global tick
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

        e=self.missiletick%self.missilefirerate==0 and (abilityselection.missilebarrage or self.collection[self.selected][0]=="F35")

        if abilityselection.emp and tick%100==0: # EMP

            self.emplist.append(emp(self.rect.x+self.playerplane.get_width()//2,self.rect.y+self.playerplane.get_height()//2,self.facing))

            if shop_contain.gunner_upgrade:
                self.emplist.append(emp(self.rect.x+self.playerplane.get_width()//2,self.rect.y+self.playerplane.get_height()//2,self.facing_opposite))

        if abilityselection.shotgun and tick%150==0:
            self.shotgunlist.append(shotgun_shoot(self.rect.x+self.playerplane.get_width()//2,self.rect.y+self.playerplane.get_height()//2,self.facing))
        
        if (pygame.key.get_pressed()[K_SPACE] and self.planetick%self.firerate==0 )and not(self.missiletick%self.missilefirerate==0 and abilityselection.missilebarrage):
            if not replitbad:
                self.shoot.play()

            self.bulletlist.append(bullet(bullets,self.rect.x+self.playerplane.get_width()//2 -10 if self.selected==1 else self.rect.x+self.playerplane.get_width()//2,self.rect.y+self.playerplane.get_height()//2 - 10 if self.selected == 1 else self.rect.y+self.playerplane.get_height()//2,self.facing,False if not self.collection[self.selected][0]=="F35" else True,False))


            if shop_contain.gunner_upgrade and self.selected==1:
                self.bulletlist.append(bullet(bullets,self.rect.centerx if self.selected==1 else self.rect.centerx,self.rect.centery if self.selected == 1 else self.rect.centery,self.facing,False if not self.collection[self.selected][0]=="F35" else True,False))
            if self.selected==1 or shop_contain.gunner_upgrade:
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
        self.emp_tick+=1


        if shop_contain.recovery_upgrade:
            self.health= self.health+1 if self.health <= (self.collection[self.selected][3] if not abilityselection.advanced() else self.collection[self.selected][3]*1.1) else self.health

        if abilityselection.kissoflife:
            if self.revive_tick==0:
                self.revive_count+=self.revive_cap
            self.revive_tick+=1
            if self.health<=0 and self.revive_count>=1:
                self.health=self.collection[self.selected][3]*0.75 if  not abilityselection.advanced() else (self.collection[self.selected][3]*1.1)*0.75
                abilityselection.reset()
                self.revive_count-=1
                listofenimies.clear()
                if not replitbad:
                    self.death_sound.play()
                
            print(self.revive_count)


        if self.health<=0:
            if self.iterative==0:
                if not replitbad:
                    self.death_sound.play()
                self.iterative+=1
            ded.message(highscore)
        








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
                            self.facing_opposite=-180 if self.facing==360 else 360 if self.facing == -180 else 270 if self.facing==-270 else -270
                        move_by=(keys[1]*1.5 if keys[1]>=0 else -abs(keys[1]*1.5)) if shop_contain.fuel_upgrade else keys[1]




                        if keys[2]=="u": # if player is moving vertical
                            self.constanty+=move_by if self.least<=self.constanty+move_by and self.constanty+move_by <= self.maxx else 0

                        else: # if player is moving diagonal
                            self.constantx+=move_by if self.least<=self.constantx+move_by and self.constantx+move_by <= self.maxx else 0



    def positionx(self):
        return self.x
    def positiony(self):
        return self.y



firstplane=player(playerplanes,x//2,y//2,collection)
playerplanes.add(firstplane)
propel=propeller_dispersion(firstplane.x,firstplane.y)



from enemy_ai import enemies
from enemy_ai import enemy




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

        self.biplane_health=130 if not shop_contain.hardmode_upgrade else 200
        self.tempest_health=500 if not shop_contain.hardmode_upgrade else 700
        self.harrier_health=1500 if not shop_contain.hardmode_upgrade else 2000
        self.beaufighter_health=10000 if not shop_contain.hardmode_upgrade else 15000


        if not replitbad:

            self.dead_enemy_sound=pygame.mixer.Sound("sound/dead_enemy.wav")
            self.dead_enemy_sound.set_volume(overall_sound)
    def enemyorbossupdate(self,list):
        global highscore,experience

        for enemycountter in islice(list,0,self.max_enemiesonscreen):
            if enemycountter.health > 0:
                if enemycountter.getposx() and enemycountter.getposy():
                    enemycountter.view()
                if not abilityselection.stillgetting() and list==listofenimies:
                    enemycountter.move_plane()
                elif enemycountter.collection[enemycountter.selected][0]=="beaufighter":
                    enemycountter.move_plane()
                    enemycountter.beaufighter_movement(bulletlistboss,bullet)

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
                experience+=(enemycountter.xpgain*3*1.25 if shop_contain.advanced_int_upgrade else enemycountter.xpgain*3 )if firstplane.selected<=3 else (enemycountter.xpgain*6*1.25 if shop_contain.advanced_int_upgrade else enemycountter.xpgain*6)
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
                    listofboss.append(enemy(enemies,x-100,y,bosscollection,self.beaufighter_health,0,0,500,screen,firstplane,abilityselection,bulletlistboss,tick,bosscollection)) # group,xx,yy,collection,health,selected,xpgain,firewait
                    self.bossalive=True
                if self.budget%30==0 and not self.bossalive: # harrier
                    listofenimies.append((enemy(enemies,x-100,y,enemycollection,self.harrier_health,2,50,None,screen,firstplane,abilityselection,bulletlistboss,tick,bosscollection)))
                    you_are_my_special=True
                if self.budget%10==0 and not self.bossalive: # tempest 



                    if sideortopside==0:
                        tempest_x=random.choice(self.listofspawnsx[0])-100
                        tempest_y=screen.get_height()//2+(random.randint(-screen.get_height()//2,screen.get_height()//2))
                    if sideortopside==1:
                        tempest_x=screen.get_width()//2+(random.randint(-screen.get_width()//2,screen.get_width()//2))
                        tempest_y=random.choice(self.listofspawnsy[0])-100
                    listofenimies.append((enemy(enemies,tempest_x-100,tempest_y,enemycollection,self.tempest_health,1,20,None,screen,firstplane,abilityselection,bulletlistboss,tick,bosscollection)))
                    you_are_my_special=True
                    self.budget-=4
                if self.budget!=0 and not you_are_my_special: #biplane

                    listofenimies.append((enemy(enemies,x-100,y,enemycollection,self.biplane_health,0,10,None,screen,firstplane,abilityselection,bulletlistboss,tick,bosscollection)))
                    self.budget-=2
        if self.listofnuke:
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

        for bullet in bulletlist: # NORMAL BULLET LOOP

            if bullet.x() and bullet.y():

                bullet.bullet_update()
                for l in islice(listofenimies,0,self.max_enemiesonscreen):
                    bullet.bullet_collide(l)
                if listofboss:
                    for boss in listofboss:
                        bullet.bullet_collide(boss)


            else:
                bulletlist.pop(bulletlist.index(bullet))

        #EMP LOOP
        for emp in emplist:
            if emp.kill:
                emplist.pop(emplist.index(emp))
            if 0<emp.rect.x<screen.get_width() and 0<emp.rect.y<screen.get_height():
                emp.image_get()
                for l in islice(listofenimies,0,self.max_enemiesonscreen):
                    if emp.explosion:
                        if l.rect.colliderect(emp.explosion_radius) and emp.explosion:
                            l.zapped=True
                            l.damage(1)
                            self.zapp_wait=l.tick+200
                    if l.rect.colliderect(emp.rect):
                        emp.explosion=True

                        l.damage(1)
                for boss in listofboss:
                    if boss.rect.colliderect(emp.explosion_radius) and emp.explosion:
                            boss.zapped=True
                            self.zapp_wait=boss.tick+200
                            boss.damage(1)
                    if boss.rect.colliderect(emp.rect):
                        emp.explosion=True
                        boss.damage(1)
            else:
                emplist.pop(emplist.index(emp))
        if abilityselection.shotgun:

            for shot in shotgunlist:
                if shot.reset_count>=1:
                    shotgunlist.pop(shotgunlist.index(shot))

                if 0<shot.rect.x<screen.get_width() and 0<shot.rect.y<screen.get_height():
                    shot.image_get()
                    for l in islice(listofenimies,0,self.max_enemiesonscreen):
                        if l.rect.colliderect(shot.rect):
                            l.damage(70)
                    for boss in listofboss:
                        if boss.rect.colliderect(shot.explosion_radius):
                            boss.damage(70)

                else:
                    shotgunlist.pop(shotgunlist.index(shot))
                

        if listofenimies:
            Round.enemyorbossupdate(listofenimies)
        if listofboss:
            Round.enemyorbossupdate(listofboss)

        if len(listofboss)==0:

            self.bossalive=False


        if self.tick%1500==0 and abilityselection.thefatman:
            from clouds_file import fatmannuke
            self.listofnuke.append(fatmannuke(firstplane.rect.x,firstplane.rect.y,firstplane.constantx,screen))
        if len(listofboss)==0 and not listofenimies or len(listofboss)==0 and self.tick%100==0:
            self.count+= 1
        if not abilityselection.stillgetting():
            self.tick+=1








Round=round()
p=paused(highscore,screen,abilityselection,replitbad,overall_sound)
from clouds_file import backdrop
while running:
    backdrop(tick,Round.nuke_detonation,screen,cloudsonscreen)
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

        if firstplane.health <=0 : 
            ded.highscore_check(event)

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
        p.draw(highscore)
        p.check()
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