import pygame
import os
class death:
    def __init__(self,highscore,screen,replitbad,overallsound,abilityselection,abilitydescription):
       

        self.boarder=pygame.Rect(screen.get_width()//4,screen.get_height()//4,screen.get_width()//2,screen.get_height()//2)

        self.move=False
        self.sfont = pygame.font.SysFont("arialblack", 50, bold=False)
        self.death_back=self.sfont.render("YOU DIED",True,(0,0,0))
        self.death_forward=self.sfont.render("YOU DIED",True,(255,0,0))
        self.highscore=highscore
        self.high=self.sfont.render(f"score:{highscore}",True,(255,255,255))
        self.mainmenu=self.sfont.render("main menu",True,(255,255,255))
        self.screen=screen
        from main_button import button
        self.menu=button(self.boarder.centerx-self.mainmenu.get_width()//2,screen.get_height()//2+self.boarder.y,self.mainmenu,overallsound,replitbad,screen)
        coin=0
        self.coins_gotten=""
        coins_have=open("how_many_coins.csv","r+")
        for lines in coins_have:
                coin=int(lines)
                coins_have.truncate()
                self.coins_gotten=f"{coin} + {self.highscore/100}"
                coin=str(coin+(self.highscore//100))
                
                coins_have=open("how_many_coins.csv","w")
                coins_have.write(coin)
        self.image_of_coin=pygame.image.load("menu-item/coin.png")
        self.coins=self.sfont.render(f"{self.coins_gotten}",True,(255,255,255))
        self.image_of_coin=pygame.transform.scale(self.image_of_coin,(self.coins.get_width(),self.coins.get_height()))
        self.tick=0

        #highscore
        self.highscore_box_there=True
        from write_button import write
        self.name_getter=self.sfont.render("enter your name:",True,(255,255,255))
        
        self.highscore_name=write(screen.get_width()//2-50,screen.get_height()//2,self.name_getter,"",screen)
        

    def message(self,highscore):
        self.highscore=highscore
      
        
        coins_have=open("how_many_coins.csv","r+")
        self.high=self.sfont.render(f"score:{highscore}",True,(255,255,255))
        
        if self.tick==0:
            for lines in coins_have:
                self.coins_gotten=0
                coin=int(lines)
                coins_have.truncate()
                coin=str(coin+(self.highscore//10))
                self.coins_gotten=f"{coin} + {self.highscore//10}"              
                coins_have=open("how_many_coins.csv","w")
                coins_have.write(coin)
        self.tick+=1
        self.image_of_coin=pygame.image.load("menu-item/coin.png")
        
        self.coins=self.sfont.render(f"{self.coins_gotten}",True,(255,255,255))
        self.image_of_coin=pygame.transform.scale(self.image_of_coin,(self.image_of_coin.get_width()//3,self.coins.get_height()))
        self.boarder.update(self.screen.get_width()//4,self.screen.get_height()//4,self.screen.get_width()//2,self.screen.get_height()//2)
        pygame.draw.rect(self.screen,(0,130,149),self.boarder)
        self.screen.blit(self.death_back,(self.boarder.centerx-self.death_back.get_width()//2,self.boarder.centery/2))
        self.screen.blit(self.death_forward,(self.boarder.centerx+5-self.death_back.get_width()//2,self.boarder.centery/2))

        self.menu.text(self.boarder.centerx-self.mainmenu.get_width()//2,self.screen.get_height()//2+self.boarder.y)
        self.screen.blit(self.high,(self.boarder.centerx-self.high.get_width()//2,self.boarder.centery/2+self.death_forward.get_height()))
        self.screen.blit(self.coins,(self.boarder.centerx-self.coins.get_width()//2+self.image_of_coin.get_width(),self.boarder.centery/2+self.death_forward.get_height()+self.high.get_height()))
        self.screen.blit(self.image_of_coin,(self.boarder.centerx-self.coins.get_width()//2,self.boarder.centery/2+self.death_forward.get_height()+self.high.get_height()))
        
        self.screen.blit(self.name_getter,(self.screen.get_width()//2-self.name_getter.get_width()//2,self.screen.get_height()//2-self.highscore_name.h//2+20))
        self.highscore_name.text(self.screen.get_width()//2-50,self.screen.get_height()//2+30)
        
        def quit():
            
            pygame.display.quit()
            highscore_list=[]
            with open ("highscore.csv","r") as highscore_file:
                highscore_file=highscore_file.read().splitlines()
                for lines in highscore_file:
                    lines=lines.split(",")
                    highscore_list.append((lines[0],lines[1]))
                index=0
                there=False
                iteration=0
                for pos,lines in enumerate(highscore_list):
                    num=0
                    iteration+=1
                    if iteration>1:
                        num=int(lines[1])
                        
                    if there:
                        break
                    if num>self.highscore:
                        index=pos
                    if num<self.highscore:
                        highscore_list.insert(pos+1,(self.highscore_name.words,self.highscore))
                        there=True
                    
                    print(num,pos,lines,highscore_list)
                if not there:
                    highscore_list.append((self.highscore_name.words,self.highscore))
            print(highscore_list)
            with open("highscore.csv","w") as highscore_file:
                total=""
                for lines in highscore_list:
                    
                    total+=f"{lines[0]},{lines[1]}\n"
                highscore_file.write(total)
                    
                
                    
                    
                
                
            os.system("python project-plane/main.py")
        self.menu.check(lambda: quit())

    def highscore_check(self,event):
            self.highscore_name.writer(None,event)


'''PUT HIGHSCORE WINDOW IN HERE, but not now as I need to do comp sci work lol'''