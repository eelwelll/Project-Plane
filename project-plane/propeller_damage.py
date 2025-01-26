import pygame
class propeller_dispersion:

    def __init__(self, xx, yy):
        self.frame = pygame.image.load("prop/propeller-0.png")
        self.rect = self.frame.get_rect()
        self.frameon = 0
        self.rect.center = xx, yy
        self.x, self.y = xx - 10, yy
        self.rect = self.rect.inflate(self.frame.get_width() * 3,
                                      self.frame.get_height() * 3)
        self.cooldown = True
    
    def image_get(self,xx,yy,enhance,tick,screen):
        if tick % 6 == 0:
            self.frameon = self.frameon + 1 if self.frameon + 1 < 9 else 0
        if not enhance:
            self.frame = pygame.image.load(f"prop/propeller-{self.frameon}.png")
        else:
            self.frame=pygame.transform.scale_by(pygame.image.load(f"fire_prop/propeller-{self.frameon}.png"),1.25)
        self.frame = pygame.transform.scale_by(self.frame, 4)
        screen.blit(self.frame, (self.rect.x, self.rect.y))
        if not enhance:
            self.rect.x = xx - self.frame.get_width() // 4
            self.rect.y = yy - self.frame.get_height() // 4
        if enhance:
            self.rect.x,self.rect.y=xx- self.frame.get_width() // 6,yy - self.frame.get_height() // 6