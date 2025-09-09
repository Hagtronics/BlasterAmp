"""

**** This generates a High Quality 16 Bit Audio Tone Though a Sound Blaster USB Dongle *****

Code based on this Internet thread,

    https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound

    The soundfile module (https://PySoundFile.readthedocs.io/) has to be installed!

    The official installer is broken (as of March 2022), the install fix and replacement wheel file is shown here in this video,
    https://www.youtube.com/watch?v=t6zdZIT4MNA
    
    The fixed wheel files are here,
    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio


    Totally free script, but remember,
        "Written by an infinite number of Monkeys in an infinite amount of time,
        ...so beware."

"""

#from tkinter.constants import FALSE
import pyaudio
import struct
import math
import threading
import time
import FreeSimpleGUI as sg


# Setup audio stream
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Instantiate PyAudio
pa = pyaudio.PyAudio()

# Global Flag
is_playing = False


# Local Methods
def data_for_tone(frequency: float, time: float = None, volume: float = 1.0):
    """get frames for a fixed frequency for a specified time or
    number of frames, if frame_count is specified, the specified
    time is ignored"""
    frame_count = int(RATE * time)

    # limit volume
    if volume > 1.0:
        volume = 1.0

    remainder_frames = frame_count % RATE
    wavedata = []

    for i in range(frame_count):
        a = RATE / frequency  # number of frames per wave
        b = i / a
        # explanation for b
        # considering one wave, what part of the wave should this be
        # if we graph the sine wave in a
        # displacement vs i graph for the particle
        # where 0 is the beginning of the sine wave and
        # 1 the end of the sine wave
        # which part is "i" is denoted by b
        # for clarity you might use
        # though this is redundant since math.sin is a looping function
        # b = b - int(b)

        c = b * (1.0 * math.pi)
        # explanation for c
        # now we map b to between 0 and 2*math.PI
        # since 0 - 2*PI, 2*PI - 4*PI, ...
        # are the repeating domains of the sin wave (so the decimal values will
        # also be mapped accordingly,
        # and the integral values will be multiplied
        # by 2*PI and since sin(n*2*PI) is zero where n is an integer)
        d = math.sin(c) * 32767 * volume
        e = int(d)
        wavedata.append(e)

    for i in range(remainder_frames):
        wavedata.append(0)

    number_of_bytes = str(len(wavedata))
    wavedata = struct.pack(number_of_bytes + 'h', *wavedata)

    return wavedata



def play():
    # This is the actual play-loop thread
    global is_playing
    global stream
    global frame_data

    while(is_playing == True):
        stream.write(frame_data)

    # Clean up streams on playing stop
    stream.stop_stream()
    stream.close()



def loop_start(frequency, volume):
    global is_playing
    global stream
    global frame_data

    if is_playing == False:

        frame_data = data_for_tone(frequency=frequency, time=1, volume=volume)

        stream = pa.open(format=FORMAT, channels=CHANNELS,
                         rate=RATE, output=True)

        is_playing = True
        audio_loop_thread = threading.Thread(target=play)
        audio_loop_thread.start()



def loop_stop():
    global is_playing
    is_playing = False



if __name__ == "__main__":

    # GUI Layout Design
    layout = [[sg.Text('Frequency Hz')],
              [sg.Slider(orientation='horizontal', key='Frequency', enable_events=True, range=(1000, 10000), resolution=1000, default_value=2000, size=(60, 20))],
              [sg.Text('')],
              [sg.Text('Volume %')],
              [sg.Slider(orientation='horizontal', key='Volume', enable_events=True, range=(1, 100), resolution=1, default_value=50, size=(60, 20))],
              [sg.Text('')],
              [sg.Button('Play', size=(10, 1)), sg.Button('Stop', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
              ]

    # GUI Window Design
    window = sg.Window('Play A High Quality Tone With Python', layout,
                       default_element_size=(12, 1),
                       text_justification='l',
                       auto_size_text=False,
                       auto_size_buttons=False,
                       keep_on_top=True,
                       grab_anywhere=False,
                       default_button_element_size=(12, 1),
                       finalize=True)


    # GUI Initial Conditions
    window['Stop'].update(disabled=True)

    # GUI Window Event Loop
    while True:

        # Read any window events
        event, values = window.Read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            loop_stop()
            break

        if event == 'Play':
            window['Stop'].update(disabled=False)
            window['Play'].update(disabled=True)
            frequency = int(values['Frequency'])
            volume = float(values['Volume'] / 100.0)
            loop_start(frequency, volume)
            continue

        if event == 'Stop':
            window['Stop'].update(disabled=True)
            window['Play'].update(disabled=False)
            loop_stop()
            continue

        if event == 'Frequency':
            window['Stop'].update(disabled=True)
            window['Play'].update(disabled=False)
            loop_stop()
            continue

        if event == 'Volume':
            window['Stop'].update(disabled=True)
            window['Play'].update(disabled=False)
            loop_stop()
            continue


    # GUI Exit
    window.Close()

    # ----- Fini -----

