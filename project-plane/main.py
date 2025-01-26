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
x, y =1340,460
xx,yy=x,y
accel=1
movement=[["w",-abs(accel),"u"],["a",-abs(accel),"di"],["s",accel,"u"],["d",accel,"di"]]
moveup,moveleft,movedown,moveright=movement[0],movement[1],movement[2],movement[3]
overall_sound=0.25
screen = pygame.display.set_mode((x, y),pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True  # Boolean to control the game loop
level = 0
screen_change_by=15


'''button.'''
class button:
    def __init__(self,x,y,content,block,text) -> None:

        self.there=False
        self.content=content
        self.block=block
        self.x,self.y=x,y
        self.rect=pygame.Rect((self.x,self.y), (content.get_width(),self.content.get_height()))
        self.sfont = pygame.font.SysFont("arialblack", int(screen.get_height()//screen_change_by), bold=False)
        self.placeholder=self.sfont.render("I",True,(255,255,255))
        if not replitbad:
            self.hover=pygame.mixer.Sound("sound/click.wav")
            self.hover.set_volume(overall_sound)

            self.selected=pygame.mixer.Sound(f"sound/clickonmenu.wav")

            self.selected.set_volume(overall_sound)
        self.hoveronce=False
        self.hovertick=0
        self.textt=text


    def text(self,x,y,content,block):
            self.sfont = pygame.font.SysFont("arialblack", int(screen.get_height()/screen_change_by), bold=False)
            self.sfont_backdrop_text = pygame.font.SysFont("arialblack", int(screen.get_height()/screen_change_by), bold=False)
            self.x,self.y=x,y
            self.content=content
            self.block=block
            self.back_text=self.sfont_backdrop_text.render(f"{self.textt}",True,(0,137,167))

            self.rect=pygame.Rect((self.x,self.y), (self.content.get_width()+10,self.content.get_height()+3))

            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(screen,(0, 195, 237) if not self.block else ( 209, 13, 49 ),self.rect)
                screen.blit(self.back_text,(self.rect.x+5,self.rect.y+6))
                screen.blit(content,(self.rect.x+5,self.rect.y+1))



                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not replitbad:
                    if not replitbad:

                        self.hover.set_volume(overall_sound)
                        self.selected.set_volume(overall_sound)

                    self.hover.play()

                self.hovertick+=1


                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(screen,(0,137,167 )  if not self.block else (235, 16, 56),self.rect)
            else:
                self.hoveronce=False
                self.hovertick=0
                
                

                pygame.draw.rect(screen,(0, 173, 212) if not self.block else (179, 4, 36),self.rect)


                #screen.blit(self.back_text,(self.rect.x+6,self.rect.y+3))
                screen.blit(content,(self.rect.x+5,self.rect.y+3))

    def check(self,objective):
        global mouse
        mouse=pygame.mouse.get_pos()
        #update it hopefully

        self.rect=pygame.Rect((self.x,self.y), (self.content.get_width(),self.content.get_height()+3))
        #
        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if not replitbad:
                        self.selected.play()
                    pygame.draw.rect(screen,(0,137,167),self.rect)


                    objective()

'''dropdown menu button, mainly used in settings menu and changing plane :D'''

class dropdown(button):
    def __init__(self,xx,yy,content,text) -> None:
        super().__init__(xx,yy,content,False,text)
        self.chosen=''
        self.toggle=False
        self.sfont = pygame.font.SysFont("arialblack", screen.get_height()//screen_change_by, bold=False)

        self.new=pygame.Rect((self.x,self.y),(self.content.get_width(),self.content.get_height()))
        self.arrow=pygame.image.load("arrow_down.png")
        self.rect=pygame.Rect((self.x,self.y),(self.content.get_width()+self.arrow.get_width(),self.arrow.get_height()))




    # can now use method text because of inheritance :D
    def view(self):
        self.content=self.orig

        self.sfont = pygame.font.SysFont("arialblack", screen.get_height()//screen_change_by, bold=False)
        self.sfont_backdrop = pygame.font.SysFont("arialblack", screen.get_height()//screen_change_by-(screen_change_by//7), bold=False)
        self.text_backdrop = self.sfont_backdrop.render(f"{self.textt}",True,(0,137,167))
        pygame.draw.rect(screen,(0,173,212),self.rect)
        self.rect=pygame.Rect((self.x,self.y),(self.content.get_width()+self.arrow.get_width(),self.arrow.get_height()))
        

        screen.blit(self.arrow,(self.posx+self.rect.w-self.arrow.get_width(),self.posy))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.text_backdrop,(self.posx+5,self.posy+5))
        else:
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
                    self.sfont = pygame.font.SysFont("arialblack",int(screen.get_height()//screen_change_by), bold=False)
                    self.new=pygame.Rect((self.x,self.y+10),(drop.get_width(),drop.get_height()))
                    self.rect=pygame.Rect((self.x,self.y+10),(drop.get_width(),drop.get_height()))



            screen.blit(drop,(self.x,self.y+r))
            r+=new.h+5



    def check(self,objective):

        if self.toggle:
            objective()

        if objective and self.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            self.toggle=True

        if objective and not self.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:

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
    def change_potato(self):
        keep_line=""
        change_csv=open("shop_unlocked.csv","r").read().splitlines()
        keep_line=f"{change_csv[0]}\n"
        keep_line+=self.chosen
        change_csv=open("shop_unlocked.csv","w")
        change_csv.write(keep_line)



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








from shop_contain_list import shop_class
shop_contain=shop_class()

class shop_button:
    def __init__(self,x,y,content,image,description,pos,cost,actual_name,type) -> None:

        self.there=False
        self.content=content
        self.what=actual_name
        self.x,self.y=x,y
        self.image_name=image
        self.type=type
        if type=="constant":
            shop_get_place=open("shop_gotten.csv","r").read().splitlines()
        if type=="ability":
            shop_get_place=open("ability_gotten.csv","r").read().splitlines()
        self.gotten=shop_get_place[pos]

        self.colour=(0, 195, 237) if self.gotten else (247, 104, 104) # left == blue
        self.colour_again=(0, 173, 212) if self.gotten else (219, 29, 29) # right sie == red , left side == blue
        self.image=pygame.image.load(image)
        self.rect=pygame.Rect((self.x,self.y), (content.get_width(),self.content.get_height()*2))
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
        self.image_in_box=pygame.transform.scale(self.image,(self.rect.h,self.rect.h)) #final image form




        self.description=self.sfont.render(description,True,(255,255,255))
        if self.type=="constant":
            self.text_box_description=pygame.Rect((screen.get_width()//1.5,Shop.description_wall.y+self.content.get_height()+10+self.image.get_height()),(screen.get_width()//2.5,Shop.description_wall.h-self.content.get_height()+10+self.image.get_height()))
        if self.type=="ability":
            self.text_box_description=pygame.Rect((screen.get_width()//1.5,Shop_ability.description_wall.y+self.content.get_height()+10+self.image.get_height()),(screen.get_width()//2.5,Shop_ability.description_wall.h-self.content.get_height()+10+self.image.get_height()))


        if not replitbad:
            self.hover=pygame.mixer.Sound("sound/click.wav")

            self.selected=pygame.mixer.Sound("sound/clickonmenu.wav")
            self.openshop=pygame.mixer.Sound("sound/shop_open.wav")



            self.openshop.set_volume(overall_sound)


            self.hover.set_volume(overall_sound)
            self.selected.set_volume(overall_sound)
        self.hoveronce=False
        self.hovertick=0
        self.drag=False
        self.click=0
        self.timesincelastclick=0

    def description_newline_get(self):
        last_let_place=0
        height=self.description.get_height()+10
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
                    self.desc_text.append((self.desc_get_text[last_let_place:des],self.text_box_description.y+5+self.image.get_height()+20+(height*len(self.desc_text))))

                    last_let_place=des

            if end:
                    des=let if let_get == space else (-previous_word)
                    self.desc_text.append((self.desc_get_text[last_let_place:des],self.text_box_description.y+5+self.image.get_height()+20+(height*len(self.desc_text))))
                    last_let_place=des


            let+=1


    def text(self,x,y,dif):
            self.x,self.y=x,y
            self.colour=(0, 195, 237) if self.gotten== "True" else (247, 104, 104) # left == blue 0, 195, 237
            self.colour_again=(0, 173, 212) if self.gotten== "True" else (219, 29, 29) # right sie == red , left side == blue
            self.colour_again=self.colour_again if self.cost_number>int(Shop.coins) or self.gotten=="True" else (212, 194, 32) 
            self.rect=pygame.Rect((self.x,self.y-dif), (self.content.get_width()+5,self.content.get_height()*2))
            if self.type=="constant":
                self.text_box_description=pygame.Rect((screen.get_width()//1.5,Shop.description_wall.y+self.content.get_height()+10+self.image.get_height()),(screen.get_width()//2.5,Shop.description_wall.h-self.content.get_height()+10+self.image.get_height()))
            if self.type=="ability":
                self.text_box_description=pygame.Rect((screen.get_width()//1.5,Shop_ability.description_wall.y+self.content.get_height()+10+self.image.get_height()),(screen.get_width()//2.5,Shop_ability.description_wall.h-self.content.get_height()+10+self.image.get_height()))
            
            
            if self.rect.collidepoint(mouse): #0, 195, 237
                pygame.draw.rect(screen,(self.colour),self.rect)
                if self.type=="constant":
                    screen.blit(self.content,(Shop.description_wall.x,Shop.description_wall.y))
                    screen.blit(self.cost,(Shop.description_wall.x+self.coin.get_width(),Shop.description_wall.y+self.content.get_height()))
                    screen.blit(self.coin,(Shop.description_wall.x,Shop.description_wall.y+self.content.get_height()))
                if self.type=="ability":
                    screen.blit(self.content,(Shop_ability.description_wall.x,Shop_ability.description_wall.y))
                    screen.blit(self.cost,(Shop_ability.description_wall.x+self.coin.get_width(),Shop_ability.description_wall.y+self.content.get_height()))
                    screen.blit(self.coin,(Shop_ability.description_wall.x,Shop_ability.description_wall.y+self.content.get_height()))
                if pygame.mouse.get_pressed()[0]:
                    self.drag=True
                    self.click+=1
                    self.timesincelastclick=clock.get_time()
                    if self.click>=2:
                        Shop_ability.doubleclicked=True


                self.hoveronce=True
                if (self.hoveronce and self.hovertick==0) and not replitbad:

                        self.hover.set_volume(overall_sound)
                        self.selected.set_volume(overall_sound)
                        self.hover.play()


                descimage=pygame.transform.scale_by(self.image,3)
                if self.type=="constant":
                    screen.blit(descimage,(Shop.description_wall.centerx-descimage.get_width(),Shop.description_wall.y+self.content.get_height()+10)) # nvm this is the final image form
                if self.type=="ability":
                    screen.blit(descimage,(Shop_ability.description_wall.centerx-descimage.get_width(),Shop_ability.description_wall.y+self.content.get_height()+10)) # nvm this is the final image form

                for lines in self.desc_text:
                    screen.blit(self.sfont.render(f"{lines[0]}",True,(255,255,255)),(self.text_box_description.x,lines[1]+50))



                self.hovertick+=1



            else:
                self.hoveronce=False
                self.hovertick=0

                pygame.draw.rect(screen,self.colour_again,self.rect)
            if  not pygame.mouse.get_pressed()[0]:
                self.drag=False
            if self.timesincelastclick+60<=clock.get_time():
                self.click=0
                Shop_ability.doubleclicked=False
            


            if self.drag and not Shop_ability.selecting and not self.rect.collidepoint(mouse) and self.gotten=="True":

                if self.type=="ability":

                    img=self.image
                    screen.blit(img,(mouse[0]-img.get_width()//2,mouse[1]-img.get_height()//2))
                    self.drag=True


               

            if pygame.display.get_init() and self.image:
                #screen.blit(self.image_in_box,(self.rect.centerx-self.image.get_width(),self.rect.centery-self.image.get_height()))
                screen.blit(self.content,(self.rect.x,self.rect.y))
    def get_collide(self):
        return self.rect.collidepoint(mouse)


    def check(self,objective,position):
        global mouse, shop_contain


        #update it hopefully


        if pygame.mouse.get_pressed()[0] and objective and self.rect.collidepoint(mouse):
                    if (self.hoveronce and self.hovertick==0) and not replitbad:
                        self.selected.play()


                    coin=0
                    have=open("how_many_coins.csv","r+")
                    for line in have:
                        coin=int(line)



                    if self.gotten == "False" and not self.cost_number-1>=coin:
                            coins_have=open("how_many_coins.csv","r+")


                            if not replitbad:
                                self.openshop.play()
                            for lin in (coins_have):

                                if int(lin)>=self.cost_number:
                                    temp=int(lin)-self.cost_number

                                    coins_have=open("how_many_coins.csv","w")
                                    coins_have.write(f"{temp}")
                                    coins_have.close()
                            temp=0
                            if self.type=="constant":
                                actualshop=open("shop_gotten.csv","w+")
                            if self.type=="ability":
                                actualshop=open("ability_gotten.csv","w+")
                            actualshop.truncate()
                            whatwewrite=""
                            length=shop_contain.shop

                            if self.type=="constant":
                                length=shop_contain.shop

                            if self.type=="ability":
                                length=shop_contain.abil


                            for pos,l in enumerate(length):


                                    if l[0]==self.what:

                                        whatwewrite+="True\n"

                                    else:
                                        whatwewrite+=f"{length[pos][3]}\n"
                            actualshop.write(whatwewrite)


                            actualshop.close()

                            shop_contain.shop_update()
                            self.gotten="True"














                                        #replacing_content=f"{self.what},{self.image_name},{self.desc_get_text},True,{self.cost}"









class shoop:
    def __init__(self,type):
        self.type=type
        self.bgcolour=((0,157,181))
        self.white=(255,255,255)
        self.sfont = pygame.font.SysFont("arialblack",  int(screen.get_height()//screen_change_by), bold=False)
        self.back=self.sfont.render("Back",True,self.white)
        self.back_button = button(screen.get_width()-10,screen.get_height()-10,self.back,False,"Back")
        self.tick=0
        self.listofitems=[]
        self.line_background_list=[background_speed(x,y,0+screen.get_width()//3),background_speed(x,y,0+screen.get_width()//2),background_speed(x,y,0+screen.get_width()-10)]
        self.line_y=0
        self.line_y_start=screen.get_height()//10
        self.dif=self.line_y_start+self.line_y
        self.scrolling=False
        self.description_wall=pygame.Rect(screen.get_width()/1.5,0,screen.get_width()/2.5,screen.get_height()-self.back.get_height()-20)
        self.scroll_line=pygame.Rect((screen.get_width()/1.5-self.description_wall.w//3,2),(screen.get_width()/100,screen.get_height()//10))
        self.scroll_line_backgroup=pygame.Rect((screen.get_width()/1.5-self.description_wall.w//3,2),(screen.get_width()/100,screen.get_height()//self.description_wall.h))

        self.coins=0

        self.cost=self.sfont.render(f"{self.coins}",True,self.white)
        original=pygame.image.load("menu-item/coin.png")
        self.coin=pygame.transform.scale(original,(self.cost.get_height(),self.cost.get_height())) 
        self.abilityshowcase=open("ability_selected.csv","r").read().splitlines()
        self.selected=[]
        for num,line in enumerate(self.abilityshowcase):
            if line =="True":
                self.selected.append(shop_contain.abil[num][1])
        
        self.wofbox,self.hofbox=screen.get_width()//20,screen.get_width()//20
        self.box1=pygame.Rect(((screen.get_width()/1.5)/2-self.wofbox*2.5,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
        self.box2=pygame.Rect(((screen.get_width()/1.5)/2-self.wofbox,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
        self.box3=pygame.Rect(((screen.get_width()/1.5)/2,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
        self.box4=pygame.Rect(((screen.get_width()/1.5)/2+self.wofbox,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
        self.box5=pygame.Rect(((screen.get_width()/1.5)/2+self.wofbox*2.5,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
        self.innerbox=pygame.Rect(((screen.get_width()/1.5)/2-self.wofbox*2.5+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
        self.innerbox2=pygame.Rect(((screen.get_width()/1.5)/2-self.wofbox+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
        self.innerbox3=pygame.Rect(((screen.get_width()/1.5)/2+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
        self.innerbox4=pygame.Rect(((screen.get_width()/1.5)/2+self.wofbox-(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
        self.innerbox5=pygame.Rect(((screen.get_width()/1.5)/2+self.wofbox*2.5+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
        self.innerboxlist=[self.innerbox,self.innerbox2,self.innerbox3,self.innerbox4,self.innerbox5]
        self.boxlist=[self.box1,self.box2,self.box3,self.box4,self.box5]
        self.drag=False
        self.dragtick=0
        self.selecting=False
        self.doubleclicked=False

        if not replitbad:
            self.openshop=pygame.mixer.Sound("sound/shop_open.wav")



            self.openshop.set_volume(overall_sound)




    def shop_create(self):
        coins_have=open("how_many_coins.csv","r").read().splitlines()
        for coin in coins_have:
            self.coins=coin


        self.cost=self.sfont.render(f"{self.coins}",True,self.white)

        global level
        level=1 if self.type == "constant" else 2

        self.description_wall=pygame.Rect(screen.get_width()/1.5,0,screen.get_width()/2.5,screen.get_height()-self.back.get_height()-20)

        if self.tick==0:
            if self.type=="constant":

                Shop.shop_maker()
            if self.type=="ability":
                Shop_ability.shop_maker()
            if not replitbad:
                self.openshop.play()
        screen.fill(self.bgcolour)

        for background_lines in self.line_background_list:
            background_lines.generate_line()
            background_lines.change_pos()
        pygame.draw.rect(screen,(0,137,167),self.description_wall)
        if self.type=="ability":
            self.wofbox,self.hofbox=screen.get_width()//20,screen.get_width()//20
            self.box1.update(((screen.get_width()/1.5)/2-self.wofbox*2.5,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
            self.box2.update(((screen.get_width()/1.5)/2-self.wofbox*1.25,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
            self.box3.update(((screen.get_width()/1.5)/2,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
            self.box4.update(((screen.get_width()/1.5)/2+self.wofbox*1.25,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
            self.box5.update(((screen.get_width()/1.5)/2+self.wofbox*2.5,screen.get_height()-screen.get_height()/4),(self.wofbox,self.hofbox))
            self.innerbox=pygame.Rect(((screen.get_width()/1.5)/2-self.wofbox*2.5+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4+(self.hofbox/10)/2),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
            self.innerbox2=pygame.Rect(((screen.get_width()/1.5)/2-self.wofbox*1.25+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4+(self.hofbox/10)/2),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
            self.innerbox3=pygame.Rect(((screen.get_width()/1.5)/2+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4+(self.hofbox/10)/2),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
            self.innerbox4=pygame.Rect(((screen.get_width()/1.5)/2+self.wofbox*1.25+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4+(self.hofbox/10)/2),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
            self.innerbox5=pygame.Rect(((screen.get_width()/1.5)/2+self.wofbox*2.5+(self.wofbox/10)/2,screen.get_height()-screen.get_height()/4+(self.hofbox/10)/2),(self.wofbox-self.wofbox/10,self.hofbox-self.hofbox/10))
            self.innerboxlist=[self.innerbox,self.innerbox2,self.innerbox3,self.innerbox4,self.innerbox5]
            self.boxlist=[self.box1,self.box2,self.box3,self.box4,self.box5]

            for box in range(len(self.boxlist)):

                pygame.draw.rect(screen,(0, 195, 237) if self.boxlist[box].collidepoint(mouse) else (0, 173, 212),self.boxlist[box])

                if (self.boxlist[box].collidepoint(mouse) and pygame.mouse.get_pressed()[0]) and not self.drag and len(self.selected)-1>=0: # clearing one box if pressed
                    replace=""
                    for num,line in enumerate(shop_contain.abil):
                        if line[1] in self.selected and box!=self.selected.index(shop_contain.abil[num][1]):
                            replace+="True\n"
                        else:
                            replace+="False\n"
                    
                    with open("ability_selected.csv","w") as abil:
                        abil.truncate()
                        abil.write(replace)
                        abil.close()
                    self.selected=[]
                    with open("ability_selected.csv","r") as abili:
                        for num,line in enumerate(abili):
                            if line =="True":
                                self.selected.append(shop_contain.abil[num][1])
        
                if self.boxlist[box].collidepoint(mouse) and not self.selecting and len(self.selected)<5 or self.doubleclicked and len(self.selected)<5: # if an ability is being hovered over in the box it gets added to current abilities
                    for count,items in enumerate(self.listofitems):
                        if ((items[0].drag and items[0].image_name not in self.selected) or (items[0].click>=2 and items[0].image_name not in self.selected)) and items[0].gotten=="True":
                            self.selected.append(items[0].image_name)
                            items[0].click=0
                    replace=""
                    for line in shop_contain.abil:
                        if line[1] in self.selected:
                            replace+="True\n"
                        else:
                            replace+="False\n"
                    
                    abil=open("ability_selected.csv","w")
                    abil.truncate()
                    abil.write(replace)
                    abil.close()



            if pygame.mouse.get_pressed()[0]:
                    self.drag=True
            else:
                    self.drag=False
                



            for inn in range(len(self.innerboxlist)):
                pygame.draw.rect(screen,(0,137,167),self.innerboxlist[inn])


                if inn<len(self.selected):
                    screen.blit(pygame.transform.scale(pygame.image.load(self.selected[inn]),(self.innerboxlist[inn].w,self.innerboxlist[inn].h)),(self.innerboxlist[inn]))


        pygame.draw.rect(screen,(186, 186, 186),self.scroll_line_backgroup)
        pygame.draw.rect(screen,(255,255,255),self.scroll_line)

        self.back_button.text(screen.get_width()-10 - self.back.get_width()-5,screen.get_height()-10- self.back.get_height()-5,self.back,False)

        for count,items in enumerate(self.listofitems):



            items[0].text(items[1][0],items[1][1],self.dif)
            items[0].check(items[2],count+1)
            if items[0].drag:
                for counter,itemer in enumerate(self.listofitems):

                    if count==counter:
                        continue
                    if itemer[0].get_collide():
                        self.selecting=True
                    elif not self.selecting:
                        self.selecting=False
                



        screen.blit(self.cost,(self.description_wall.x+self.coin.get_width(),self.description_wall.h-self.coin.get_height()-2))
        screen.blit(self.coin,(self.description_wall.x,self.description_wall.h-self.coin.get_height()-2))
        self.line_y_start=screen.get_height()//10
        self.dif=self.line_y_start+self.line_y - self.scroll_line.h

        if (self.scroll_line_backgroup.collidepoint(mouse) or self.scrolling) and pygame.mouse.get_pressed()[0] and self.scroll_line_backgroup.contains(self.scroll_line):
            self.line_y=mouse[1] - (self.scroll_line.h/2)
            self.scrolling=True
        if not pygame.mouse.get_pressed()[0]:
            self.scrolling=False
            self.selecting=False
        if not self.scroll_line_backgroup.contains(self.scroll_line) and not self.scrolling:
            if self.scroll_line.y<screen.get_height()/2:
                self.line_y+=1
            else:
                self.line_y-=1
        if event.type==pygame.MOUSEWHEEL and self.scroll_line_backgroup.contains(self.scroll_line):
            self.line_y-=event.y*10
            event.y=0

        self.scroll_line_backgroup=pygame.Rect((screen.get_width()/1.5-screen.get_width()/100-2,2),(screen.get_width()/100,self.description_wall.h-2))
        self.scroll_line=pygame.Rect((screen.get_width()/1.5-screen.get_width()/100-2,3+self.line_y),(screen.get_width()/100,(screen.get_height()//10)))


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

            shop_items=shop_contain.shop
            shop_abilities=shop_contain.abil
            xofbox=2
            yofbox=2
            line_get=1

            if self.type=="constant":
                shop_gotten=open("shop_gotten.csv","r").read().splitlines()

                for pos,items in enumerate(shop_items):

                    item_name=self.sfont.render(f"{items[0]}",True,(self.white))

                    self.listofitems.append((shop_button(xofbox,yofbox,item_name,items[1],items[2],pos,items[4],items[0],self.type),(xofbox,yofbox),line_get)) # x,y,content,image,description,if they got the ability,cost
                    yofbox+=(item_name.get_height()+2)*2

                    line_get+=1




            if self.type=="ability":

                ability_gotten=open("ability_gotten.csv","r").read().splitlines()
                numberinrow=0
                for pos,items in enumerate(shop_abilities):
                    nfont = pygame.font.SysFont("arialblack",  int(screen.get_height()/screen_change_by/2), bold=False)
                    item_name=nfont.render(f"{items[0]}",True,(self.white))

                    self.listofitems.append((shop_button(xofbox,yofbox,item_name,items[1],items[2],pos,items[4],items[0],self.type),(xofbox,yofbox),line_get,)) # x,y,content,image,description,if they got the ability,cost
                    if ((xofbox+item_name.get_width() + 20) <= screen.get_width()/2 ) and  numberinrow<4:
                        numberinrow+=1
                        xofbox+=item_name.get_width() + 10
                    else:
                        xofbox=2
                        yofbox+=(item_name.get_height()+2)*2
                        if numberinrow>=4:
                            numberinrow=0
                        numberinrow+=1
                    if items[0] == "Advanced-Airframe":
                        yofbox+=(item_name.get_height() + 2 )*2




                    line_get+=1
            for item in self.listofitems:

                item[0].description_newline_get()

class select_ability(shoop):
    def __init__(self):
        pass



class highscore:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.white=(255,255,255)#
        self.bgcolour = ((0, 157, 181))
        self.sfont = pygame.font.SysFont("arialblack",  int(screen.get_height()//screen_change_by), bold=False)
        self.highscore_text= self.sfont.render("highscore",True,self.white)
        self.text=""
        self.max=0
        self.max_height=0
        self.hightext=self.sfont.render(self.text,True,self.white)
        self.back=self.sfont.render("Back",True,self.white)
        self.back_button = button(self.x-(screen.get_width()*0.2),self.y-(screen.get_height()*0.3),self.back,False,"Back")


    def highscore_create(self):
        global level
        level=-2
        screen.fill(self.bgcolour)
        Highscore.figure()

        highscore_rect=pygame.Rect((screen.get_width()//2-self.max/1.5,screen.get_height()//2-(self.max_height*4)),(self.max+10,(self.max_height*5)))
        #pygame.draw.rect(screen,(0,173,212),highscore_rect)

        self.back_button.text((screen.get_width()-15-self.back.get_width()),(screen.get_height()-self.back.get_height()-15),self.back,False)
        self.hightext=self.sfont.render(Highscore.figure(),True,self.white)

        screen.blit(self.highscore_text,(10,10))
        screen.blit(self.hightext,(self.x//2,self.y//2))


        #highscore(x,y).highscore_check()

    def figure(self):
        num=[]
        high=open("highscore.csv","r").read().splitlines()
        for lines in high:
            lines=lines.split(",")
            num.append((lines[0],lines[1]))

        iteration=0

        while iteration<=len(high): 
            for number in range(1,len(num)-1):
                temp=num[number][1]

                if number+1<=len(num):
                    if int(num[number][1])>int(num[number+1][1]):
                          temp=num[number+1]
                          num[number+1]=num[number]
                          num[number]=temp
                          iteration-=1
                iteration+=1


        r=0
        num.reverse()
        for l in range(4):
            r+=44

            self.text=(f"{l+1}.   {str(num[l][0])},{str(num[l][1])}")
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
        self.line_behind=pygame.Rect((self.line.x+1,self.line.y+1),(3,60))
        self.line2_behind=pygame.Rect((self.line2.x+1,self.line2.y+1),(3,60))
        self.line3_behind=pygame.Rect((self.line3.x+1,self.line3.y+1),(3,60))
        self.line4_behind=pygame.Rect((self.line3.x+1,self.line3.y+1),(3,60))

        self.colour_for_beind=(200, 200, 200)

    def generate_line(self):

        pygame.draw.rect(screen,self.colour_for_beind,self.line_behind)
        pygame.draw.rect(screen,self.colour_for_beind,self.line2_behind)
        pygame.draw.rect(screen,self.colour_for_beind,self.line4_behind)
        pygame.draw.rect(screen,(self.colour_for_beind),self.line3_behind)
        pygame.draw.rect(screen,(255,255,255),self.line)
        pygame.draw.rect(screen,(255,255,255),self.line2)
        pygame.draw.rect(screen,(255,255,255),self.line4)
        pygame.draw.rect(screen,(255,255,255),self.line3)
    def change_pos(self):
        self.liney-=15

        self.line4=pygame.Rect((self.linex+random.randint(10,screen.get_width()),self.liney-random.randint(10,screen.get_height())),(3,60))
        self.line3=pygame.Rect((self.linex+random.randint(10,screen.get_width()),self.liney),(3,60))
        self.line2=pygame.Rect((self.linex-random.randint(10,screen.get_width()),self.liney+random.randint(10,screen.get_height())),(3,60))
        self.line_behind=pygame.Rect((self.line.x+3,self.line.y+1),(3,60))
        self.line2_behind=pygame.Rect((self.line2.x+3,self.line2.y+1),(3,60))
        self.line3_behind=pygame.Rect((self.line3.x+3,self.line3.y+1),(3,60))
        self.line4_behind=pygame.Rect((self.line3.x+3,self.line3.y+1),(3,60))

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
    self.sfont = pygame.font.SysFont("arialblack",  int(screen.get_height()//screen_change_by), bold=False)

    #more settings to be implemented


    '''I really dont want to create a whole new class for the keybinds tab :('''
    #text
    self.general=self.sfont.render("General",True,self.white)
    self.back=self.sfont.render("Back",True,self.white)
    self.xy=self.sfont.render("Resolution",True,self.white)
    self.movement=self.sfont.render("Movement",True,self.white)
    self.volume_text=self.sfont.render("Vol",True,self.white)
    self.potato_text=self.sfont.render("Potato",True,self.white)

    self.xybackground = dropdown(10+self.volume_text.get_width()+180,0+(y*0.3),self.xy,"Resolution")


    self.movement_change=dropdown(30+self.xy.get_width()+self.volume_text.get_width()+250,0+(screen.get_height()*0.3),self.movement,"Movement")
    self.playbackground = button(10, 10, self.general,False,"General")
    self.backbackground = button(screen.get_width()-(screen.get_width()),screen.get_height()-(screen.get_height()),self.back,False,"Back")
    self.volume_slider = slider(10,(screen.get_height()*0.3),self.volume_text)
    self.potato_dropdown=dropdown(10,screen.get_height()*0.4,self.potato_text,"Potato")





  def setting_create(self):
    global level

    level=-1
    screen.fill(self.bgcolour)
    setting(x,y).settings_check(event) #checks if button pressed and does the functionality
    self.sfont = pygame.font.SysFont("arialblack",  int(screen.get_height()//screen_change_by), bold=False)
    self.general=self.sfont.render("General",True,self.white)
    self.back=self.sfont.render("Back",True,self.white)
    self.xy=self.sfont.render("Resolution",True,self.white)
    self.movement=self.sfont.render("Movement",True,self.white)
    self.volume_text=self.sfont.render("Vol",True,self.white)
    self.potato_text=self.sfont.render("Potato",True,self.white)

    self.playbackground.text(10, 10,self.general,False)
    self.backbackground.text(screen.get_width()-(self.back.get_width())-15,screen.get_height()-(self.back.get_height())-15,self.back,False)
    self.xybackground.check(lambda:self.xybackground.drop("resolution_choice",lambda:self.xybackground.change_res()))
    self.movement_change.check(lambda:self.movement_change.drop("movement_choice",lambda:self.movement_change.change_control()))
    self.potato_dropdown.check(lambda: self.potato_dropdown.drop("true_false_choice",self.potato_dropdown.change_potato()))

    self.xybackground.text(10+self.volume_text.get_width()+180,0+(y*0.3),self.xy,False)
    self.movement_change.text(30+self.xy.get_width()+self.volume_text.get_width()+250,0+(screen.get_height()*0.3),self.movement,False)
    self.volume_slider.view()
    self.potato_dropdown.text(10,screen.get_height()*0.4,self.potato_text,False)


  def settings_check(self,event):
    global level,x,y

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
      self.titl = pygame.font.Font("fonts/Project_plane_font.ttf",  int(screen.get_height()//screen_change_by*2),)
      self.titl_backdrop = pygame.font.Font("fonts/Project_plane_font.ttf",  int(screen.get_height()//screen_change_by*2.75),)
      self.sfont = pygame.font.SysFont("arialblack",  int(screen.get_height()//screen_change_by), bold=False)
      self.name=self.titl.render("Project Plane",True,self.white)
      self.titl_second_backdrop=pygame.font.Font("fonts/Project_plane_font.ttf",  int(screen.get_height()//screen_change_by*2.9))
      self.name_second_backdrop=self.titl_second_backdrop=self.titl_second_backdrop.render("Project Plane",True,(110, 110, 110))
      self.name_backdrop=self.titl_backdrop.render("Project Plane",True,(0,0,0))
      self.play = self.sfont.render("Play", True, self.white)
      self.settings = self.sfont.render("Settings", True, self.white)
      self.highscore_text = self.sfont.render("Highscore",True,self.white)
      self.quit = self.sfont.render("Quit", True, self.white)
      self.shop = self.sfont.render("Shop",True,self.white)
      self.othershop= self.sfont.render("Ability Select",True,self.white)
      self.reset_text = self.sfont.render("Reset",True,self.white)

      self.buttonplacey = (screen.get_height() // 2)
      self.buttonplacex = (screen.get_width() // 2) - 50

      self.diff = 0.1  # How far the buttons are away from each other 

      # We build rectangles for buttons
      self.blocker =button((screen.get_width() // 2)  - self.play.get_width()//2, (screen.get_height() // 3) ,self.play,False,"Play")  # play
      self.blocker2 = button((screen.get_width() // 2) -self.settings.get_width()//2, (screen.get_height() // 3) + (self.diff+5+self.play.get_height()),self.settings,False,"Settings")  # settings
      self.highscore = button((screen.get_width() // 2) - self.highscore_text.get_width()//2,(screen.get_height() // 3) + (self.diff +self.settings.get_height()+10+self.play.get_height()) , self.highscore_text,False,"Highscore")
      self.blocker3 = button((screen.get_width() // 2)  - self.quit.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+15+self.highscore_text.get_height()+self.play.get_height()+self.othershop.get_height()),self.quit,False,"Quit")  # quit
      if shop_contain.shop_status:
          self.shopper = button((screen.get_width() // 2)  - self.shop.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+20+self.highscore_text.get_height()+self.play.get_height())+self.quit.get_height(),self.shop,False,"Shop")
          self.reset = button(10,screen.get_height()-self.reset_text.get_height()-10,self.reset_text,False,"Reset")
          self.abilityshopper = button((screen.get_width() // 2)  - self.othershop.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+20+self.highscore_text.get_height()+self.play.get_height()+self.shop.get_height()),self.othershop,False if shop_contain.abil_status else True,"Abiliy select")

  def menu_create(self):
      self.titl = pygame.font.Font("fonts/Project_plane_font.ttf",  int(screen.get_height()//screen_change_by*3),)
      self.titl_backdrop = pygame.font.Font("fonts/Project_plane_font.ttf",  int(screen.get_height()//screen_change_by*2.75),)
      self.sfont = pygame.font.SysFont("arialblack",  int(screen.get_height()//screen_change_by), bold=False)
      self.name=self.titl.render("Project Plane",True,self.white)
      self.name_backdrop=self.titl_backdrop.render("Project Plane",True,(0,0,0))
      self.play = self.sfont.render("Play", True, self.white)
      self.settings = self.sfont.render("Settings", True, self.white)
      self.highscore_text = self.sfont.render("Highscore",True,self.white)
      self.quit = self.sfont.render("Quit", True, self.white)
      self.shop = self.sfont.render("Shop",True,self.white)
      self.othershop= self.sfont.render("Ability Select",True,self.white)
      self.reset_text = self.sfont.render("Reset",True,self.white)
      self.titl_second_backdrop=pygame.font.Font("fonts/Project_plane_font.ttf",  int(screen.get_height()//screen_change_by*2.85))
      self.name_second_backdrop=self.titl_second_backdrop=self.titl_second_backdrop.render("Project Plane",True,(110, 110, 110))
      
      screen.fill(self.bgcolour)  # Fills background
       # Checks if there is any button presses in the menu :D
      self.line_background1.generate_line(), self.line_background1.change_pos()
      self.line_background2.generate_line(), self.line_background2.change_pos()
      self.line_background3.generate_line(), self.line_background3.change_pos()
      self.buttonplacey = (screen.get_height() // 2)
      self.buttonplacex = (screen.get_width() // 2)

      self.blocker.text(((screen.get_width() // 2) - self.play.get_width()//2),( (screen.get_height() // 3)),self.play,False)
      self.blocker2.text((screen.get_width() // 2) -self.settings.get_width()//2,( (screen.get_height() // 3) + (self.diff+5+self.play.get_height())),self.settings,False)
      self.highscore.text((screen.get_width() // 2) - self.highscore_text.get_width()//2,((screen.get_height() // 3) + (self.diff +self.settings.get_height()+10+self.play.get_height())),self.highscore_text,False)
      self.blocker3.text((screen.get_width() // 2)  - self.quit.get_width()//2,( (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+25+self.highscore_text.get_height()+self.play.get_height()+self.shop.get_height()+self.othershop.get_height())),self.quit,False)
      if shop_contain.shop_status:
        self.shopper.text((screen.get_width() // 2)  - self.shop.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+15+self.highscore_text.get_height()+self.play.get_height()),self.shop,False)
        self.reset.text(10,screen.get_height()-self.reset_text.get_height()-10,self.reset_text,False)
        self.abilityshopper.text((screen.get_width() // 2)  - self.othershop.get_width()//2, (screen.get_height() // 3)  + (self.diff+self.settings.get_height()+20+self.highscore_text.get_height()+self.play.get_height()+self.shop.get_height()),self.othershop,False if shop_contain.abil_status else True)
      screen.blit(self.name_backdrop, (self.buttonplacex - self.name_backdrop.get_width()//2, self.buttonplacey - (screen.get_height()*self.diff*4)))
      screen.blit(self.name_second_backdrop,(self.buttonplacex - self.name_second_backdrop.get_width()//2, self.buttonplacey - (screen.get_height()*self.diff*4)))
      screen.blit(self.name, (self.buttonplacex - self.name.get_width()//2, self.buttonplacey - (screen.get_height()*self.diff*4)))
  def play_game(self):

      with open("settings-containing.csv","w",newline="") as settings_file:
        csv.writer(settings_file).writerows(movement)

        settings_file.write(f"{screen.get_width()}\n{screen.get_height()}\n{overall_sound}")
      settings_file.close()
      pygame.display.quit()
      os.system("python project-plane/game.py")
  def clear_progress(self):
    with open("how_many_coins.csv","w") as coin:
        coin.write("0")
    reset_gotten=open("shop_gotten.csv","w")
    reset_ability=open("ability_gotten.csv","w")
    reset_ability_selected=open("ability_selected.csv","w")
    reset_gotten.truncate()
    reset_ability.truncate()
    replace=""
    for lines in shop_contain.shop:
        replace+="False\n"


    reset_gotten.write(str(replace))
    replace=""
    for l in range(5):
        replace+="True\n"
    for l in range(len(shop_contain.abil)-5):
        replace+="False\n"
    reset_ability.write(str(replace))
    reset_ability_selected.write(str(replace))
    reset_ability_selected.close()
    reset_ability.close()
    shop_contain.abil_status=False

      



  def checker(self): # sadly got to be in a diff function in the event loop so it works every click :(
      self.blocker.check(lambda: Menu().play_game())
      self.blocker2.check(lambda: setting(screen.get_width(),screen.get_height()).setting_create())

      self.highscore.check(lambda: highscore(screen.get_width(),screen.get_height()).highscore_create()) 
      self.blocker3.check(lambda: pygame.quit())
      if shop_contain.shop_status:
          self.shopper.check(lambda : shoop("constant").shop_create())
          self.abilityshopper.check(lambda : shoop("ability").shop_create() if shop_contain.abil_status else None)
          self.reset.check(lambda: Menu().clear_progress())

#main running section
Shop=shoop("constant")
Shop_ability=shoop("ability")
menu = Menu()


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
        if level == 2:
            Shop_ability.shop_check()


    if level == 0:
        menu.menu_create()
    if level == -1:
      Settings.setting_create()
    if level == -2:
        Highscore.highscore_create()
    if level == 1:
        Shop.shop_create()
    if level==2:
        Shop_ability.shop_create()




    clock.tick(60)
    pygame.display.update()

'''to do list
1. redo menu, doesn't work as intended and could look better (tick, slightly)
2. more settings e.g. potato PC mode ( tick, doesn't work sometimes though)
3. Find an good font to use to make the game feel unique ( tick )
4. PLEASE MAKE THE GAME EFFICIENT FOR MY BAD CHROMEBOOK ( idk it started working better on repl)

5. ambient of falling while in the main menu ||||||||||||||||||||||||||||
6. engine sounds for the playerplane ||||||||||||||||||||||||||||||||||||
7. pause menu while playing the game (tick) 
8. "add in dificulyty setting" - Harry ( tick )
9. "Add fix gramma to this" - Harry |||||||||||||||||||||||||||||||||||||
10. "SoundTrack" - Harry (what the flip ) |||||||||||||||||||||||||||||||
11. add a EMP that disruts enemy movement - Kleidi ( tick )
12. Have cooldown for proppeller dispersion on early planes ( not tick )

13. fix screen for ability shop
14. make ability shop translate to the actual game ( tick )
15. maybe add more bosses


16. have upgrades as a choice when entering, choose between 5    
'''