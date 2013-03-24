from pylab import *
import scikits.audiolab as audiolab
from pydub import AudioSegment
import os
# usage
# call sound_wave('song.extenstion')
# wave form of song saved as 'wave_form.png' in current directory
def sound_wave(songFile):
    setup(songFile)
    sound_wav()
    teardown()

#implementation
def setup(songFile):
    if songFile.endswith('.wav'):
        song = AudioSegment.from_file(songFile, "wav")
    else:
        song = AudioSegment.from_file(songFile, "m4a")
    wave_song = song.export('temp.wav', format='wav')

def teardown():
    os.remove('temp.wav')

def sound_wav():
    clf()
    (snd, sampFreq, nBits) = audiolab.wavread('temp.wav')
    wave_form = []
    signal = snd[:,0]
    if (len(signal)) < 500000:
        timeArray = arange(0, float(len(signal)), 1)
        timeArray = timeArray / sampFreq
        wave_form = signal
    else:
        downsample_factor = len(signal) / 30000
        i = 0
        while i < len(signal):
            wave_form = wave_form + [signal[i]]
            i = i + downsample_factor
        timeArray = arange(0, float(len(wave_form)), 1)
        timeArray = timeArray * downsample_factor / sampFreq
    timeArray = timeArray * 1000
    plot(timeArray, wave_form, color='k')
    ylabel('Amplitude')
    xlabel('Time (ms)')
    savefig('wave_form.png', bbox_inches=0)
    # show()
# setup('skream.wav')
# sound_wav()
# teardown()