import pygame, sys , os
class button:
    def __init__(self,x,y,content,replitbad,overallsound,screen,abilityselection,abilitydescription):
        self.repl=replitbad
        self.sound=overallsound
        self.screen=screen
        self.ability=abilityselection
        self.des=abilitydescription
        
        self.there=False
        self.content=content
        self.x,self.y=x,y
        self.rect=pygame.Rect((self.x,self.y), (content.get_width() if content.get_width()>100 else 100,content.get_height()))
        if not replitbad:
            self.hover=pygame.mixer.Sound("sound/click.wav")
            self.hover.set_volume(self.sound)
            self.selected=pygame.mixer.Sound("sound/selectabil.wav")
            self.selected.set_volume(self.sound)
        self.hoveronce=False
        self.hovertick=0
    def text(self,ability,bigbox,anumber,textbox,evolve):

            self.rect=pygame.Rect((self.x,self.y), (self.content.get_width() if self.content.get_width()>100 else 100,self.content.get_height()))

            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(self.screen,(0, 195, 237),self.rect)
                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not self.repl:
                    self.hover.play()

                self.hovertick+=1
                if ability:
                    e=pygame.image.load(f"abilities/{ability}.gif")

                    text=pygame.font.SysFont("arialblack",self.ability.bigbox.w//40)
                    ability_image=pygame.transform.scale_by(e,self.ability.bigbox.w//(e.get_width()*4))


                    toptext=""
                    bottomtext=""
                    if not evolve:
                        for numbers,letters in enumerate(self.des[anumber]):

                            if letters=="^":


                                toptext=self.des[anumber][:numbers]
                                bottomtext=self.des[anumber][numbers+1:]

                    dave=text.render(f"{toptext}",True,(255,255,255))
                    pygame.draw.rect(self.screen,(0,137,167),textbox)
                    self.screen.blit(dave,(textbox[0],bigbox[1]+ability_image.get_height()+30))
                    self.screen.blit(text.render(f"{bottomtext}",True,(255,255,255)),(textbox[0],bigbox[1]+ability_image.get_height()+dave.get_height()+30))
                    self.screen.blit(ability_image,bigbox)
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(self.screen,(0,137,167),self.rect)
            else:
                self.hoveronce=False
                self.hovertick=0
                pygame.draw.rect(self.screen,(0, 173, 212),self.rect)

            if pygame.display.get_init():
                self.screen.blit(self.content,self.rect)

    def check(self,objective):
        global mouse
        mouse=pygame.mouse.get_pos()
        #update it hopefully
        self.rect=pygame.Rect((self.x,self.y), (self.content.get_width() if self.content.get_width()>100 else 100,self.content.get_height()))
        #
        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if not self.repl:
                        self.selected.play()
                    pygame.draw.rect(self.screen,(0,137,167),self.rect)


                    objective()
    def returnmm(self):
        pygame.display.quit()
        os.system("python main.py")
        sys.exit()

    def select_ability(self,ability,gottenability,select):
        select

        gottenability.append(ability)