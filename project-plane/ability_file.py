import pygame
class propeller_dispersion:
    def __init__(self,xx,yy):
        self.frame=pygame.image.load("prop/propeller-0.png")
        self.rect=self.frame.get_rect()
        self.frameon=0
        self.rect.center=xx,yy
        self.x,self.y=xx-10,yy
        self.rect=self.rect.inflate(self.frame.get_width()*3,self.frame.get_height()*3)
        self.cooldown=True
    def image_get(self,tick,firstplane,screen):
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
    def image_get(self,tick,screen):
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
    def __init__(self,xx,yy,facing,firstplane) -> None:
        self.frameon=0
        self.frame=pygame.image.load(f"shotgun_sprite_sheet/shotgun_shot-{self.frameon}.png")
        self.frame=pygame.transform.scale_by(self.frame,4)
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
        self.xx,self.yy=xx,yy
        self.rect.centerx,self.rect.centery=xx+(-abs(self.diagonal*firstplane.rect.w*2) if self.diagonal<0 else self.diagonal*firstplane.rect.w+firstplane.rect.w),yy+(-abs(self.vertical*firstplane.rect.h*2) if self.vertical<0 else self.vertical*firstplane.rect.h*2)
        if self.diagonal==0:
            self.rect.x-=firstplane.rect.w

    def image_get(self,tick,screen):
        screen.blit(self.frame,(self.rect.x,self.rect.y))
        #pygame.draw.rect(screen,(255,255,255),self.rect)
        if tick%4==0:
            self.frameon=self.frameon+1 if self.frameon+1<6 else 0
            self.reset_count+=1 if self.frameon==5 else 0

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
        self.frame=pygame.transform.scale_by(self.frame,4)

