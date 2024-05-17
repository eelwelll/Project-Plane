
class shop_class:
    def __init__(self) -> None:
        
        actual_shop=open("shop_gotten.csv","r").read().splitlines()
        shop_unlocked=open("shop_unlocked.csv","r").read().splitlines()
        self.shop_status=shop_unlocked[0]  == "True"
        self.potato=shop_unlocked[1] == "True"
           
        self.shop=[["Bullet hell","Bullet_Sprite/Bullet.png"," Cutting-edge technology derived from Foreign objects allows for aiming in different directions from where the plane is facing  . .",actual_shop[0],"200",1],
         ["High quality fuel","Bullet_Sprite/Bullet.png"," Better fuel has allowed the plane to carry less overall fuel leading to faster acceleration  . .",actual_shop[1],"300",1],
         ["Gunner","Bullet_Sprite/Bullet.png"," A top turret has been placed on your plane it might weigh the plane down though  . .",actual_shop[2],"750",1],
         ["Recovery","Bullet_Sprite/Bullet.png"," The plane now gains health over time  . .",actual_shop[3],"2000",1],
         ["Friendly support","Bullet_Sprite/Bullet.png"," Friendly artillery will rain down shots (not in game yet)  . .",actual_shop[4],"1000",1],
         ["Advanced intelligence","Bullet_Sprite/Bullet.png"," Gain more EXP per enemy combatant taken down  . .",actual_shop[5],"5000",1],
         ["Hardmode","abilities/Advanced-Airframe.gif","combatant planes have become harder to fight against",actual_shop[6],"20000",1]]
        self.bullet_upgrade= self.shop[0][3] == "True" 
        self.fuel_upgrade=  self.shop[1][3] == "True" 
        self.gunner_upgrade=  self.shop[2][3] == "True" 
        self.recovery_upgrade = self.shop[3][3] == "True" 
        self.friendly_support_upgrade = self.shop[4][3] == "True"
        self.advanced_int_upgrade = self.shop[5][3] == "True"
        self.hardmode_upgrade = self.shop[6][3] == "True"

        
    def shop_update(self):
        actual_shop=open("shop_gotten.csv","r").read().splitlines()
        shop_unlocked=open("shop_unlocked.csv","r").read().splitlines()
        self.shop_status=shop_unlocked[0] == "True"
        self.shop=[["Bullet hell","Bullet_Sprite/Bullet.png"," Cutting-edge technology derived from Foreign objects allows for aiming in different directions from where the plane is facing  . .",actual_shop[0],"100",1],
             ["High quality fuel","Bullet_Sprite/Bullet.png"," Better fuel has allowed the plane to carry less overall fuel leading to faster acceleration  . .",actual_shop[1],"300",1],
             ["Gunner","Bullet_Sprite/Bullet.png"," A top turret has been placed on your plane it might weigh the plane down though  . .",actual_shop[2],"400",1],
             ["Recovery","Bullet_Sprite/Bullet.png"," The plane now gains health over time  . .",actual_shop[3],"500",1],
             ["Friendly support","Bullet_Sprite/Bullet.png"," Friendly artillery will rain down shots  . .",actual_shop[4],"1000",1],
             ["Advanced intelligence","Bullet_Sprite/Bullet.png"," Gain more EXP per enemy combatant taken down  . .",actual_shop[5],"200",1]]
        
 
    