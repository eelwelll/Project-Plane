import pygame
class death:
    def __init__(self,highscore,screen,button,replitbad,overallsound,abilityselection,abilitydescription):
        global highsore

        self.boarder=pygame.Rect(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)

        self.move=False
        self.sfont = pygame.font.SysFont("arialblack", 100, bold=False)
        self.death_back=self.sfont.render("YOU DIED",True,(0,0,0))
        self.death_forward=self.sfont.render("YOU DIED",True,(255,0,0))
        self.high=self.sfont.render(f"score:{highscore}",True,(255,255,255))
        self.mainmenu=self.sfont.render("main menu",True,(255,255,255))
        self.screen=screen
        self.menu=button(self.boarder.centerx-self.mainmenu.get_width()//2,screen.get_height()//2+self.boarder.y,self.mainmenu,replitbad,overallsound,screen,abilityselection,abilitydescription)
    def message(self):
        self.boarder.update(self.screen.get_width()//4,self.screen.get_height()//4,self.screen.get_width()//2,self.screen.get_height()//2)
        pygame.draw.rect(self.screen,(0,130,149),self.boarder)
        self.screen.blit(self.death_back,(self.boarder.centerx-self.death_back.get_width()//2,self.boarder.centery/2))
        self.screen.blit(self.death_forward,(self.boarder.centerx+5-self.death_back.get_width()//2,self.boarder.centery/2))

        self.menu.text(None,None,None,None,None)
        self.screen.blit(self.high,(self.boarder.centerx-self.high.get_width()//2,self.boarder.centery))
        self.menu.check(lambda: self.menu.returnmm())