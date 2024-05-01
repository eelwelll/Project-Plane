import pygame,random
class cloud:
    def __init__(self,y,least,most,screen,cloudsonscreen) -> None:
        self.screen=screen
        self.cloudsonscreen=cloudsonscreen

        self.cloud=pygame.image.load(f"Clouds/cloud-{random.randint(least,most)}.png")
        self.cloud_positionx=0-self.cloud.get_width()
        self.cloud_positiony=y


    def update(self):

        self.cloud_positionx=1+self.cloud_positionx


        self.screen.blit(self.cloud,(self.cloud_positionx,self.cloud_positiony))

    def nuked(self):
        pass

    def get_x(self):
        return True if self.cloud_positionx<self.screen.get_width() else False
fade=[0,166,201]
nuke_tint=[224, 151, 16]

def backdrop(tick,nuke,screen,cloudsonscreen):
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
            cloudsonscreen.append(cloud(random.randint(0,screen.get_height()),1,2,screen,cloudsonscreen))
        if tick%500==0:
            cloudsonscreen.append(cloud(random.randint(0,screen.get_height()),3,4,screen,cloudsonscreen))
        for theclouds in cloudsonscreen:
            if theclouds.get_x():
                theclouds.update()

            else:
                cloudsonscreen.pop(cloudsonscreen.index(theclouds))

            if nuke:
                theclouds.nuked()

class fatmannuke:
    def __init__(self,xx,yy,sideveloc,screen):
        self.screen=screen

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
        self.screen.blit(self.nuke_image,(self.rect.centerx,self.rect.centery))
    def explode(self):
        pass