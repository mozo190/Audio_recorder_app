from kivy.core.window import Window
from kivymd.app import MDApp
import kivy
from kivy.uix.relativelayout import RelativeLayout

from kivy.uix.button import Button
from threading import Thread
import pyaudio
import wave

from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (350, 300)

class AudioRecorderApp(MDApp):
    def start_recording(self, instance):
        pass

    def build(self):

        layout = MDRelativeLayout(md_bg_color=(173 / 255, 181 / 255, 189 / 255, 1))



        # Add your layout here
        self.record_button = Button(text='Record', pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                    size_hint=(0.3, 0.1), on_press=self.start_recording, bold=True,
                                    background_color=(52 / 255, 58 / 255, 64 / 255, 1))


        layout.add_widget(self.record_button)

        return layout

if __name__ == '__main__':
    AudioRecorderApp().run()