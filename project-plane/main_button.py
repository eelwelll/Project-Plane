from typing import overload
import pygame
class button:
    def __init__(self,x,y,content,overall_sound,replitbad,screen) -> None:

        self.there=False
        self.content=content
        self.x,self.y=x,y
        self.rect=pygame.Rect((self.x,self.y), (content.get_width(),self.content.get_height()))
        self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
        self.placeholder=self.sfont.render("I",True,(255,255,255))
        if not replitbad:
            self.hover=pygame.mixer.Sound("sound/click.wav")
            self.hover.set_volume(overall_sound)

            self.selected=pygame.mixer.Sound(f"sound/clickonmenu.wav")

            self.selected.set_volume(overall_sound)
        self.hoveronce=False
        self.hovertick=0

        self.replitbad=replitbad
        self.overallsound=overall_sound
        self.screen=screen



    def text(self,x,y,content):
            self.x,self.y=x,y
            self.content=content
            self.rect=pygame.Rect((self.x,self.y), (self.content.get_width()+5,self.content.get_height()))
            mouse=pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(self.screen,(0, 195, 237),self.rect)


                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not self.replitbad:
                    if not self.replitbad:

                        self.hover.set_volume(self.overallsound)
                        self.selected.set_volume(self.overallsound)

                    self.hover.play()

                self.hovertick+=1


                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(self.screen,(0,137,167),self.rect)
            else:
                self.hoveronce=False
                self.hovertick=0

                pygame.draw.rect(self.screen,(0, 173, 212),self.rect)

            if pygame.display.get_init():
                self.screen.blit(self.content,self.rect)

    def check(self,objective):

        mouse=pygame.mouse.get_pos()
        #update it hopefully

        self.rect=pygame.Rect((self.x,self.y), (self.content.get_width(),self.content.get_height()))

        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if not self.replitbad:
                        self.selected.play()
                    pygame.draw.rect(self.screen,(0,137,167),self.rect)


                    objective()