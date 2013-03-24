from pydub import AudioSegment
import subprocess
import Queue
import sys
import os
# usage
# expected input *args=[file1, offset1, gain1]...[fileN, offsetN, gainN]
# concaac(*args) will place the file 'mix.aac' in current directory
# this file will be a concatenation of each of the files with their
# respective games at their respective offset times.
# gain is to be specified in dB between -30 and +10
def render(mix_id, *args):
    minimum = sys.maxint
    for arg in args:
        if arg[0] < minimum:
            minimum = arg[0]
    for arg in args:
        arg[0] -= minimum
    prio_queue = Queue.PriorityQueue()
    for arg in args:
        prio_queue.put(arg)
    base = prio_queue.get(0)
    base_track = AudioSegment.from_file(base[1], "m4a")
    gain = base[2]
    base_track = base_track.apply_gain(gain)
    while not prio_queue.empty():
        overlay = prio_queue.get(0)
        overlay_track = AudioSegment.from_file(overlay[1], "m4a")
        gain = overlay[2]
        if gain != 0:
            overlay_track = overlay_track.apply_gain(gain)
        base_track = base_track.overlay(overlay_track, position=overlay[0])
    base_track.export('mix.wav', format='wav')
    command = 'ffmpeg -b 66k -y -f wav -i ./mix.wav ./mix.aac'
    subprocess.call(command, shell=True)
    os.remove('mix.wav')

# concaac(mix_id, [0, "test1.m4a", 0], [5000, "test2.m4a", -10], [10000, "test3.m4a", 5])