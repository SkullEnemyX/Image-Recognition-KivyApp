from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color,Rectangle
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics','resizable','1')
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
import os
import cv2
import numpy as np
import urllib.request
import bs4 as bs
import requests



status='p'
Builder.load_file(os.path.abspath("amazon.kv"))
#Initialize
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
watch_cascade = cv2.CascadeClassifier('watch_cascade.xml')
knife_cascade = cv2.CascadeClassifier('knife_cascade.xml')
rcube_cascade = cv2.CascadeClassifier(r"C:\Users\Vineet Kishore\PycharmProjects\ImageSVK\rcube_cascade.xml")
#sharp_cascade = cv2.CascadeClassifier('sharp_cascade.xml')
#id_cascade = cv2.CascadeClassifier('id_cascade.xml')

class StartScreen(Screen):

    def on_pre_enter(self):
        Window._set_window_pos(0, 10)
        Window.maximize()
        Window.size = (1920, 1080)
    def __init__(self,**kwargs):
        super(StartScreen,self).__init__(**kwargs)
        self.img1 = Image(source='logoCLA', size_hint=(30, 30), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout = FloatLayout()
        layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)
        ret, img = self.capture.read()
        self.add_widget(layout)
        Clock.schedule_interval(self.atualizaImagem,1.0 / 30.0)

    def atualizaImagem(self, dt):
        ret, img = self.capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        watch = watch_cascade.detectMultiScale(gray, 1.85, 6)
        rcube = rcube_cascade.detectMultiScale(gray, 1.9, 4)
        #sharp = sharp_cascade.detectMultiScale(gray, 2.5, 3)
        #id = id_cascade.detectMultiScale(gray, 1.28, 5)
        # knife = knife_cascade.detectMultiScale(gray, 55, 11)
        '''for (x,y,w,h) in knife:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,'Knife', (x-w, y-h), font,1, (110,255,255),2,cv2.LINE_AA)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,115,0),2)
    '''

        '''for (x,y,w,h) in sharp:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,'Sharp', (x-w, y-h), font,1, (0,0,255),2,cv2.LINE_AA)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        
        for (x, y, w, h) in id:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'ID', (x - w, y - h), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (102, 255, 255), 2)'''

        for (x, y, w, h) in rcube:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'Rcube', (x - w, y - h), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

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

class GameScreen(Screen):
    def __init__(self,**kwargs):
        super(GameScreen,self).__init__(**kwargs)

    def on_pre_enter(self):
        Window.maximize()
        Window.size = (1920,1080)
        Window._set_window_pos(0,10)


    def check(self,*args):
        research_later = str(self.ids.pink.text)
        goog_search = "https://www.google.co.in/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + research_later + "Wikipedia"
        r = requests.get(goog_search)
        soup = bs.BeautifulSoup(r.text, "html.parser")
        website = soup.find('cite').text
        # website = input('Enter a website you want to visit: ')
        if 'wikipedia' in website:
            if 'https://' in website:
                website = list(website)
                for i in range(len(website)):
                    if website[i] == 's':
                        website.remove('s')
                        break
                website = ''.join(map(str, website))

                # print(website)
                response = urllib.request.urlopen(website, timeout=10).read().decode('UTF-8')
            elif 'http://' not in website:
                response = urllib.request.urlopen('http://' + website, timeout=10).read()
            else:
                response = urllib.request.urlopen(website, timeout=10).read()

            soup = bs.BeautifulSoup(response, 'lxml')

            l = []

            def infobox():
                table = soup.find('table', {'class': 'infobox vcard'})
                for tr in table.findAll('tr'):
                    l.append(tr.text)


                with open("chapde.txt", "w") as f:
                    for i in l:
                        f.write(str(i.encode('utf-8')) + '\r\n')

                imgs = soup.findAll('img')
                list_of_image = []
                for img in imgs:
                    list_of_image.append(img['src'])
                image_link1 = list_of_image[3][2:]
                image_link2 = list_of_image[2][2:]
                image_link1 = image_link1.replace("'", '"')
                image_link2 = image_link2.replace("'", '"')
                image = urllib.request.URLopener()
                urllib.request.urlretrieve("http://" + image_link1, research_later + "1" + '.jpg')
                urllib.request.urlretrieve("http://" + image_link2, research_later + "2" + '.jpg')

            infobox()
        else:
            print('Relative wikipedia website not found! Recheck again')
            # print(soup.prettify())

        with open("Output.txt", "r") as fob:
            self.ids.view.text = fob.readlines()

        #self.ids.view.text = [line.rstrip('\n') for line in open('Output.txt',"r")]
    def game(self,*args):
        texts = self.ids.pink.text
        print(type(texts))
        self.ids.view.text = texts


class RootScreen(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        self.title=("Gun Detection")
        return RootScreen()

if __name__ == "__main__":
    MainApp().run()