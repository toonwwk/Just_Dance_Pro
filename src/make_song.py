import cv2
import os
import pickle
import random
import time
from ffpyplayer.player import MediaPlayer


class MakeSong:
    def __init__(self, f):
        self.filename = f
        self.color_palates = {'red': (56, 56, 192), 'green': (89, 169, 99), 'blue': (230, 174, 74),
                              'yellow': (83, 219, 237), 'white': (255, 255, 255), 'black': (0, 0, 0)}
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'data')
        path = os.path.join(path, 'song')
        self.path = path

    def save_data(self, data, filename):
        with open(self.path + '/arrow/' + filename + '.pickle', 'wb') as f:
            pickle.dump(data, f)
        print('complete')

    def make_song(self):
        video_path = self.path + '/song/doubt.mp3'
        player = MediaPlayer(video_path)
        window_name = 'Just Dance'
        start = time.time()
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FPS, 60)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        time_list = [197]

        while capture.isOpened():
            audio_frame, val = player.get_frame()
            if val != 'eof' and audio_frame is not None:
                # audio
                img, t = audio_frame

            k = cv2.waitKey(33)
            if k == 27:
                break

            ret, frame = capture.read()

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)

            current = time.time() - start

            if current > 10:
                if k == ord('a'):
                    time_list.append(current)

                cv2.putText(frame, str(current), (width // 2, 605), cv2.FONT_ITALIC, 1, (0, 0, 0), 2, cv2.LINE_AA)
            else:
                random_color = random.choice(list(self.color_palates.keys()))
                cv2.putText(frame, str(10 - int(current)), (540, height // 2 + 50), cv2.FONT_ITALIC, 10,
                            self.color_palates[random_color], 10, cv2.LINE_AA)

            cv2.imshow(window_name, frame)

        capture.release()
        cv2.destroyAllWindows()
        self.save_data(time_list, self.filename)


if __name__ == '__main__':
    # make each arrow by pressing 'a' button then will save current time to the data file
    # when the screen is released the time data in time_list will automatically save to the /song accroding to the name of song
    song = MakeSong('doubt')
    song.make_song()