import pygame
import sqlite3
import random
import time
import os 
import sys
import RPi.GPIO as GPIO
from pygame.locals import *
from main_game import MainGame
class Gameplay:
    def __init__(self):
        pygame.init()
        self.arrowsP1 = []
        self.arrowsP2 = []
        self.countScreen = 0
        self.selectedSong = 0
        self.width = 800
        self.height = 600
        self.font = pygame.font.SysFont(None, 40)
        self.username = ''
        self.background = pygame.image.load("background.png")
        self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.setArrowArrange()
        self.songEnd = 0
        self.scoreP1 = 0
        self.scoreP2 = 0
        self.k = 0
        self.selectedMode = 0
        self.song = ""
        self.check = True
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)



        # # GPIO.setup(4, GPIO.OUT)
        # # GPIO.setup(17, GPIO.OUT)
        # # GPIO.setup(27, GPIO.OUT)
        # # GPIO.setup(22, GPIO.OUT)
        # # GPIO.setup(16, GPIO.OUT)
        # # GPIO.setup(21, GPIO.OUT)
        # # GPIO.setup(19, GPIO.OUT)
        # # GPIO.setup(7, GPIO.OUT)

        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(21, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(26, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(19, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(16, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(24, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(27, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(17, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        GPIO.add_event_detect(4, GPIO.RISING, callback=self.button_callback, bouncetime=200)
        
        # GPIO.output(7, True)
        # GPIO.output(17, False)
        # GPIO.output(27, False)
        # GPIO.output(22, False)
        # GPIO.output(16, False)
        # GPIO.output(21, False)
        # GPIO.output(19, False)
        # GPIO.output(26, False)
        self.highScore = [[100,'TooN'],[25,'tOOn'],[20,'TtoonN'],[0,'None'],[0,'None']]
    def button_callback(self, channel):
        direction = None
        ch1 = [21,26,19,16]
        if channel in ch1:
            if channel == 21:
                direction = 0
            elif channel == 26:
                direction = 1
            elif channel == 19:
                direction = 2
            elif channel == 16:
                 direction = 3
            for arrow in self.arrowsP1:
                if arrow.direction == direction and arrow.checkElapse():
                    self.scoreP1 += 500
                    arrow.setY(self.height + 50)
                    break
        else:
            if channel == 24:
                direction = 4
            elif channel == 27:
                direction = 5
            elif channel == 17:
                direction = 6
            elif channel == 4:
                direction = 7
            for arrow in self.arrowsP2:
                if arrow.direction == direction and arrow.checkElapse():
                    self.scoreP2 += 500
                    arrow.setY(self.height + 50)
                    break
                
    def setArrowArrange(self):
        self.startX = [self.width * 0.144791667, self.width * 0.2, self.width * 0.25364583,
                       self.width * 0.3088125, self.width * 0.6442700, self.width * 0.6984375,
                       self.width * 0.7546875, self.width * 0.8127708]
        self.endX = [self.width * 0.05, self.width * 0.16875, self.width * 0.2864503,
                     self.width * 0.404375, self.width * 0.55, self.width * 0.66875,
                     self.width * 0.78333, self.width * 0.90364583]
        self.endY = self.height * 0.71111111
        self.startY = self.height * 0.062037
        self.m = []
        self.c = []
        for i in range(8):
            self.m.append((self.endY - self.startY) / (self.endX[i] - self.startX[i]))
            self.c.append(((-(self.startX[i])) * self.m[i]) + self.startY)

    def setBackground(self, path):
        self.background = pygame.image.load(path)

    def startPage(self):
        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))

    def getNamePage(self):
        self.setBackground("background2.png")
        name = pygame.image.load("nameEnter.png").convert_alpha()
        temp = self.height
        self.input_box = pygame.Rect(self.width * 0.35732188, self.height * 0.49333358, self.width * 0.28480312,
                                     self.height * 0.08739076)
        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        while (temp > 0):
            self.screen.blit(pygame.transform.scale(name, (self.width, self.height)), (0, temp))
            pygame.display.flip()
            temp -= 60

        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        self.screen.blit(pygame.transform.scale(name, (self.width, self.height)), (0, 0))

        pygame.draw.rect(self.screen, [239, 255, 226], self.input_box)

    def selectSongPage(self):
        self.setBackground("background3.png")
        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        songSelect = pygame.image.load("songSelect.png").convert_alpha()
        songSelected = pygame.image.load("songSelected.png").convert_alpha()
        songName = pygame.image.load("songName.png").convert_alpha()
        yPlus = 0
        for i in range(5):
            if i == self.selectedSong:
                self.screen.blit(
                    pygame.transform.scale(songSelected,
                                           (round(self.width * 0.50364583), round(self.height * 0.09074074))),
                    (self.width * 0.24791667, self.height * 0.25722222 + yPlus))
            else:
                self.screen.blit(
                    pygame.transform.scale(songSelect,
                                           (round(self.width * 0.50364583), round(self.height * 0.09074074))),
                    (self.width * 0.24791667, self.height * 0.25722222 + yPlus))
            yPlus += self.height * 0.12962963
        self.screen.blit(pygame.transform.scale(songName, (self.width, self.height)), (0, 0))

    def startGame(self):
        self.setBackground("background4.png")
        self.arrowImage = pygame.image.load("arrow.png").convert_alpha()

        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        p1 = random.randint(0, 3)
        p2 = p1 + 4
        if len(self.arrowsP1) > 0:
            if self.arrowsP1[-1].getY() > self.startY + 60:
                self.arrowsP1.append(Arrow(p1, self.startX[p1], self.height, self.m[p1], self.c[p1]))
                self.arrowsP2.append(Arrow(p2, self.startX[p2], self.height, self.m[p2], self.c[p2]))
        else:
            self.arrowsP1.append(Arrow(p1, self.startX[p1], self.height, self.m[p1], self.c[p1]))
            self.arrowsP2.append(Arrow(p2, self.startX[p2], self.height, self.m[p2], self.c[p2]))
        count = 0
        for i in self.arrowsP1:
            if i.getY() < self.height * 0.751111:
                self.screen.blit(pygame.transform.scale(self.arrowImage, (
                round(self.width * 0.05533854), round(self.height * 0.06866417))), (i.getX(), i.getY()))
                i.changeXY()
            if i.getY() > self.height * 0.751111:
                count += 1
            i.changeSpeed()

        for i in range(count):
            self.arrowsP1.pop(0)

        count = 0

        for i in self.arrowsP2:
            if i.getY() < self.height * 0.751111:
                self.screen.blit(pygame.transform.scale(self.arrowImage, (
                round(self.width * 0.05533854), round(self.height * 0.06866417))), (i.getX(), i.getY()))
                i.changeXY()
            if i.getY() > self.height * 0.751111:
                count += 1
            i.changeSpeed()

        for i in range(count):
            self.arrowsP2.pop(0)

        txt_surface = self.font.render(str(self.scoreP1), True, [255, 255, 255])
        self.screen.blit(txt_surface, (10,10))

        ll = len(str(self.scoreP2))*40
        txt_surface2 = self.font.render(str(self.scoreP2), True, [255, 255, 255])
        self.screen.blit(txt_surface2, (self.width-ll, 10))

    def playSound(self, event):
        if event.key == pygame.K_RETURN:
            pygame.mixer.music.load('enter.mp3')
            pygame.mixer.music.play()
            self.countScreen += 1

        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            pygame.mixer.music.load('select.wav')
            pygame.mixer.music.play()

    def endVs(self):
        if self.scoreP1 > self.scoreP2:
            image = pygame.image.load("p1Win.png").convert_alpha()
        elif self.scoreP2 > self.scoreP1:
            image = pygame.image.load("p2Win.png").convert_alpha()
        else:
            image = pygame.image.load("draw.png").convert_alpha()

        self.screen.blit(pygame.transform.scale(image, (self.width, self.height)), (0, 0))

    def selectMode(self):
        if self.selectedMode == 0:
            self.setBackground("singleMode.png")
        else:
            self.setBackground("multiMode.png")
        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0)) 
    def showHighScore(self):
        font = self.font
        ind = -1
        songSelect = pygame.image.load("songSelect.png").convert_alpha()
        songSelected = pygame.image.load("songSelected.png").convert_alpha()
        if self.scoreP1 > self.highScore[4][0]:
            self.countScreen = 4
            for i in range(5):
                if (self.highScore[i][0] < self.scoreP1):
                    ind = i
                    break
            if ind != -1:
                for j in range(4,ind-1,-1):
                    if j != ind:
                        self.highScore[j][0] = self.highScore[j-1][0]
                        self.highScore[j][1] = self.highScore[j-1][1]
                    else:
                        self.highScore[j][0] = self.scoreP1

        self.getNamePage()
        pygame.display.flip()
        temp = True
        while(temp):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.highScore[ind][1] = self.username
                        temp = False
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif len(self.username) <= 10:
                        self.username += event.unicode
                    pygame.draw.rect(self.screen, [239, 255, 226], self.input_box)
                    txt_surface = self.font.render(self.username, True, [0, 0, 0])
                    self.screen.blit(txt_surface, (self.input_box.x * 1.1, self.input_box.y * 1.05))
                    pygame.display.flip()

        txt_surface1 = font.render(str(self.highScore[0][1]), True, [0, 0, 0])
        txt_surface6 = font.render(str(self.highScore[0][0]), True, [0, 0, 0])
        txt_surface2 = font.render(str(self.highScore[1][1]), True, [0, 0, 0])
        txt_surface7 = font.render(str(self.highScore[1][0]), True, [0, 0, 0])
        txt_surface3 = font.render(str(self.highScore[2][1]), True, [0, 0, 0])
        txt_surface8 = font.render(str(self.highScore[2][0]), True, [0, 0, 0])
        txt_surface4 = font.render(str(self.highScore[3][1]), True, [0, 0, 0])
        txt_surface9 = font.render(str(self.highScore[3][0]), True, [0, 0, 0])
        txt_surface5 = font.render(str(self.highScore[4][1]), True, [0, 0, 0])
        txt_surface10 = font.render(str(self.highScore[4][0]), True, [0, 0, 0])

        self.setBackground("background5.png")
        self.screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        yPlus = 0

        for j in range(5):
            if j == ind and ind > -1:
                self.screen.blit(pygame.transform.scale(songSelected,
                                                   (round(self.width * 0.50364583),
                                                    round(self.height * 0.09074074))),
                            (self.width * 0.24791667, self.height * 0.24722222 + yPlus))
            else:
                self.screen.blit(
                    pygame.transform.scale(songSelect,
                                           (round(self.width * 0.50364583), round(self.height * 0.09074074))),
                    (self.width * 0.24791667, self.height * 0.24722222 + yPlus))
            if j == 0:
                self.screen.blit(txt_surface1,
                            (self.width * 0.24791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
                self.screen.blit(txt_surface6,
                            (self.width * 0.54791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
            elif j == 1:
                self.screen.blit(txt_surface2,
                            (self.width * 0.24791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
                self.screen.blit(txt_surface7,
                            (self.width * 0.54791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
            elif j == 2:
                self.screen.blit(txt_surface3,
                            (self.width * 0.24791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
                self.screen.blit(txt_surface8,
                            (self.width * 0.54791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
            elif j == 3:
                self.screen.blit(txt_surface4,
                            (self.width * 0.24791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
                self.screen.blit(txt_surface9,
                            (self.width * 0.54791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
            elif j == 4:
                self.screen.blit(txt_surface5,
                            (self.width * 0.24791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
                self.screen.blit(txt_surface10,
                            (self.width * 0.54791667 * 1.1, (self.height * 0.24722222 + yPlus) * 1.05))
            yPlus += self.height * 0.12962963
        
        pygame.display.flip()
        time.sleep(5)

    def run(self):
        self.startPage()
        pygame.display.flip()
        while True:
            if self.countScreen == 3:
                if self.selectedMode == 1:
                    self.startGame()
                elif self.check:
                    game = MainGame('doubt')
                    self.scoreP1 = game.run()
                    self.check = False
            for event in pygame.event.get():
                if event.type == self.songEnd:
                    print('end',self.songEnd)
                    if self.selectedMode == 1:
                        self.endVs()
                        pygame.display.flip()
                        time.sleep(3)
                        self.scoreP1 = 0
                        self.scoreP2 = 0
                    else:
                        self.showHighScore()
                    pygame.mixer.music.set_endevent(self.k)
                    os.system("sudo ./Test")
                    self.arrowsP1 = []
                    self.arrowsP2 = []
                    self.countScreen = 1
                    self.scoreP1 = 0
                    self.scoreP2 = 0
                    self.songEnd = 0
                    self.selectedSong = 0
                    self.selectedMode = 0
                    self.song = ""
                    self.username = ""
                    

                    self.check = True
                    self.selectMode()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.countScreen != 3:
                        self.playSound(event)
                        if self.countScreen == 3:
                            self.songEnd = pygame.USEREVENT + 1
                            print('strat',self.songEnd+1)
                            if self.selectedSong == 0:
                                self.song = 'closer'
                            elif self.selectedSong == 1:
                                self.song = 'killthislove'
                            elif self.selectedSong == 2:
                                self.song = 'sunflower'
                            elif self.selectedSong == 3:
                                self.song = 'uptownfunk'
                            elif self.selectedSong == 4:
                                self.song = 'shape_of_you'
                            os.system("sudo ./Lab6")
                            pygame.mixer.music.set_endevent(self.songEnd)
                            pygame.mixer.music.load(self.song+'.mp3')
                            pygame.mixer.music.play()
                    if self.countScreen == 1:
                        if event.key == pygame.K_UP:
                            self.playSound(event)
                            self.selectedMode -= 1
                            if self.selectedMode == -1:
                                self.selectedMode = 1
                        elif event.key == pygame.K_DOWN:
                            self.playSound(event)
                            self.selectedMode += 1
                            if self.selectedMode == 2:
                                self.selectedMode = 0
                        self.selectMode()


                    elif self.countScreen == 2:
                        if event.key == pygame.K_UP:
                            self.playSound(event)
                            self.selectedSong -= 1
                            if self.selectedSong == -1:
                                self.selectedSong = 4
                        elif event.key == pygame.K_DOWN:
                            self.playSound(event)
                            self.selectedSong += 1
                            if self.selectedSong == 5:
                                self.selectedSong = 0
                        self.selectSongPage()


                if event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    self.width, self.height = self.screen.get_size()
                    self.setArrowArrange()
                    if self.countScreen == 0:
                        self.startPage()
                    elif self.countScreen == 1:
                        self.selectMode()
                    # elif self.countScreen == 1:
                    #     self.getNamePage()
                    #     pygame.draw.rect(self.screen, [239, 255, 226], self.input_box)
                    #     txt_surface = self.font.render(self.username, True, [0, 0, 0])
                    #     self.screen.blit(txt_surface, (self.input_box.x * 1.1, self.input_box.y * 1.05))
                    elif self.countScreen == 2:
                        self.selectSongPage()
                    pygame.display.flip()

                if event.type == QUIT:
                    pygame.display.quit()
            pygame.display.flip()


class Arrow:
    def __init__(self, direction, x, y, m, c):
        self.direction = direction
        self.speed = 40
        self.c = c
        self.m = m
        self.x = x
        self.y = y * 0.062037
        self.yEnd = y * 0.68703704

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def changeXY(self):
        self.y += self.speed
        self.x = (self.y - self.c) / self.m

    def changeSpeed(self):
        self.speed += 0.1

    def getDirection(self):
        return self.direction

    def checkElapse(self):
        if self.y > self.yEnd:
            return True
        return False


jdp = Gameplay()
jdp.run()


