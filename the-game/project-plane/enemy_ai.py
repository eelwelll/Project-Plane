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
        self.enemy_sprite=pygame.image.load(f"D:/SteamLibrary/git_repo_projectplane/Project-Plane/the-game/Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png")


        self.facing=360
        self.facingindex=0
        #I hate that this is the solution to rotating the plane        
        self.angle=[(360,f"D:/SteamLibrary/git_repo_projectplane/Project-Plane/the-game/Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Forward.png"),(270,f"D:/SteamLibrary/git_repo_projectplane/Project-Plane/the-game/Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Left.png"),(-180,f"D:/SteamLibrary/git_repo_projectplane/Project-Plane/the-game/Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Down.png"),(-270,f"D:/SteamLibrary/git_repo_projectplane/Project-Plane/the-game/Planes/{self.collection[self.selected][0]}/{self.collection[self.selected][0]}-Facing-Right.png")]

        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.Surface((self.enemy_sprite.get_width(),self.enemy_sprite.get_height()))

        self.rect=self.image.get_rect()
        self.rect.center=xx,yy

    def view(self):
        self.tick+=1



        self.group.update()

        self.screen.blit(self.enemy_sprite,(self.x,self.y))
        if self.collection is self.bosscollection:
            self.health=self.health

            healthbarr_backdrop=pygame.Rect(14,self.screen.get_height()-26,self.screen.get_width()-30,22)
            pygame.draw.rect(self.screen,(0,0,0),(healthbarr_backdrop))
            healthbarr=pygame.Rect(15,self.screen.get_height()-25,(self.health/self.healthmax)*healthbarr_backdrop.width,20)

            pygame.draw.rect(self.screen,(255,0,0),(healthbarr))

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

    def move_plane(self):

        if not self.abilityselection.selecting:
            self.rect.x=self.rect.x+self.constantx
            self.rect.y=self.rect.y+self.constanty
            self.x=self.rect.x
            self.y=self.rect.y



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








        if not self.abilityselection.stillgetting():
            self.x+=self.constantx
            self.y+=self.constanty


        if self.rect.colliderect(self.firstplane.rect):
            self.firstplane.damage(10)

    def beaufighter_movement(self,bulletlistboss,bullet):
        #pygame.draw.circle(screen,(0,0,0),(screen.get_width()//2,screen.get_height()//2),screen.get_height()//3)
        '''boss make boss path around the player and shoot''' 
     
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
