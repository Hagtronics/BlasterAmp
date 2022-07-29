"""This script uses SciPy and produces a high quality, 16 bit, WAV file to disk.

If you are going to be 'looping' the audio file, make sure that the start and end
of the WAV file data does not contain any discontinuities, or there will be a
"Burp" when the WAV file loops.

Written By Steve Hageman, July 2022
Total Freeware, but beware this was written by an infinite number of Monkeys on an 
infinite number of Laptops, so it probably contains errors....
"""

import numpy as np
from scipy.io.wavfile import write

# Inputs
file_name = "test.wav"
duration = 100          # Seconds
sample_rate = 44100     # Bitrate Samples per second
tone_freq = 2000        # Hz


# Code
t = np.linspace(0., 1., sample_rate * duration)

amplitude = np.iinfo(np.int32).max

data = amplitude * np.sin(2. * np.pi * tone_freq * t * duration)

write(file_name, sample_rate, data.astype(np.int32))
