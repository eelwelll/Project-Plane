import pygame


class write:

    def __init__(self, xx, xy, content, word, screen):
        self.screen = screen

        self.yx, self.yy = xx, xy
        self.diff = content.get_width()
        screen.blit(content, (xx, xy))
        self.sfont = pygame.font.SysFont("arialblack", 40, bold=False)
        self.words = word
        self.context = self.sfont.render(self.words, True, (255, 255, 255))
        self.rect = pygame.Rect((self.yx + self.diff, self.yy),
                                (self.context.get_width() if
                                 self.context.get_width() > 100 else 100, 44))

        self.w=self.rect.w
        self.h=self.rect.h

    def text(self,newx,newy):
        self.rect = pygame.Rect((newx , newy),
                                (self.context.get_width() if
                                 self.context.get_width() > 100 else 100, 44))

        pygame.draw.rect(self.screen, (0, 173, 212), self.rect)

        self.context = self.sfont.render(self.words, True, (255, 255, 255))
        self.screen.blit(self.context, self.rect)

    def writer(self, objective,event):
            mouse=pygame.mouse.get_pos()
      
            if event.type == pygame.KEYDOWN and self.rect.collidepoint(mouse):
                if event.key == pygame.K_BACKSPACE:
                    self.words = self.words[:-1]
                elif event.key == pygame.K_RETURN:
                    if objective:
                        objective()
                elif len(self.words) <= 10:
                    self.words += event.unicode

    def change_res(self, event):
        global x, y
        #BIT THAT IS UNIQUE THE RESOLUTION
        newx, newy = '', ''

        change = False
        for l in range(len(self.words)):
            if self.words[l].lower() == 'x' and change is False:
                change = True
            if self.words[l] == "x":
                continue
            if not change:
                newx += str(self.words[l])
            else:
                newy += str(self.words[l])
        pygame.display.set_mode((int(newx), int(newy)), pygame.RESIZABLE)
        x, y = int(newx), int(newy)

    def change_movement(self, event, movement):
        global moveup, movedown, moveleft, moveright
        count = 0
        if event.key == pygame.K_RETURN:
            for l in range(0, len(self.words), 2):
                movement[count] = self.words[l]
                count += 1
