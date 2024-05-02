import random
import sys
import os
import pygame
import csv
import pandas as pd


projecticon=pygame.image.load("Planes/F22/F22-Facing-Forward.png")
pygame.display.set_caption("project plane")
pygame.display.set_icon(projecticon)
pygame.font.init()
replitbad=False


if not replitbad:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)
  # Initializes pygame module
x, y =1300,500
xx,yy=x,y
accel=1
movement=[["w",-abs(accel),"u"],["a",-abs(accel),"di"],["s",accel,"u"],["d",accel,"di"]]
moveup,moveleft,movedown,moveright=movement[0],movement[1],movement[2],movement[3]
overall_sound=0.25
screen = pygame.display.set_mode((x, y),pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True  # Boolean to control the game loop
level = 0


'''for buttons to type in, mainly used in the settings'''
'''unless I use a drop down menu'''
class write:
    def __init__(self,xx,xy,content,word):
        self.yx,self.yy=xx,xy
        self.diff=content.get_width()
        screen.blit(content,(xx,xy))
        self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
        self.words=word
        self.context=self.sfont.render(self.words,True,(255,255,255))
        self.rect=pygame.Rect((self.yx+self.diff,self.yy),(self.context.get_width() if self.context.get_width() > 100 else 100,44))


    def text(self):  
            self.rect=pygame.Rect((self.yx+self.diff,self.yy),(self.context.get_width() if self.context.get_width() > 100 else 100,44))

            pygame.draw.rect(screen,(0,173,212),self.rect)

            self.context=self.sfont.render(self.words,True,(255,255,255))
            screen.blit(self.context,self.rect)

    def writer(self,event,objective):

        if event.type == pygame.KEYDOWN and self.rect.collidepoint(mouse):
                if event.key == pygame.K_BACKSPACE:
                    self.words=self.words[:-1]
                elif event.key==pygame.K_RETURN:

                    objective()
                elif len(self.words)<=10:
                    self.words+=  event.unicode
    def change_res(self,event):
             global x,y
             #BIT THAT IS UNIQUE THE RESOLUTION
             newx,newy='',''

             change=False
             for l in range(len(self.words)):
                if self.words[l].lower() == 'x' and change is False:
                    change = True
                if self.words[l]=="x":
                    continue
                if not change:
                    newx += str(self.words[l])
                else:
                    newy += str(self.words[l])
             pygame.display.set_mode((int(newx),int(newy)),pygame.RESIZABLE)
             x,y=int(newx),int(newy)


    def change_movement(self,event):
        global moveup,movedown,moveleft,moveright,movement
        count=0
        if event.key == pygame.K_RETURN:
            for l in range(0,len(self.words),2):
                movement[count]=self.words[l]
                count+=1

'''dropdown menu button, mainly used in settings menu and changing plane :D'''

class dropdown:
    def __init__(self,xx,yy,content) -> None:
        self.posx,self.posy=xx,yy
        self.orig=content
        self.content=content
        self.x,self.y=xx,yy
        self.chosen=''
        self.toggle=False
        self.sfont = pygame.font.SysFont("arialblack", screen.get_height()//20, bold=False)

        self.placeholder=self.sfont.render("I",True,(255,255,255))
        self.new=pygame.Rect((self.x,self.y),(self.content.get_width(),self.content.get_height()))
        self.square=pygame.Rect((self.x,self.y),(self.content.get_width(),self.content.get_height()))




    def view(self):
        self.content=self.orig

        self.sfont = pygame.font.SysFont("arialblack", screen.get_height()//20, bold=False)
        pygame.draw.rect(screen,(0,173,212),self.square)
        self.square=pygame.Rect((self.x,self.y),(self.content.get_width(),self.content.get_height()))
        screen.blit(self.content,(self.posx,self.posy))


    def drop(self,file,change):
        global y
        r=self.content.get_height()+5
        dropper=open(f"{file}.csv","r").read().splitlines()

        for line in dropper:

            if self.y+r+self.content.get_height()<screen.get_height():
                drop=self.sfont.render(line,True,(255,255,255))
            else:
                drop=self.sfont.render("...",True,(255,255,255))
            new=pygame.Rect((self.x,self.y+r),(drop.get_width(),drop.get_height()))
            pygame.draw.rect(screen,(0,173,212),new)

            if new.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                self.chosen=line
                if change:
                    change()
                    #updating bit
                    self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
                    self.new=pygame.Rect((self.x,self.y+10),(drop.get_width(),drop.get_height()))
                    self.square=pygame.Rect((self.x,self.y+10),(drop.get_width(),drop.get_height()))



            screen.blit(drop,(self.x,self.y+r))
            r+=new.h+5



    def check(self,objective):

        if self.toggle:
            objective()

        if objective and self.square.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            self.toggle=True

        if objective and not self.square.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:

            self.toggle=False


    def change_res(self):
             global x,y
             #BIT THAT IS UNIQUE THE RESOLUTION
             newx,newy='',''
             change=False
             for l in range(len(self.chosen)):
                if self.chosen[l].lower() == 'x' and change == False:
                    change = True
                if self.chosen[l]=="x":
                    continue
                if not change:
                    newx += str(self.chosen[l])
                else:
                    newy += str(self.chosen[l])
             pygame.display.set_mode((int(newx),int(newy)),pygame.RESIZABLE)
             x,y=int(newx),int(newy)
    def change_control(self):
        global moveup,movedown,moveleft,moveright,movement
        l=0
        itterval=0
        value=[-1,"u",-1,"di",1,"u",1,"di",1,"u"]
        for control in range(len(movement)):
            movement[control]=[self.chosen[l],value[itterval],value[itterval+1]]
            l+=2
            itterval+=2


'''slider for sliding (mainly for volume :D)'''

class slider:
    def __init__(self,xx,xy,content):
        self.content=content
        self.x,self.y=xx+content.get_width()+30,xy
        self.adjust=15
        self.line=pygame.Rect((self.x,self.y+25),(100,10))
        self.sliderr=pygame.Rect((self.x+85,self.y+self.adjust),(14,30))
        self.max=pygame.Rect((self.x+100,self.y+25),(10,10))
        self.least=pygame.Rect((self.x-10,self.y+25),(10,10))
        if not replitbad:
            self.soundeffect=pygame.mixer.Sound("sound/synth.wav")
        self.value=self.sliderr[0]-self.line[0]

        self.held=0
    def view(self):
        screen.blit(self.content,(self.x-self.content.get_width()-30,self.y))
        pygame.draw.rect(screen,(0,173,212),self.line)
        pygame.draw.rect(screen,(0,173,212),self.sliderr)
        pygame.draw.rect(screen,(255,255,255),self.max)
        pygame.draw.rect(screen,(255,255,255),self.least)
    def volumer(self,event):
            global overall_sound
            overall_sound=self.value/100

            if not replitbad:
                self.soundeffect.set_volume(self.value/100 if self.value/100<1 else 0.5)

                self.soundeffect.play() if self.line.collidepoint(mouse) and pygame.mouse.get_pressed()[0] else 0

    def check(self,objective,event):
        e=pygame.mouse.get_pressed()[0] and not self.sliderr.colliderect(self.max or self.least)
        if self.sliderr.collidepoint(mouse) and e or self.line.collidepoint(mouse) and e:

                    self.sliderr=pygame.Rect((mouse[0]-7,self.y+self.adjust),(14,30))


        if self.sliderr.colliderect(self.max):
            self.sliderr=pygame.Rect((self.x+86,self.y+self.adjust),(14,30))

        if self.sliderr.colliderect(self.least):
            self.sliderr=pygame.Rect((self.x,self.y+self.adjust),(14,30))
        self.value=self.sliderr[0]-self.line[0]

        if objective:
            objective()








'''button.'''
class button:
    def __init__(self,x,y,content) -> None:

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


    def text(self,x,y):
            self.x,self.y=x,y
            self.rect=pygame.Rect((self.x,self.y), (self.content.get_width()+5,self.content.get_height()))

            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(screen,(0, 195, 237),self.rect)


                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not replitbad:
                    if not replitbad:

                        self.hover.set_volume(overall_sound)
                        self.selected.set_volume(overall_sound)

                    self.hover.play()

                self.hovertick+=1


                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(screen,(0,137,167),self.rect)
            else:
                self.hoveronce=False
                self.hovertick=0

                pygame.draw.rect(screen,(0, 173, 212),self.rect)

            if pygame.display.get_init():
                screen.blit(self.content,self.rect)

    def check(self,objective):
        global mouse
        mouse=pygame.mouse.get_pos()
        #update it hopefully

        self.rect=pygame.Rect((self.x,self.y), (self.content.get_width(),44))
        #
        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if not replitbad:
                        self.selected.play()
                    pygame.draw.rect(screen,(0,137,167),self.rect)


                    objective()

class shop_button:
    def __init__(self,x,y,content,image,description,gotten,cost,actual_name) -> None:

        self.there=False
        self.content=content
        self.what=actual_name
        self.x,self.y=x,y
        self.image_name=image
        self.gotten=gotten
        self.colour=(247, 104, 104) if self.gotten else (0, 195, 237) # left == red icba to reverse this so im leaving these notes here
        self.colour_again=(0, 173, 212) if not self.gotten else (219, 29, 29) # right sie == red , left side == blue
        self.image=pygame.image.load(image)
        self.rect=pygame.Rect((self.x,self.y), (content.get_width(),self.content.get_height()))
        self.sfont = pygame.font.SysFont("arialblack", 25, bold=False)
        self.change=0
        self.cost_number=int(cost)
        self.cost=self.sfont.render(cost,True,(255,255,255))
        original=pygame.image.load("menu-item/coin.png")
        self.coin=pygame.transform.scale(original,(self.cost.get_height(),self.cost.get_height()))        
        self.placeholder=self.sfont.render("___________",True,(255,255,255))
        self.desc_get_text=description
        self.desc_text=[]
        self.coll=0

        self.description=self.sfont.render(description,True,(255,255,255))
        self.text_box_description=pygame.Rect((screen.get_width()//1.5,Shop.description_wall.y+self.content.get_height()+10+self.image.get_height()),(screen.get_width()//2.5,Shop.description_wall.h-self.content.get_height()+10+self.image.get_height()))


        if not replitbad:
            self.hover=pygame.mixer.Sound("sound/click.wav")

            self.selected=pygame.mixer.Sound("sound/clickonmenu.wav")
            self.openshop=pygame.mixer.Sound("sound/shop_open.wav")



            self.openshop.set_volume(overall_sound)

            self.hover.set_volume(overall_sound)
            self.selected.set_volume(overall_sound)
        self.hoveronce=False
        self.hovertick=0
    def description_newline_get(self):
        last_let_place=0
        height=self.description.get_height()
        self.desc_text.clear()
        word=0
        space=" "
        end=False
        let=0
        previous_word=0
        while let!=len(self.desc_get_text):


            if let+1<len(self.desc_get_text):
                let_get=self.desc_get_text[let+1]
                word+=1
            else:
                let_get=self.desc_get_text[let]
            end=True if let_get == "." else False


            if self.desc_get_text[let]==space:
                previous_word=word
                word=0
            if (pygame.font.Font.size(self.sfont,self.desc_get_text[last_let_place:let])[0])>=self.text_box_description.w-self.text_box_description.w//4:
                if not end:
                    let-=word
                    des=let if let_get == space else let
                    self.desc_text.append((self.desc_get_text[last_let_place:des],self.text_box_description.y+5+self.image.get_height()+(height*len(self.desc_text))))

                    last_let_place=des

            if end:
                    des=let if let_get == space else (-previous_word)
                    self.desc_text.append((self.desc_get_text[last_let_place:des],self.text_box_description.y+5+self.image.get_height()+(height*len(self.desc_text))))
                    last_let_place=des


            let+=1


    def text(self,x,y):
            self.x,self.y=x,y
            self.colour=(247, 104, 104) if self.gotten else (0, 195, 237) # left == red icba to reverse this so im leaving these notes here
            self.colour_again=(0, 173, 212) if not self.gotten else (219, 29, 29) # right sie == red , left side == blue
            self.rect=pygame.Rect((self.x,self.y), (self.content.get_width()+5,self.content.get_height()+self.image.get_height()))
            self.text_box_description=pygame.Rect((screen.get_width()//1.5,Shop.description_wall.y+self.content.get_height()+10+self.image.get_height()),(screen.get_width()//2.5,Shop.description_wall.h-self.content.get_height()+10+self.image.get_height()))

            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(screen,(self.colour),self.rect)
                screen.blit(self.content,(Shop.description_wall.x,Shop.description_wall.y))
                screen.blit(self.cost,(Shop.description_wall.x+self.coin.get_width(),Shop.description_wall.y+self.content.get_height()))
                screen.blit(self.coin,(Shop.description_wall.x,Shop.description_wall.y+self.content.get_height()))
                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not replitbad:

                        self.hover.set_volume(overall_sound)
                        self.selected.set_volume(overall_sound)
                        self.hover.play()


                descimage=pygame.transform.scale_by(self.image,3)
                screen.blit(descimage,(Shop.description_wall.centerx-descimage.get_width(),Shop.description_wall.y+self.content.get_height()+10))
                for lines in self.desc_text:
                    screen.blit(self.sfont.render(f"{lines[0]}",True,(255,255,255)),(self.text_box_description.x,lines[1]))



                self.hovertick+=1




            else:
                self.hoveronce=False
                self.hovertick=0

                pygame.draw.rect(screen,self.colour_again,self.rect)

            if pygame.display.get_init() and self.image:
                screen.blit(self.image,(self.rect.centerx-self.image.get_width(),self.rect.centery-self.image.get_height()))
                screen.blit(self.content,(self.rect.x,self.rect.y+self.content.get_height()//1.75))


    def check(self,objective,position):
        global mouse
        mouse=pygame.mouse.get_pos()
        #update it hopefully


        #
        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if (self.hoveronce and self.hovertick==0) and not replitbad:
                        self.selected.play()


                    if self.gotten:
                            coins_have=open("how_many_coins.csv","r+")
                            
                            
                            if not replitbad:
                                self.openshop.play()
                            for lin in (coins_have):
    
                                if int(lin)>=self.cost_number:
                                    temp=int(lin)-self.cost_number

                                    coins_have=open("how_many_coins.csv","w")
                                    coins_have.write(f"{temp}")
                                    coins_have.close()
                                    shopper=open("shop_contain.csv","r").read().splitlines()
                                    shopy=csv.reader(shopper, delimiter = ",")
                                    shop_get_list=list(shopy)
                                    for col_num,row in enumerate(shopy):
                                        print(row[0] ,self.what)
                                        if row[0] == self.what:
                                            self.coll=col_num
                                            print(col_num)
                                    print(shop_get_list[self.coll])
                                        #replacing_content=f"{self.what},{self.image_name},{self.desc_get_text},True,{self.cost}"

                                    
                                    
                                        



                            self.gotten=False

class shoop:
    def __init__(self):

        self.bgcolour=((0,157,181))
        self.white=(255,255,255)
        self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
        self.back=self.sfont.render("back",True,self.white)
        self.back_button = button(screen.get_width()-10,screen.get_height()-10,self.back)
        self.tick=0
        self.listofitems=[]
        self.line_background_list=[background_speed(x,y,0+screen.get_width()//3),background_speed(x,y,0+screen.get_width()//2),background_speed(x,y,0+screen.get_width()-10)]
        self.line_y=0
        self.description_wall=pygame.Rect(screen.get_width()/1.5,0,screen.get_width()/2.5,screen.get_height()-self.back.get_height()-20)
        self.scroll_line=pygame.Rect((screen.get_width()/1.5-self.description_wall.w//3,2),(screen.get_width()/100,screen.get_height()//10))
        self.scroll_line_backgroup=pygame.Rect((screen.get_width()/1.5-self.description_wall.w//3,2),(screen.get_width()/100,screen.get_height()//self.description_wall.h))
        self.coins=0
        self.cost=self.sfont.render(f"{self.coins}",True,self.white)
        original=pygame.image.load("menu-item/coin.png")
        self.coin=pygame.transform.scale(original,(self.cost.get_height(),self.cost.get_height())) 

        if not replitbad:
            self.openshop=pygame.mixer.Sound("sound/shop_open.wav")



            self.openshop.set_volume(overall_sound)




    def shop_create(self):
        coins_have=open("how_many_coins.csv","r").read().splitlines()
        for coin in coins_have:
            self.coins=coin

        self.cost=self.sfont.render(f"{self.coins}",True,self.white)


        global level
        level=1
        self.description_wall=pygame.Rect(screen.get_width()/1.5,0,screen.get_width()/2.5,screen.get_height()-self.back.get_height()-20)
        self.scroll_line_backgroup=pygame.Rect((screen.get_width()/1.5-screen.get_width()/100-2,2),(screen.get_width()/100,self.description_wall.h-2))
        self.scroll_line=pygame.Rect((screen.get_width()/1.5-screen.get_width()/100-2,2),(screen.get_width()/100,screen.get_height()//10))

        if self.tick==0:
            Shop.shop_maker()
            if not replitbad:
                self.openshop.play()
        screen.fill(self.bgcolour)

        for background_lines in self.line_background_list:
            background_lines.generate_line()
            background_lines.change_pos()
        pygame.draw.rect(screen,(0,137,167),self.description_wall)
        pygame.draw.rect(screen,(186, 186, 186),self.scroll_line_backgroup)
        pygame.draw.rect(screen,(255,255,255),self.scroll_line)

        self.back_button.text(screen.get_width()-10 - self.back.get_width()-5,screen.get_height()-10- self.back.get_height()-5)

        for count,items in enumerate(self.listofitems):







            items[0].text(items[1][0],items[1][1])
            items[0].check(items[2],count+1)
        screen.blit(self.cost,(self.description_wall.x+self.coin.get_width(),self.description_wall.h-self.coin.get_height()-2))
        screen.blit(self.coin,(self.description_wall.x,self.description_wall.h-self.coin.get_height()-2))


        self.tick+=1
    def shop_check(self):
        def goback():
            global level
            level=0
            self.tick=0
            menu.menu_create()
        self.back_button.check(lambda:goback())
    def shop_maker(self):
        self.listofitems.clear()
        with open("shop_contain.csv") as shop_items:
            shop_items= csv.reader(shop_items, delimiter = ",")
            xofbox=2
            yofbox=2
            line_get=1
            ticktoignoretitles=0
            for items in shop_items:
                if ticktoignoretitles>=1:
                    item_name=self.sfont.render(f"{items[0]}",True,(self.white))
                    self.listofitems.append((shop_button(xofbox,yofbox,item_name,items[1],items[2],items[3],items[4],items[0]),(xofbox,yofbox),line_get)) # x,y,content,image,description,if they got the ability,cost
                    yofbox+=item_name.get_height()+pygame.image.load(items[1]).get_height() + 2
                    line_get+=1
                ticktoignoretitles+=1
                



            for item in self.listofitems:

                item[0].description_newline_get()


class highscore:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.white=(255,255,255)#
        self.bgcolour = ((0, 157, 181))
        self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
        self.highscore_text= self.sfont.render("highscore",True,self.white)
        self.text=""
        self.max=0
        self.max_height=0
        self.hightext=self.sfont.render(self.text,True,self.white)
        self.back=self.sfont.render("back",True,self.white)
        self.back_button = button(self.x-(screen.get_width()*0.2),self.y-(screen.get_height()*0.3),self.back)


    def highscore_create(self):
        global level
        level=-2
        screen.fill(self.bgcolour)
        Highscore.figure()

        highscore_rect=pygame.Rect((screen.get_width()//2-self.max/1.5,screen.get_height()//2-(self.max_height*4)),(self.max+10,(self.max_height*5)))
        pygame.draw.rect(screen,(0,173,212),highscore_rect)

        self.back_button.text((screen.get_width()-15-self.back.get_width()),(screen.get_height()-self.back.get_height()-15))
        self.hightext=self.sfont.render(Highscore.figure(),True,self.white)

        screen.blit(self.highscore_text,(10,10))
        screen.blit(self.hightext,(self.x//2,self.y//2))


        #highscore(x,y).highscore_check()

    def figure(self):
        high=open("highscore.csv","r").read().splitlines()
        r=0

        for l in range(3):
            r+=44

            self.text=(f"{l+1}.   {str(high[l])}")
            self.hightext=self.sfont.render(self.text,True,self.white)
            self.max=self.hightext.get_width() if self.hightext.get_width()>self.max else self.max
            self.max_height=self.hightext.get_height() if self.hightext.get_height() > self.max_height else self.max_height
            screen.blit(self.hightext,(screen.get_width()//2-150,screen.get_height()//2-150+r))


    def highscore_check(self):
        def goback():
            global level
            level=0
            menu.menu_create()
        self.back_button.check(lambda:goback())






'''this might be getting difficult to navigate'''


class background_speed:
    def __init__(self,xx,yy,place) -> None:
        self.x,self.y=xx,yy
        self.linex,self.liney=place,random.randint(0,screen.get_height())

        self.line4=pygame.Rect((self.linex+random.randint(10,screen.get_width()),self.liney-screen.get_height()),(3,60))
        self.line3=pygame.Rect((self.linex+random.randint(10,screen.get_width()),self.liney),(3,60))
        self.line2=pygame.Rect((self.linex-random.randint(10,screen.get_width()),self.liney+screen.get_height()),(3,60))
        self.line=pygame.Rect((self.linex,self.liney-60),(3,60))


    def generate_line(self):

        pygame.draw.rect(screen,(255,255,255),self.line)
        pygame.draw.rect(screen,(255,255,255),self.line2)
        pygame.draw.rect(screen,(255,255,255),self.line4)
        pygame.draw.rect(screen,(255,255,255),self.line3)

    def change_pos(self):
        self.liney-=15

        self.line4=pygame.Rect((self.linex+random.randint(10,screen.get_width()),self.liney-random.randint(10,screen.get_height())),(3,60))
        self.line3=pygame.Rect((self.linex+random.randint(10,screen.get_width()),self.liney),(3,60))
        self.line2=pygame.Rect((self.linex-random.randint(10,screen.get_width()),self.liney+random.randint(10,screen.get_height())),(3,60))
        self.line=pygame.Rect((self.linex,self.liney-60),(3,60))
        if self.liney<-120:
            self.liney=self.y


class setting:
  def __init__(self,x,y): # this will be a lot of variables :(
    self.x=x
    self.y=y
    self.place="general"

    self.bgcolour = ((0, 157, 181)) #common things
    self.white = ((255, 255, 255))
    self.box_colour=0, 173, 212
    self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)

    #more settings to be implemented


    '''I really dont want to create a whole new class for the keybinds tab :('''
    #text
    self.general=self.sfont.render("general",True,self.white)
    self.back=self.sfont.render("back",True,self.white)
    self.xy=self.sfont.render("resolution",True,self.white)
    self.movement=self.sfont.render("movement",True,self.white)
    self.volume_text=self.sfont.render("vol",True,self.white)

    self.xybackground = dropdown(10+self.volume_text.get_width()+180,0+(y*0.3),self.xy)


    self.movement_change=dropdown(30+self.xy.get_width()+self.volume_text.get_width()+180,0+(screen.get_height()*0.3),self.movement)
    self.playbackground = button(10, 10, self.general)
    self.backbackground = button(screen.get_width()-(screen.get_width()),screen.get_height()-(screen.get_height()),self.back)
    self.volume_slider = slider(10,(screen.get_height()*0.3),self.volume_text)





  def setting_create(self):
    global level

    level=-1
    screen.fill(self.bgcolour)
    setting(x,y).settings_check(event) #checks if button pressed and does the functionality

    self.playbackground.text(10, 10,)
    self.backbackground.text(screen.get_width()-(self.back.get_width())-15,screen.get_height()-(self.back.get_height())-15)
    self.xybackground.check(lambda:self.xybackground.drop("resolution_choice",lambda:self.xybackground.change_res()))
    self.movement_change.check(lambda:self.movement_change.drop("movement_choice",lambda:self.movement_change.change_control()))

    self.xybackground.view()
    self.movement_change.view()
    self.volume_slider.view()


  def settings_check(self,event):
    global level,active,x,y

    pygame.mouse.get_pos()


    def general_change(): self.place="general"
    self.playbackground.check(lambda: general_change())

    def backer(): # we go back to main menu
            global level
            level=0
            Menu().menu_create()
    self.backbackground.check(lambda: backer())

    self.volume_slider.check(lambda: self.volume_slider.volumer(event),event)



    #self.movement_change.writer(event,lambda: change_movement(self))





# This is where all the menu is
class Menu:
  def __init__(self):
      self.bgcolour = ((0, 157, 181))
      self.white = ((255, 255, 255))
      self.line_background1=background_speed(x,y,0+screen.get_width()//3)
      self.line_background2=background_speed(x,y,0+screen.get_width()//2)
      self.line_background3=background_speed(x,y,0+screen.get_width()-10)
      #consolas
      self.titl = pygame.font.SysFont("constantia", 40, bold=True)
      self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
      self.name=self.titl.render("Project Plane",True,self.white)
      self.play = self.sfont.render("Play", True, self.white)
      self.settings = self.sfont.render("Settings", True, self.white)
      self.highscore_text = self.sfont.render("Highscore",True,self.white)
      self.quit = self.sfont.render("Quit", True, self.white)
      self.shop = self.sfont.render("Shop",True,self.white)

      self.buttonplacey = (screen.get_height() // 2)
      self.buttonplacex = (screen.get_width() // 2) - 50

      self.diff = 0.1  # How far the buttons are away from each other xD

      # We build rectangles for buttons
      self.blocker =button((screen.get_width() // 2)  - self.play.get_width()//2, (screen.get_height() // 3) ,self.play)  # play
      self.blocker2 = button((screen.get_width() // 2) -self.settings.get_width()//2, (screen.get_height() // 3) + (self.diff+5+self.play.get_height()),self.settings)  # settings
      self.highscore = button((screen.get_width() // 2) - self.highscore_text.get_width()//2,(screen.get_height() // 3) + (self.diff +self.settings.get_height()+10+self.play.get_height()) , self.highscore_text)
      self.blocker3 = button((screen.get_width() // 2)  - self.quit.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+15+self.highscore_text.get_height()+self.play.get_height()),self.quit)  # quit
      self.shopper = button((screen.get_width() // 2)  - self.shop.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+20+self.highscore_text.get_height()+self.play.get_height())+self.quit.get_height(),self.shop)

  def menu_create(self):

      screen.fill(self.bgcolour)  # Fills background
       # Checks if there is any button presses in the menu :D
      self.line_background1.generate_line(), self.line_background1.change_pos()
      self.line_background2.generate_line(), self.line_background2.change_pos()
      self.line_background3.generate_line(), self.line_background3.change_pos()
      self.buttonplacey = (screen.get_height() // 2)
      self.buttonplacex = (screen.get_width() // 2)

      self.blocker.text(((screen.get_width() // 2) - self.play.get_width()//2),( (screen.get_height() // 3)))
      self.blocker2.text((screen.get_width() // 2) -self.settings.get_width()//2,( (screen.get_height() // 3) + (self.diff+5+self.play.get_height())))
      self.highscore.text((screen.get_width() // 2) - self.highscore_text.get_width()//2,((screen.get_height() // 3) + (self.diff +self.settings.get_height()+10+self.play.get_height())))
      self.blocker3.text((screen.get_width() // 2)  - self.quit.get_width()//2,( (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+20+self.highscore_text.get_height()+self.play.get_height()+self.shop.get_height())))
      self.shopper.text((screen.get_width() // 2)  - self.shop.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+15+self.highscore_text.get_height()+self.play.get_height()))

      screen.blit(self.name, (self.buttonplacex - self.name.get_width()//2, self.buttonplacey - (screen.get_height()*self.diff*3)))
  def play_game(self):

      with open("settings-containing.csv","w",newline="") as settings_file:
        csv.writer(settings_file).writerows(movement)

        settings_file.write(f"{screen.get_width()}\n{screen.get_height()}\n{overall_sound}")
      settings_file.close()
      pygame.display.quit()
      os.system("python project-plane/game.py")





  def checker(self): # sadly got to be in a diff function in the event loop so it works every click :(
      self.blocker.check(lambda: Menu().play_game())
      self.blocker2.check(lambda: setting(screen.get_width(),screen.get_height()).setting_create())

      self.highscore.check(lambda: highscore(screen.get_width(),screen.get_height()).highscore_create()) 
      self.blocker3.check(lambda: pygame.quit())
      self.shopper.check(lambda : shoop().shop_create())

#main running section
Shop=shoop()
menu = Menu()
active=False

Settings=setting(screen.get_width(),screen.get_height())
Highscore=highscore(screen.get_width(),screen.get_height())

while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if level==0:
            menu.checker()

        if level == -1:
          Settings.settings_check(event)

        if level == -2:
            Highscore.highscore_check()
        if level == 1 :
            Shop.shop_check()



    if level == 0:
        menu.menu_create()
    if level == -1:
      Settings.setting_create()
    if level == -2:
        Highscore.highscore_create()
    if level == 1: 
        Shop.shop_create()






    clock.tick(60)
    pygame.display.update()

'''to do list
1. redo menu, doesn't work as intended and could look better
2. more settings e.g. potato PC mode
3. Find an good font to use to make the game feel unique
4. PLEASE MAKE THE GAME EFFICIENT FOR MY BAD CHROMEBOOK

5. ambient of falling while in the main menu
6. engine sounds for the playerplane
7. pause menu while playing the game (tick)
8. 
'''
