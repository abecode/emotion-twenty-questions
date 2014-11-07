#!/usr/bin/python


""" 
lists audio devices
"""

import _portaudio as pa

def listAudioDevices(devNum=None):
    pa.initialize()
    if not devNum:
        for x in range(pa.get_device_count()):
            dev = pa.get_device_info(x)
            print x, dev.name

    else:
        dev = pa.get_device_info(devNum)
        print "device number", devNum, "(", dev.name, ")"
        for y in ["name","structVersion","hostApi","maxInputChannels","maxOutputChannels","defaultLowInputLatency","defaultHighInputLatency","defaultLowOutputLatency","defaultHighOutputLatency"]:
            print "\t", y, ":", dev.__getattribute__(y)

if __name__ == "__main__":

    import sys
    try:
        listAudioDevices(int(sys.argv[1]))
    except IndexError:
        listAudioDevices()


