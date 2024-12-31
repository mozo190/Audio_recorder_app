import os
import time
import wave
from threading import Thread

import pyaudio
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (350, 300)


class AudioRecorderApp(MDApp):
    # Function to record audio
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.record_thread = None
        self.durations_time_label = None
        self.stop_button = None
        self.record_button = None
        self.recording_active = None

    def record_audio(self):
        self.recording_active = True
        self.record_button.text = 'Recording...'
        # Set the format type and the sample rate
        format = pyaudio.paInt16  # 16-bit resolution
        rate = 44100
        chunk = 1024
        channels = 1

        # Create an instance of the pyaudio class
        audio = pyaudio.PyAudio()

        # Try to open the audio stream
        try:
            stream = audio.open(format=format, channels=channels,
                                rate=rate, input=True,
                                frames_per_buffer=chunk)
        except Exception as e:
            print(f"Error initializing audio stream: {e}")
            return

        frames = []
        start_time = time.time()

        # Record audio for a given number of seconds
        try:
            while self.recording_active:
                elapsed_time = time.time() - start_time
                self.durations_time_label.text = f'Duration: {int(elapsed_time // 60)}:{int(elapsed_time % 60):02d}'

                data = stream.read(chunk)
                frames.append(data)
        except Exception as e:
            print(f"Error recording audio: {e}")
        finally:
            # Close the audio stream
            stream.stop_stream()
            stream.close()
            audio.terminate()

        print('Recording complete')

        # Save the audio to a file
        os.makedirs('assets/audio', exist_ok=True)
        waveFile = wave.open('assets/audio/output.wav', 'wb')
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audio.get_sample_size(format))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def start_recording(self, instance):
        # Create a new thread to record audio
        self.record_thread = Thread(target=self.record_audio)
        self.record_thread.start()

        # Enable the stop button
        self.stop_button.disabled = False
        # Disable the record button
        self.record_button.disabled = True

    def stop_recording(self, instance):
        self.recording_active = False
        if self.record_thread and self.record_thread.is_alive():
            # Stop the recording thread
            self.record_thread.join()

        # Disable the stop button
        self.stop_button.disabled = True
        # Enable the record button
        self.record_button.disabled = False

    def build(self):
        self.recording_active = False

        layout = MDRelativeLayout(md_bg_color=(173 / 255, 181 / 255, 189 / 255, 1))

        # Add your layout here
        self.record_button = Button(text='Record', pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                    size_hint=(0.4, 0.3), on_press=self.start_recording, bold=True,
                                    background_color=(52 / 255, 58 / 255, 64 / 255, 1))
        self.stop_button = Button(text='Stop Recording', pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                  size_hint=(0.7, 0.3), on_press=self.stop_recording, bold=True,
                                  background_color=(52 / 255, 58 / 255, 64 / 255, 1), disabled=True)
        self.durations_time_label = Label(text='Duration: 0:00', pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                          font_size=20)

        layout.add_widget(self.record_button)
        layout.add_widget(self.durations_time_label)
        layout.add_widget(self.stop_button)

        return layout


if __name__ == '__main__':
    AudioRecorderApp().run()
