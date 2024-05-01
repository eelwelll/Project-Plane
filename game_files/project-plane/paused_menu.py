import pygame

class paused:
    def __init__(self,highscore,screen,abilityselection) -> None:
        self.screen=screen
        self.abilityselection=abilityselection
        self.highscore=highscore
        # three variables needed because of the new file format that I am using
        self.sfont=pygame.font.SysFont("arialblack",100,bold=False)
        self.paused_text_behind=self.sfont.render("PAUSED",True,(0,0,0))
        self.paused_text=self.sfont.render("PAUSED",True,(255,255,255))
        
        self.score=self.sfont.render(f"score:{highscore}",True,(255,255,255))
    def draw(self,highscore):
        self.abilityselection.update_location()

        self.sfont=pygame.font.SysFont("arialblack",self.screen.get_height()//7,bold=False)
        self.paused_text_behind=self.sfont.render("PAUSED",True,(0,0,0))
        self.paused_text=self.sfont.render("PAUSED",True,(255,255,255))
        self.highscore=highscore
        self.score=self.sfont.render(f"score:{self.highscore}",True,(255,255,255))
        if not self.abilityselection.real:
            self.screen.blit(self.score,(self.abilityselection.bigbox.centerx-self.score.get_width()//2,self.abilityselection.bigbox.y))
            self.screen.blit(self.paused_text,(self.abilityselection.bigbox.centerx-self.paused_text.get_width()//2,self.abilityselection.bigbox.y+self.score.get_height()))
            #self.screen.blit(self.paused_text_behind,(self.abilityselection.bigbox.centerx-self.paused_text.get_width()//2-5,self.abilityselection.bigbox.centery-self.paused_text.get_height()//2))
