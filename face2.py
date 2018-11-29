from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.lang import Builder
import os
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color,Rectangle
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics','resizable','1')
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
import cv2
import numpy as np
status='p'
Builder.load_file(os.path.abspath("amazon.kv"))
#Initialize
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
watch_cascade = cv2.CascadeClassifier('watch_cascade.xml')
knife_cascade = cv2.CascadeClassifier('knife_cascade.xml')

class StartScreen(Screen):

    def on_pre_enter(self):
        Window._set_window_pos(0, 10)
        Window.maximize()
        Window.size = (1920, 1080)
    def __init__(self,**kwargs):
        super(StartScreen,self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        ret, img = self.capture.read()
        Clock.schedule_interval(self.atualizaImagem,1.0 / 30.0)
    def pause(self,status):
        print('hello')


    def atualizaImagem(self, dt):
        ret, img = self.capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 2, 5)
        watch = watch_cascade.detectMultiScale(gray, 6, 6)
        knife = knife_cascade.detectMultiScale(gray, 55, 11)
        for (x, y, w, h) in knife:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'Knife', (x - w, y - h), font, 1, (110, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 115, 0), 2)

        for (x, y, w, h) in watch:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'Watch', (x - w, y - h), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()

        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.texture = texture1
class GameScreen(Screen):
    def on_pre_enter(self):
        Window.maximize()
        Window.size = (1920,1080)
        Window._set_window_pos(0,10)

class RootScreen(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootScreen()

if __name__ == "__main__":
    MainApp().run()