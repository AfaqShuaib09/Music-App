import math
import os
import eyed3
from mutagen.mp3 import MP3
import pygame
import kivy
import kivy.animation
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Animation, Window
from kivy.properties import NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout

music_list = list()
img_list = list()
global list_index 
list_index = 0

def load_music_files():
    songs = 0
    path = os.getcwd()
    if os.path.exists(f'{path}/Music'):
        # Change the current working Directory
        os.chdir(f'{path}/Music')
    file_path = None
    for file in os.listdir():
        if file.endswith(".wav") or file.endswith('.mp3'):
            file_path = f'{path}\{file}'
            music_list.append(file)
    # if os.path.exists(f'{path}/'):
    #     # Change the current working Directory
    #     os.chdir(f'{path}/Music')
    for file in os.listdir():
        if file.endswith(".jpg") or file.endswith('.png'):
            file_path = f'{path}\{file}'
            img_list.append(file)
    print(img_list)
    
            

Window.size = (320, 600)
class MusicScreen(Screen):
    pass

class SongCover(MDBoxLayout):
    music_player_state = 0
    music_time_span = 0.0
    list_index_mp = 0
    no_of_songs = 5
    angle = NumericProperty()
    anim = kivy.animation.Animation(angle= 360, d=3, t="linear")
    anim += kivy.animation.Animation(angle=0, d=0, t="linear")
    anim.repeat = True

    progress = kivy.animation.Animation(value= 100, d=100, t="linear")
    
    def rotate(self):
        if self.anim.have_properties_to_animate(self):
            self.anim.stop(self)
            self.progress.stop(self.widget)
        else:
            self.anim.start(self)
            self.progress.start(self.widget)
    def play(self, widget, widget2, widget3, widget4):
        if self.music_player_state == 0:
            self.music_player_state = 1
            self.widget = widget
            print(self.list_index_mp)
            file_name = music_list[self.list_index_mp]
            img_file = img_list[self.list_index_mp]
            audiofile = eyed3.load(f'{os.getcwd()}/{file_name}')
            widget2.text = file_name[:-4]
            widget3.text = audiofile.tag.artist
            audio = MP3(f'{os.getcwd()}/{file_name}')
            self.music_time_span = float(audio.info.length)
            widget.value = 0
            widget.min = 0
            widget.max = math.ceil(int(audio.info.length))
            widget4.source = f'Music/{img_file}'
            pygame.mixer.init()
            pygame.mixer.music.load(f'{os.getcwd()}/{file_name}')
            pygame.mixer.music.play(loops=0, start=0.0)
            self.progress.start(widget)
            self.rotate()
        elif self.music_player_state==1:
            self.music_player_state =2
            pygame.mixer.music.pause()
            self.rotate()
        elif self.music_player_state == 2:
            self.music_player_state =1
            pygame.mixer.music.unpause()
            self.rotate()
    def restart(self, widget):
        self.rotate()
        widget.value = 0
        pygame.mixer.music.rewind()
        self.rotate()
    def skip_ten_sec(self, widget):
        self.rotate()
        run_time = float(pygame.mixer.music.get_pos())/1000
        if run_time-10 < 0 :
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            #pygame.mixer.music.set_pos(float(0.0))
            widget.value = 0
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.play(loops=0, start=run_time-10)
            #pygame.mixer.music.set_pos(run_time-10)
            widget.value = run_time-10
        self.rotate()

    def forward_ten_sec(self, widget):
        self.rotate()
        print(float(pygame.mixer.music.get_pos())/1000)
        run_time = float(pygame.mixer.music.get_pos())/1000
        if run_time + 10 < self.music_time_span :
            pygame.mixer.music.set_pos(run_time+10)
            widget.value = run_time + 10
            self.rotate()
        else:
            pygame.mixer.music.stop()
            widget.value = widget.max
    
    def previous_song(self, widget, widget1, widget2, widget3):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.music_player_state = 0
        self.list_index_mp = (self.list_index_mp +self.no_of_songs-1)% self.no_of_songs
        self.play(widget,widget1,widget2,widget3)

    def next_song(self, widget, widget1, widget2, widget3):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.music_player_state = 0
        self.list_index_mp = (self.list_index_mp + 1)% self.no_of_songs
        self.play(widget,widget1,widget2, widget3)


class MainApp(MDApp):
    def build(self):
        MDApp.title = 'My Music App'
        return MusicScreen()


if __name__ == "__main__":
    load_music_files()
    MainApp().run()