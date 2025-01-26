import pygame
import math
import random
bullets=pygame.sprite.Group()

enemies=pygame.sprite.Group()
class enemy(pygame.sprite.Sprite):
    def __init__(self,group,xx,yy,collection,health,selected,xpgain,firewait,screen,firstplane,abilityselection,bulletlistboss,tick,bosscollection):
        self.screen=screen
        self.firstplane=firstplane
        self.abilityselection=abilityselection
        self.bulletlistboss=bulletlistboss
        self.tick=tick
        self.bosscollection=bosscollection
        
        
        
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

        self.zapped=False
        self.zapp_wait=0

        if self.collection[self.selected][0]=="hornet":
            from propeller_damage import propeller_dispersion
            self.propell=propeller_dispersion(self.rect.x,self.rect.y)
        self.dash=130
        self.dash_tick=0
        self.slow_tick=0
        self.savex,self.savey=0,0
        self.width=1

    def view(self):
        self.tick+=1



        self.group.update()

        self.screen.blit(self.enemy_sprite,(self.x,self.y))
        if self.collection is self.bosscollection:
            self.health=self.health
            sfont = pygame.font.SysFont("arialblack", 30, bold=False)

            self.name=sfont.render(self.bosscollection[self.selected][0],True,(255,255,255))
            
            healthbarr_backdrop=pygame.Rect(14,self.screen.get_height()-26,self.screen.get_width()-30,22)
            pygame.draw.rect(self.screen,(0,0,0),(healthbarr_backdrop))
            healthbarr=pygame.Rect(15,self.screen.get_height()-25,(self.health/self.healthmax)*healthbarr_backdrop.width,20)
            self.screen.blit(self.name,(healthbarr_backdrop.x,healthbarr_backdrop.y-self.name.get_height()-5))
            pygame.draw.rect(self.screen,(255,0,0),(healthbarr))
        if (self.constantx > self.maxx
            and self.constantx > 0) and self.dash_tick == self.tick:
                self.constantx = self.maxx
        if (self.constantx < self.least
            and self.constantx < 0) and self.dash_tick == self.tick:
                self.constantx = self.least
        if (self.constanty > self.maxx
            and self.constanty > 0) and self.dash_tick == self.tick:
                self.constanty = self.maxx
        if (self.constanty < self.least
            and self.constanty < 0) and self.dash_tick == self.tick:
                self.constanty = self.least

    def damage(self,damage_taken):
        self.health-=damage_taken





    def health_get(self):

        return True if int(self.health)>0 else False

    def getposx(self):
        return True if 0-self.enemy_sprite.get_width()<self.rect.x<self.screen.get_width() else False

    def getposy(self):
        return True if 0-self.enemy_sprite.get_height()<self.rect.y<self.screen.get_height() else False
    def get_plane(self):
        return self.collection[self.selected]

    def move_plane(self,pause,abilityselection,ded):

        if not self.abilityselection.selecting:
           
            self.rect.x=self.rect.x+self.constantx
            
            
            self.rect.y=self.rect.y+self.constanty
            self.x=self.rect.x
            self.y=self.rect.y

        if self.tick<=self.slow_tick or (self.tick==self.dash_tick-11 and self.health<self.healthmax/3):
            
            self.savex,self.savey=self.firstplane.rect.centerx,self.firstplane.rect.centery
            self.width=self.width+1 if self.width+1<=10 else 9
            if self.firstplane.rect.x<self.x:
                self.constantx=-1
            else:
                self.constantx=1
                
            if self.firstplane.rect.y<self.y:
                self.constanty=-1
               
            else:
                self.constanty=1
            if self.firstplane.rect.y-self.screen.get_width()//5<self.rect.centery<self.firstplane.rect.y+self.screen.get_width()//5:
                self.constanty=0
            if self.firstplane.rect.x-self.screen.get_height()//5<self.rect.centerx<self.firstplane.rect.x+self.screen.get_height()//5:
                self.constantx=0
            pygame.draw.line(self.screen,(255,00,00),(self.rect.centerx,self.rect.centery),(self.savex,self.savey),width=self.width)
        if self.tick==self.slow_tick+1 or self.tick==self.dash_tick-10 and self.health<self.healthmax/3:
            dash_mult=5
            self.width=1
            if self.constantx < 0:
                self.constantx = -abs(self.least * dash_mult)
            elif self.constantx != 0:
                self.constantx = self.maxx * dash_mult
            if self.constanty < 0:
                self.constanty = -abs(self.least * dash_mult)
            elif self.constanty != 0:
                self.constanty = self.maxx * dash_mult



        if self.facing!=self.angle[self.facingindex][0]:

                self.enemy_sprite=pygame.image.load(self.angle[self.facingindex][1])
                self.facing=self.angle[self.facingindex][0]


        if self.firstplane.rect.center[0] >= self.x+self.constantx and self.constantx<=self.maxx:
            self.constantx+=0.05
        elif self.firstplane.rect.center[0] <= self.x+self.constantx and self.constantx>=self.least:
            self.constantx-=0.05
        if self.firstplane.rect.center[1] >= self.y+self.constanty and self.constanty<=self.maxx:
            self.constanty+=0.05
        elif self.firstplane.rect.center[1] <= self.y+self.constanty and self.constanty>=self.least:

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


        if self.zapped:
            self.constantx,self.constanty=0,0
        if self.zapp_wait<self.tick:
            self.zapped=False




        


        if not self.abilityselection.stillgetting():
            if 0<self.x+self.constantx<self.screen.get_width():
                self.x+=self.constantx
            if 0<self.y+self.constanty<self.screen.get_height():
                self.y+=self.constanty
            


        if self.rect.colliderect(self.firstplane.rect)  and not pause and not abilityselection.stillgetting() and not ded.active:
            self.firstplane.damage(10)

    def beaufighter_movement(self,bulletlistboss,bullet):
        #pygame.draw.circle(screen,(0,0,0),(screen.get_width()//2,screen.get_height()//2),screen.get_height()//3)
        '''boss make boss path around the player and shoot''' 
        #if self.tick-20
        if self.tick%self.firewait==0:
            self.burst=True
            self.burst_tick=self.tick
        if self.burst_tick+self.firerate*5>=self.tick and self.tick%self.firerate==0:
            
            bulletlistboss.append(bullet(bulletlistboss,self.rect.centerx,self.rect.centery,self.facing,False,True))
        else:
            self.burst=False
        for bullet in bulletlistboss:
            if bullet.x() and bullet.y():
                bullet.bullet_update()
                bullet.bullet_collide(self.firstplane)

            else:
                bulletlistboss.pop(bulletlistboss.index(bullet))
    def spawn_enemy_horde(self,listofenimies,screen,enemycollection):
        
            listofspawnsx = [(1, screen.get_width() + 200)]
            listofspawnsy = [(-10, screen.get_height() + 200)]
            sideortopside = random.randint(0, 1)
            if sideortopside == 0:
                x = random.choice(listofspawnsx[0]) - 100
                y = screen.get_height() // 2 + (random.randint(
                    -screen.get_height() // 2,
                    screen.get_height() // 2))
            if sideortopside == 1:
                x = screen.get_width() // 2 + (random.randint(
                    -screen.get_width() // 2,
                    screen.get_width() // 2))
                y = random.choice(listofspawnsy[0]) - 100
            listofenimies.append(
                (enemy(enemies, x - 100, y, enemycollection,
                       70, 3, 10, None, screen,
                       self.firstplane, self.abilityselection, self.bulletlistboss,
                       self.tick, self.bosscollection)))
    def propel(self):
        self.propell.image_get(self.rect.x,self.rect.y,True,self.tick,self.screen)
        if self.propell.rect.colliderect(self.firstplane.rect):
            self.firstplane.damage(5)
        if self.dash>=100:

            self.dash = 0
            dash_mult = 5
            self.slow_tick=self.tick + 45
            self.dash_tick = self.tick + 80

            if self.constantx < 0:
                self.constantx = -abs(self.least * dash_mult)
            elif self.constantx != 0:
                self.constantx = self.maxx * dash_mult
            if self.constanty < 0:
                self.constanty = -abs(self.least * dash_mult)
            elif self.constanty != 0:
                self.constanty = self.maxx * dash_mult
        else:
            self.dash+=1
        
        
    