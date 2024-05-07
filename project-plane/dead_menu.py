import pygame
import os
class death:
    def __init__(self,highscore,screen,button,replitbad,overallsound,abilityselection,abilitydescription):
       

        self.boarder=pygame.Rect(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)

        self.move=False
        self.sfont = pygame.font.SysFont("arialblack", 50, bold=False)
        self.death_back=self.sfont.render("YOU DIED",True,(0,0,0))
        self.death_forward=self.sfont.render("YOU DIED",True,(255,0,0))
        self.highscore=highscore
        self.high=self.sfont.render(f"score:{highscore}",True,(255,255,255))
        self.mainmenu=self.sfont.render("main menu",True,(255,255,255))
        self.screen=screen
        self.menu=button(self.boarder.centerx-self.mainmenu.get_width()//2,screen.get_height()//2+self.boarder.y,self.mainmenu,replitbad,overallsound,screen,abilityselection,abilitydescription)
        coin=0
        self.coins_gotten=""
        coins_have=open("how_many_coins.csv","r+")
        for lines in coins_have:
                coin=int(lines)
                coins_have.truncate()
                coin=str(coin+(self.highscore//100))
                self.coins_gotten=f"{coin} + {self.highscore/100}"
                
                coins_have=open("how_many_coins.csv","w")
                coins_have.write(coin)
        self.image_of_coin=pygame.image.load("menu-item/coin.png")
        self.coins=self.sfont.render(f"{self.coins_gotten}",True,(255,255,255))
        print(self.highscore)
        

    def message(self,highscore):
        self.highscore=highscore
        coin=0
        self.coins_gotten=""
        coins_have=open("how_many_coins.csv","r+")
        for lines in coins_have:
                coin=int(lines)
                coins_have.truncate()
                coin=str(coin+(self.highscore//100))
                self.coins_gotten=f"{coin} + {self.highscore//100}"
                
                coins_have=open("how_many_coins.csv","w")
                coins_have.write(coin)
        self.image_of_coin=pygame.image.load("menu-item/coin.png")
        self.coins=self.sfont.render(f"{self.coins_gotten}",True,(255,255,255))
        print(self.highscore)
        self.boarder.update(self.screen.get_width()//4,self.screen.get_height()//4,self.screen.get_width()//2,self.screen.get_height()//2)
        pygame.draw.rect(self.screen,(0,130,149),self.boarder)
        self.screen.blit(self.death_back,(self.boarder.centerx-self.death_back.get_width()//2,self.boarder.centery/2))
        self.screen.blit(self.death_forward,(self.boarder.centerx+5-self.death_back.get_width()//2,self.boarder.centery/2))

        self.menu.text(None,None,None,None,None)
        self.screen.blit(self.high,(self.boarder.centerx-self.high.get_width()//2,self.boarder.centery/2+self.death_forward.get_height()))
        self.screen.blit(self.coins,(self.boarder.centerx-self.coins.get_width()//2+self.image_of_coin.get_width(),self.boarder.centery/2+self.death_forward.get_height()+self.high.get_height()))
        self.screen.blit(self.image_of_coin,(self.boarder.centerx-self.coins.get_width()//2,self.boarder.centery/2+self.death_forward.get_height()+self.high.get_height()))
        def quit():
            
            pygame.display.quit()
            os.system("python project-plane/main.py")
        self.menu.check(lambda: quit())