from kivy.core.window import Window
from kivymd.app import MDApp
import kivy

from kivy.uix.button import Button
from threading import Thread
import pyaudio
import wave

from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (350, 300)

class AudioRecorderApp(MDApp):
    # Function to record audio
    def record_audio(self, event):
        # Set the format_type type and the sample rate
        format_type = pyaudio.paInt16 # 16-bit resolution
        rate = 44100
        chunk = 1024
        channels = 2
        seconds = 5

        # Create an instance of the pyaudio class
        audio = pyaudio.PyAudio()

        # Open the audio stream
        stream = audio.open(format=format_type, channels=channels,
                            rate=rate, input=True,
                            frames_per_buffer=chunk)

        frames = []

        # Record audio for a given number of seconds
        for i in range(0, int(rate / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Close the audio stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the audio to a file
        waveFile = wave.open('output.wav', 'wb')
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audio.get_sample_size(format_type))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def start_recording(self, instance):
        # Create a new thread to record audio
        self.record_thread = Thread(target=self.record_audio)
        self.record_thread.start()

    def stop_recording(self, instance):
        pass

    def build(self):

        layout = MDRelativeLayout(md_bg_color=(173 / 255, 181 / 255, 189 / 255, 1))



        # Add your layout here
        self.record_button = Button(text='Record', pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                    size_hint=(0.4, 0.3), on_press=self.start_recording, bold=True,
                                    background_color=(52 / 255, 58 / 255, 64 / 255, 1))
        self.stop_button = Button(text='Stop Recording', pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                    size_hint=(0.7, 0.3), on_press=self.stop_recording, bold=True,
                                    background_color=(52 / 255, 58 / 255, 64 / 255, 1), disabled=True)

        layout.add_widget(self.record_button)
        layout.add_widget(self.stop_button)

        return layout

if __name__ == '__main__':
    AudioRecorderApp().run()