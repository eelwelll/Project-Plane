import pygame
import os


class paused:

    def __init__(self, highscore, screen, abilityselection, replitbad,
                 overallsound) -> None:
        self.screen = screen
        self.abilityselection = abilityselection
        self.highscore = highscore
        # three variables needed because of the new file format that I am using
        self.sfont = pygame.font.SysFont("arialblack", 100, bold=False)
        self.small_font = pygame.font.SysFont("arialblack", 30, bold=False)
        self.paused_text_behind = self.sfont.render("PAUSED", True, (0, 0, 0))
        self.paused_text = self.sfont.render("PAUSED", True, (255, 255, 255))
        self.quit_text = self.sfont.render("QUIT", True, (255, 255, 255))
        from main_button import button
        self.quit = button(screen.get_width() // 2,
                           screen.get_height() // 2, self.quit_text,
                           overallsound, replitbad, screen)
        self.coin_image = pygame.image.load("menu-item/coin.png")
        self.coin_gotten = ""

        with open("how_many_coins.csv", "r") as coins_have:
            for line in coins_have:
                self.coin_gotten = line
        self.coin_text = self.small_font.render(self.coin_gotten, True,
                                                (255, 255, 255))
        self.coin_image = pygame.transform.scale(
            self.coin_image,
            (self.coin_image.get_width(), self.coin_text.get_height()))
        self.score = self.sfont.render(f"score:{highscore}", True,
                                       (255, 255, 255))

    def draw(self, highscore):
        self.quit.text(
            self.screen.get_width() // 2 - self.quit.rect.w // 2,
            self.screen.get_height() // 2 + self.abilityselection.bigbox.y,
            self.quit_text)
        self.abilityselection.update_location()

        self.sfont = pygame.font.SysFont("arialblack",
                                         self.screen.get_height() // 7,
                                         bold=False)
        self.paused_text_behind = self.sfont.render("PAUSED", True, (0, 0, 0))
        self.paused_text = self.sfont.render("PAUSED", True, (255, 255, 255))
        self.highscore = highscore
        self.score = self.sfont.render(f"score:{self.highscore}", True,
                                       (255, 255, 255))
        if not self.abilityselection.real:
            self.screen.blit(
                self.score,
                (self.abilityselection.bigbox.centerx -
                 self.score.get_width() // 2, self.abilityselection.bigbox.y))
            self.screen.blit(
                self.paused_text,
                (self.abilityselection.bigbox.centerx -
                 self.paused_text.get_width() // 2,
                 self.abilityselection.bigbox.y + self.score.get_height()))
            #self.screen.blit(self.paused_text_behind,(self.abilityselection.bigbox.centerx-self.paused_text.get_width()//2-5,self.abilityselection.bigbox.centery-self.paused_text.get_height()//2))
        with open("how_many_coins.csv", "r") as coins_have:
            coins_have = coins_have.read().splitlines()
            self.coin_gotten = coins_have[0]

        self.coin_text = self.small_font.render(
            f"{self.coin_gotten} + {self.highscore//10}", True,
            (255, 255, 255))
        self.coin_image = pygame.transform.scale(
            self.coin_image,
            (self.coin_image.get_width(), self.coin_text.get_height()))
        self.screen.blit(
            self.coin_image,
            (self.screen.get_width() // 2 -
             self.coin_text.get_width() - self.coin_image.get_width() // 2,
             self.screen.get_height() // 2 + self.paused_text.get_height()))
        self.screen.blit(
            self.coin_text,
            (self.screen.get_width() // 2 - self.coin_text.get_width() // 2,
             self.screen.get_height() // 2 + self.paused_text.get_height()))

    def check(self):

        def quit():

            pygame.display.quit()
            highscore_list = []
            with open("highscore.csv", "r") as highscore_file:
                highscore_file = highscore_file.read().splitlines()
                for lines in highscore_file:
                    lines = lines.split(",")
                    highscore_list.append((lines[0], lines[1]))
                index = 0
                there = False
                iteration = 0
                for pos, lines in enumerate(highscore_list):
                    num = 0
                    iteration += 1
                    if iteration > 1:
                        num = int(lines[1])

                    if there:
                        break
                    if num > self.highscore:
                        index = pos
                    if num < self.highscore:
                        highscore_list.insert(pos + 1, ("", self.highscore))
                        there = True

                    print(num, pos, lines, highscore_list)
                if not there:
                    highscore_list.append(("", self.highscore))
            print(highscore_list)
            with open("highscore.csv", "w") as highscore_file:
                total = ""
                for lines in highscore_list:

                    total += f"{lines[0]},{lines[1]}\n"
                highscore_file.write(total)
            coins_have = open("how_many_coins.csv", "r+")
            coin = 0
            for lines in coins_have:
                coin = int(lines)
                coins_have.truncate()

                coin = str(coin + (self.highscore // 10))
                coins_have = open("how_many_coins.csv", "w")

                coins_have.write(coin)
            coins_have = open("how_many_coins.csv", "r+")

            os.system("python project-plane/main.py")

        self.quit.check(lambda: quit())
