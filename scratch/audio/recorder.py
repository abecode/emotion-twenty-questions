#!/usr/bin/python


""" 
Record a audio and save to a WAVE file.
cf, http://people.csail.mit.edu/hubert/pyaudio/

"""
import pyaudio
import wave
import sys

import signal
def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    raise IOError()
    #sys.exit(0)
    #StopIteration()

signal.signal(signal.SIGINT, signal_handler)

# print 'Press Ctrl+C'
# while True:
#     continue
 
#chunk = 1024
chunk = 160000
#chunk = 256
FORMAT = pyaudio.paInt16
CHANNELS = 2
#RATE = 44100
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

try:
    devNum = int(sys.argv[1])
except IndexError:
    devNum = None

print devNum
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk,
                input_device_index = devNum
                )

print "* recording"
all = []
#for i in range(0, RATE / chunk * RECORD_SECONDS):

#open output file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)

try:
    while True:
        #print "whoa"
        print stream.get_read_available()
        #data = stream.read(stream.get_read_available())
        data = stream.read(chunk)
        wf.writeframes(data) # write data to WAVE file
        
except IOError, e:
    print e
    print "* done recording"
    stream.close()
    p.terminate()
    wf.close()


#wf.writeframes(data)


#next, upload to couchdb
