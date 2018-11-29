from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label

import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
watch_cascade = cv2.CascadeClassifier('watch_cascade.xml')
knife_cascade = cv2.CascadeClassifier('knife_cascade.xml')
class CameraApp(App):

    def build(self):
        self.img1 = Image(source='logoCL',size_hint=(200,200),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label1 = Label(text="Gun and Ammunication")
        label2 = Label(text="www.cadernodelaboratorio.com.br")
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(label1)
        layout.add_widget(self.img1)
        layout.add_widget(label2)

        self.capture = cv2.VideoCapture(0)
        ret, img = self.capture.read()
        Clock.schedule_interval(self.atualizaImagem,
                                1.0 / 30.0)
        return layout

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

        self.img1.texture = texture1



if __name__ == '__main__':
    CameraApp().run()