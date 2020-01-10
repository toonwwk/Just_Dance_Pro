import cv2
import os
import pickle
import random
import time
import pygame
# from ffpyplayer.player import MediaPlayer

from components.arrow import Arrow
from components.circle import Circle

class MainGame:
    def __init__(self, n, s=10):
        self.filename = n
        self.speed = s
        self.color_palates = {'red': (56, 56, 192), 'green': (89, 169, 99), 'blue': (230, 174, 74),
                              'yellow': (83, 219, 237), 'white': (255, 255, 255), 'black': (0, 0, 0)}

        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'data')
        path = os.path.join(path, 'song')
        self.path = path
        print(path)

    def get_data(self, filename):
        with open(self.path + '/arrow/' + filename + '.pickle', 'rb') as f:
            song_time = pickle.load(f)
        
        print(self.path)
        
        print('load successfully')
        return song_time

    def run(self):
        video_path = self.path + '/song/doubt.mp3'
#         player = MediaPlayer(video_path)

        window_name = 'Just Dance'
        score = [0]
        start = time.time()

        capture = cv2.VideoCapture(0)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        capture.set(cv2.CAP_PROP_FPS, 60)
        print(width, height)
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        red_circle = Circle(60, 60, self.color_palates['red'], -1)
        blue_circle = Circle(width - 60, 60, self.color_palates['blue'], 1)
        green_circle = Circle(60, height - 60, self.color_palates['green'], -1)
        yellow_circle = Circle(width - 60, height - 60, self.color_palates['yellow'], 1)

        arrows = []
        circles = [red_circle, blue_circle, green_circle, yellow_circle]
        # convert the time in data to 1 decimal point and minus 5 for the time lost during ready
        song = ['%.1f' % (s - 5) for s in self.get_data(self.filename)]
        while capture.isOpened():
            current = time.time() - start
            if float(current) > float(song[-1]) + 5:
                print('dance done')
                break
            k = cv2.waitKey(33)
            if k == 27:
                break

            ret, frame = capture.read()
            fps = capture.get(cv2.CAP_PROP_FPS)
            # print('fps:', fps)

#             audio_frame, val = player.get_frame()
#             if val != 'eof' and audio_frame is not None:
                # audio
#                 img, t = audio_frame

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)

            for c in circles:
                c.display(frame)

            if current > 5:
                cv2.circle(frame, (width // 2, height // 2), 20, (255, 255, 255), -1)
#                 print('%.1f' % current, song[-1])
                # if the current time match the time in song then will create arrow
                if '%.1f' % current in song:
                    choice = random.choice(circles)
                    new_arrow = Arrow(width // 2, height // 2, choice.color, choice, self.speed, arrows)
                    arrows.append(new_arrow)

                for a in arrows:
                    a.display(frame, score)

                cv2.putText(frame, str(current - 5), (250, 405), cv2.FONT_ITALIC, 1, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                # if current time is less than 5 then show count down
                for c in circles:
                    c.origin_frame = frame
                random_color = random.choice(list(self.color_palates.keys()))
                cv2.putText(frame, str(5 - int(current)), (270, height // 2 + 50), cv2.FONT_ITALIC, 5,
                            self.color_palates[random_color], 5, cv2.LINE_AA)

            cv2.putText(frame, 'Score: ' + str(score[0]), (250, 75), cv2.FONT_ITALIC, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow(window_name, frame)

        capture.release()
        time.sleep(3)
        cv2.destroyAllWindows()
        return score[0]


#if __name__ == '__main__':
    # base path for current file, to play game there must be data for the song in the /data/song
#    song_name = 'doubt'

#    game = MainGame(song_name)
#    game.run()  # if the main game is finish then the song should stop
#    print('song stop')