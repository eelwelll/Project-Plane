
class shop_class:
    def __init__(self) -> None:
    
        actual_shop=open("shop_gotten.csv","r").read().splitlines()
        
           
        self.shop=[["Bullet hell","Bullet_Sprite/Bullet.png"," Cutting-edge technology derived from Foreign objects allows for aiming in different directions from where the plane is facing  . .",actual_shop[0],"100",1],
         ["High quality fuel","Bullet_Sprite/Bullet.png"," Better fuel has allowed the plane to carry less overall fuel leading to faster acceleration  . .",actual_shop[1],"300",1],
         ["Gunner","Bullet_Sprite/Bullet.png"," A top turret has been placed on your plane it might weigh the plane down though  . .",actual_shop[2],"400",1],
         ["Recovery","Bullet_Sprite/Bullet.png"," The plane now gains health over time  . .",actual_shop[3],"500",1],
         ["Friendly support","Bullet_Sprite/Bullet.png"," Placeholder text  . .",actual_shop[4],"1000",1],
         ["Advanced intelligence","Bullet_Sprite/Bullet.png"," Placeholder text  . .",actual_shop[5],"200",1]]
        self.bullet_upgrade= self.shop[0][3] == "True" 
        self.fuel_upgrade=  self.shop[1][3] == "True" 
        self.gunner_upgrade=  self.shop[2][3] == "True" 
        self.recovery_upgrade = self.shop[3][3] == "True" 
        self.friendly_support_upgrade = self.shop[4][3] == "True"
        self.advanced_int_upgrade = self.shop[5][3] == "True"
        print(self.bullet_upgrade,"\n",type(self.bullet_upgrade))
        
    def shop_update(self):
        actual_shop=open("shop_gotten.csv","r").read().splitlines()
        self.shop=[["Bullet hell","Bullet_Sprite/Bullet.png"," Cutting-edge technology derived from Foreign objects allows for aiming in different directions from where the plane is facing  . .",actual_shop[0],"100",1],
     ["High quality fuel","Bullet_Sprite/Bullet.png"," Better fuel has allowed the plane to carry less overall fuel leading to faster acceleration  . .",actual_shop[1],"300",1],
     ["Gunner","Bullet_Sprite/Bullet.png"," A top turret has been placed on your plane it might weigh the plane down though  . .",actual_shop[2],"400",1],
     ["Recovery","Bullet_Sprite/Bullet.png"," The plane now gains health over time  . .",actual_shop[3],"500",1],
     ["Friendly support","Bullet_Sprite/Bullet.png"," Placeholder text  . .",actual_shop[4],"1000",1],
     ["Advanced intelligence","Bullet_Sprite/Bullet.png"," Placeholder text  . .",actual_shop[5],"200",1]]
        
 
    