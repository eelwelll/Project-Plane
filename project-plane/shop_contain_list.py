
class shop_class:
    def __init__(self) -> None:

        actual_shop=open("shop_gotten.csv","r").read().splitlines()
        shop_unlocked=open("shop_unlocked.csv","r").read().splitlines()
        actual_abilshop=open("ability_gotten.csv","r").read().splitlines()
        selected_abil=open("ability_selected.csv","r").read().splitlines()
        self.shop_status=shop_unlocked[0]  == "True"
        self.potato=shop_unlocked[1] == "True"
        self.abil_status=actual_shop[1] == "True"
        print(self.abil_status)

        self.shop=[["Bullet hell","Bullet_Sprite/Bullet.png"," Cutting-edge technology derived from Foreign objects allows for aiming in different directions from where the plane is facing  . .",actual_shop[0],"200",1],
         ["Unlock Ability shop","Bullet_Sprite/Bullet.png","  unlock and fit new potential power into your aircraft  . .", actual_shop[1],"200",1],
         ["Air burst","abilities/Propeller-Dispresion.gif"," Propeller upgrades enable the plane to let out short burst of power  . .",actual_shop[2],"200",1],
         ["High quality fuel","Bullet_Sprite/Bullet.png"," Better fuel has allowed the plane to carry less overall fuel leading to faster acceleration  . .",actual_shop[3],"600",1],
         ["Gunner","Bullet_Sprite/Bullet.png"," A top turret has been placed on your plane it might weigh the plane down though  . .",actual_shop[4],"1250",1],
         ["Recovery","Bullet_Sprite/Bullet.png"," The plane now gains health over time  . .",actual_shop[5],"5000",1],
         ["Friendly support","Bullet_Sprite/Bullet.png"," Friendly artillery will rain down HE air burst shots  . .",actual_shop[6],"10000",1],
         ["Advanced intelligence","Bullet_Sprite/Bullet.png"," Gain more EXP per enemy combatant taken down  . .",actual_shop[7],"15000",1],
         ["Hardmode","abilities/Advanced-Airframe.gif","combatant planes have become harder to fight against  . .",actual_shop[8],"20000",1]]
        self.bullet_upgrade= self.shop[0][3] == "True"
        self.dash_upgrade= self.shop[2][3] == "True"
        self.fuel_upgrade=  self.shop[3][3] == "True" 
        self.gunner_upgrade=  self.shop[4][3] == "True" 
        self.recovery_upgrade = self.shop[5][3] == "True" 
        self.friendly_support_upgrade = self.shop[6][3] == "True"
        self.advanced_int_upgrade = self.shop[7][3] == "True"
        self.hardmode_upgrade = self.shop[8][3] == "True"

        self.abil=[["Propeller-Dispresion","abilities/Propeller-Dispresion.gif"," uncertainty in the design makes the plane let out bursts of wind  . .",actual_abilshop[0],"0",selected_abil[0]],
                   ["Missile-Barrage","abilities/Missile-Barrage.gif"," The plane can now carry unguided missiles  . .",actual_abilshop[1],"0",selected_abil[1]],
                   ["High-Calibre","abilities/High-Calibre.gif","The plane has the ability to carry high calibre bullets, making it more deadly  . .",actual_abilshop[2],"0",selected_abil[2]],
                   ["Accelerated-Shot","abilities/Accelerated-Shot.gif","The planes barrel has been upgraded, allowing for more shots per minute  . .",actual_abilshop[3],"0",selected_abil[3]],
                   ["Advanced-Airframe","abilities/Advanced-Airframe.gif"," airframe has ained more structural integrity  . .",actual_abilshop[4],"0",selected_abil[4]],
                   ["Retarded-bombs","abilities/retarded_bomb-1.gif"," The plane can now carry not only unguided missiles but retarded bombs!  . .",actual_abilshop[5],"250",selected_abil[5]],
                   ["The-Fat-Man","abilities/The-Fat-Man.gif","nuke  . .",actual_abilshop[6],"500",selected_abil[7]],
                   ["EMP","abilities/EMP.gif","A burst of electromagnetic radiation, stopping enemies in their tracks, looks rather alien  . .", actual_shop[7],"1000",selected_abil[7]],
                   ["Shotgun","abilities/Shotgun.gif","Why hasn't anyone thought of putting a shotgun on a plane yet!  . .",actual_abilshop[8],"1500",selected_abil[8]],
                   ["Coin-madness","abilities/Coin-madness.gif","200% increase in highscore/gold  . .",actual_abilshop[9],"2000",selected_abil[9]],
                   ["The-kiss-of-life","abilities/The-kiss-of-life.gif","gain a life, but at a cost   . .",actual_abilshop[10],"5000",selected_abil[10]],
                   ["Purple-hollow","Purple_hollow/purple-hollow-6.png","Nine Ropes, Polarized Light, Crows, and Shimyo, Between Front and Back  . .",actual_abilshop[10],"10000",selected_abil[10]],
                   ["Myriads-Spear","abilities/Myriads-spear.gif","Sacred power from divine beings, how did it end up in your hands?  . .",actual_abilshop[11],"11000",selected_abil[11]]]



    def shop_update(self):
        actual_shop=open("shop_gotten.csv","r").read().splitlines()
        shop_unlocked=open("shop_unlocked.csv","r").read().splitlines()
        actual_abilshop=open("ability_gotten.csv","r").read().splitlines()
        selected_abil=open("ability_selected.csv","r").read().splitlines()
        self.shop_status=shop_unlocked[0] == "True"
        self.potato=shop_unlocked[1] == "True"
        self.abil_status=actual_shop[1] == "True"
        
        self.shop=[["Bullet hell","Bullet_Sprite/Bullet.png"," Cutting-edge technology derived from Foreign objects allows for aiming in different directions from where the plane is facing  . .",actual_shop[0],"200",1],
             ["Unlock Ability shop","Bullet_Sprite/Bullet.png","  unlock and fit new potential power into your aircraft  . .", actual_shop[1],"200",1],
             ["Air burst","abilities/Propeller-Dispresion.gif"," Propeller upgrades enable the plane to let out short burst of power  . .",actual_shop[2],"200",1],
             ["High quality fuel","Bullet_Sprite/Bullet.png"," Better fuel has allowed the plane to carry less overall fuel leading to faster acceleration  . .",actual_shop[3],"600",1],
             ["Gunner","Bullet_Sprite/Bullet.png"," A top turret has been placed on your plane it might weigh the plane down though  . .",actual_shop[4],"1250",1],
             ["Recovery","Bullet_Sprite/Bullet.png"," The plane now gains health over time  . .",actual_shop[5],"5000",1],
             ["Friendly support","Bullet_Sprite/Bullet.png"," Friendly artillery will rain down HE air burst shots  . .",actual_shop[6],"10000",1],
             ["Advanced intelligence","Bullet_Sprite/Bullet.png"," Gain more EXP per enemy combatant taken down  . .",actual_shop[7],"15000",1],
             ["Hardmode","abilities/Advanced-Airframe.gif","combatant planes have become harder to fight against  . .",actual_shop[8],"20000",1]]
        self.bullet_upgrade= self.shop[0][3] == "True"
        self.dash_upgrade= self.shop[2][3] == "True"
        self.fuel_upgrade=  self.shop[3][3] == "True" 
        self.gunner_upgrade=  self.shop[4][3] == "True" 
        self.recovery_upgrade = self.shop[5][3] == "True" 
        self.friendly_support_upgrade = self.shop[6][3] == "True"
        self.advanced_int_upgrade = self.shop[7][3] == "True"
        self.hardmode_upgrade = self.shop[8][3] == "True"
        self.abil=[["Propeller-Dispresion","abilities/Propeller-Dispresion.gif"," uncertainty in the design makes the plane let out bursts of wind  . .",actual_abilshop[0],"0",selected_abil[0]],
               ["Missile-Barrage","abilities/Missile-Barrage.gif"," The plane can now carry unguided missiles  . .",actual_abilshop[1],"0",selected_abil[1]],
               ["High-Calibre","abilities/High-Calibre.gif","The plane has the ability to carry high calibre bullets, making it more deadly  . .",actual_abilshop[2],"0",selected_abil[2]],
               ["Accelerated-Shot","abilities/Accelerated-Shot.gif","The planes barrel has been upgraded, allowing for more shots per minute  . .",actual_abilshop[3],"0",selected_abil[3]],
               ["Advanced-Airframe","abilities/Advanced-Airframe.gif"," airframe has ained more structural integrity  . .",actual_abilshop[4],"0",selected_abil[4]],
               ["Retarded-bombs","abilities/retarded_bomb-1.gif"," The plane can now carry not only unguided missiles but retarded bombs!  . .",actual_abilshop[5],"250",selected_abil[5]],
               ["The-Fat-Man","abilities/The-Fat-Man.gif","nuke  . .",actual_abilshop[6],"500",selected_abil[7]],
               ["EMP","abilities/EMP.gif","A burst of electromagnetic radiation, stopping enemies in their tracks, looks rather alien  . .", actual_shop[7],"1000",selected_abil[7]],
               ["Shotgun","abilities/Shotgun.gif","Why hasn't anyone thought of putting a shotgun on a plane yet!  . .",actual_abilshop[8],"1500",selected_abil[8]],
               ["Coin-madness","abilities/Coin-madness.gif","200% increase in highscore/gold  . .",actual_abilshop[9],"2000",selected_abil[9]],
               ["The-kiss-of-life","abilities/The-kiss-of-life.gif","gain a life, but at a cost   . .",actual_abilshop[10],"5000",selected_abil[10]],
               ["Purple-hollow","Purple_hollow/purple-hollow-6.png","Nine Ropes, Polarized Light, Crows, and Shimyo, Between Front and Back  . .",actual_abilshop[10],"10000",selected_abil[10]],
               ["Myriads-Spear","abilities/Myriads-spear.gif","Sacred power from divine beings, how did it end up in your hands?  . .",actual_abilshop[11],"11000",selected_abil[11]]]
        