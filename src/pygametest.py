import pygame, sys
import sqlite3

from pygame.locals import *

pygame.camera.init()
cameras = pygame.camera.list_cameras()

checkScreen = 0
selectedSong = 0

pygame.init()
screen = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF | RESIZABLE)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


start = pygame.image.load("background.png")
start2 = pygame.image.load("background2.png")
start3 = pygame.image.load("background3.png")
start4 = pygame.image.load("background4.png")

name = pygame.image.load("nameEnter.png").convert_alpha()
songSelect = pygame.image.load("songSelect.png").convert_alpha()
songSelected = pygame.image.load("songSelected.png").convert_alpha()
songName = pygame.image.load("songName.png").convert_alpha()

username = ''
font = pygame.font.SysFont(None, 40)
score = 550

screen.blit(pygame.transform.scale(start, (800, 600)), (0, 0))
pygame.display.flip()
#pygame.font.SysFont('Comic Sans MS', 30)

while True:
    pygame.event.pump()
    event = pygame.event.wait()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and checkScreen == 0:
            pygame.mixer.music.load('enter.mp3')
            pygame.mixer.music.play()
            width, height = screen.get_size()
            temp = height
            input_box = pygame.Rect(width*0.35732188, height*0.49333358, width*0.28480312, height*0.08739076)
            screen.blit(pygame.transform.scale(start2, (width, height)), (0, 0))
            while(temp > 0):
                screen.blit(pygame.transform.scale(name, (width, height)), (0, temp))
                pygame.display.flip()
                temp -= 60
            screen.blit(pygame.transform.scale(start2, (width, height)), (0, 0))
            screen.blit(pygame.transform.scale(name, (width, height)), (0, 0))
            pygame.draw.rect(screen, [239, 255, 226], input_box)
            pygame.display.flip()
            checkScreen += 1

        elif checkScreen == 1:
            if event.key == pygame.K_RETURN:
                pygame.mixer.music.load('enter.mp3')
                pygame.mixer.music.play()
                screen.blit(pygame.transform.scale(start3, (width, height)), (0, 0))
                yPlus = 0
                for i in range(5):
                    if i == selectedSong:
                        screen.blit(pygame.transform.scale(songSelected, (round(width*0.50364583), round(height*0.09074074))), (width*0.24791667, height*0.25722222+ yPlus))
                    else:
                        screen.blit(pygame.transform.scale(songSelect, (round(width*0.50364583), round(height*0.09074074))), (width*0.24791667, height*0.25722222 + yPlus))
                    yPlus += height*0.12962963
                screen.blit(pygame.transform.scale(songName, (width, height)), (0, 0))
                pygame.display.flip()
                checkScreen += 1
            else:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                    print(username)
                elif len(username) <= 10:
                    username += event.unicode
                txt_surface = font.render(username, True, [0, 0, 0])
                pygame.draw.rect(screen, [239, 255, 226], input_box)
                screen.blit(txt_surface, (input_box.x * 1.1, input_box.y * 1.05))
                pygame.display.flip()


        elif checkScreen == 2 :

            if event.key == pygame.K_RETURN:
                pygame.mixer.music.load('enter.mp3')
                pygame.mixer.music.play()
                screen.blit(pygame.transform.scale(start4, (width, height)), (0, 0))
                checkScreen += 1

                ##-----------------------------------------------------------------------
                ##------------------------------START CAMERA ----------------------------
                ##-----------------------------------------------------------------------


            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                width, height = screen.get_size()
                pygame.mixer.music.load('select.wav')
                pygame.mixer.music.play()
                if event.key == pygame.K_UP:
                    selectedSong -= 1
                    if selectedSong == -1:
                        selectedSong = 4
                if event.key == pygame.K_DOWN:
                    selectedSong += 1
                    if selectedSong == 5:
                        selectedSong = 4

                screen.blit(pygame.transform.scale(start3, (width, height)), (0, 0))
                yPlus = 0
                for i in range(5):
                    if i == selectedSong:
                        screen.blit(
                            pygame.transform.scale(songSelected,
                                                   (round(width * 0.50364583), round(height * 0.09074074))),
                            (width * 0.24791667, height * 0.24722222 + yPlus))
                    else:
                        screen.blit(
                            pygame.transform.scale(songSelect, (round(width * 0.50364583), round(height * 0.09074074))),
                            (width * 0.24791667, height * 0.24722222 + yPlus))
                    yPlus += height * 0.12962963
                screen.blit(pygame.transform.scale(songName, (width, height)), (0, 0))
                pygame.display.flip()





    if event.type == QUIT:
        pygame.display.quit()
    elif event.type == VIDEORESIZE:
        screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        width, height = screen.get_size()

        if(checkScreen == 0):
            screen.blit(pygame.transform.scale(start, event.dict['size']), (0, 0))
        if(checkScreen == 1):
            input_box = pygame.Rect(width * 0.35732188, height * 0.49333358, width * 0.28480312, height * 0.08739076)
            screen.blit(pygame.transform.scale(start2, event.dict['size']), name.get_rect())
            screen.blit(pygame.transform.scale(name, event.dict['size']), name.get_rect())
            pygame.draw.rect(screen, [239, 255, 226], input_box)
            txt_surface = font.render(username, True, [0, 0, 0])
            screen.blit(txt_surface, (input_box.x * 1.1, input_box.y * 1.05))
        if (checkScreen == 2):
            screen.blit(pygame.transform.scale(start3, (width, height)), (0, 0))
            yPlus = 0
            for i in range(5):
                if i == selectedSong:
                    screen.blit(
                        pygame.transform.scale(songSelected, (round(width * 0.50364583), round(height * 0.09074074))),
                        (width * 0.24791667, height * 0.24722222 + yPlus))
                else:
                    screen.blit(
                        pygame.transform.scale(songSelect, (round(width * 0.50364583), round(height * 0.09074074))),
                        (width * 0.24791667, height * 0.24722222 + yPlus))
                yPlus += height * 0.12962963
            screen.blit(pygame.transform.scale(songName, (width, height)), (0, 0))
            pygame.display.flip()
        pygame.display.flip()
pygame.quit()

