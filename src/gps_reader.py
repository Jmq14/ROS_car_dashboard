#!/usr/bin/env python

import rospy
from nmea_msgs.msg import Sentence
import numpy as np

x0 = np.nan
y0 = np.nan

def parse_gps(data):
    global x0
    global y0
    s = data.sentence
    if s.startswith('<'): 
        info = s[1:].strip().split(' ')
        if info[0] == 'SOL_COMPUTED':
            status = info[1]
            latitude = float(info[2])
            longitude = float(info[3])
            altitude = float(info[4])
            
            accuracy = (float(info[7]), float(info[8]), float(info[9]))
            
#            if status == 'PPP':
#                print 'gps data is accurate now!'
#                print '{{lat: {}, lng: {}}},'.format(latitude, longitude)
#            elif status == 'PPP_CONVERGING':
#                print 'gps data is converging! Current accuracy is {}'.format(accuracy)
#                print '{{lat: {}, lng: {}}},'.format(latitude, longitude)
#            elif status == 'SINGLE':
#                print 'gps data is invalid!'


            # calculate x, y, z in local coordinates
            cosLat = np.cos(np.radians(latitude))
            sinLat = np.sin(np.radians(latitude))
            cosLon = np.cos(np.radians(longitude))
            sinLon = np.sin(np.radians(longitude))

            rad = 6378137.0  # earth radius
            f = 1.0 / 298.257224  # flattening
            C = 1.0 / np.sqrt(cosLat * cosLat + (1.0-f) * (1.0-f) * sinLat * sinLat)
            S = (1.0-f) * (1.0-f) * C
            
            x = (rad * C + altitude) * cosLat * cosLon
            y = (rad * C + altitude) * cosLat * sinLon
            
            if np.isnan(x0) and np.isnan(y0):
                x0 = x
                y0 = y
                x = 0
                y = 0
            else:
                x = x - x0
                y = y - y0

            print '({}, {})'.format(x, y)


#s = '<     SOL_COMPUTED PPP_CONVERGING 37.91582244278 -122.32797679330 8.6851 -32.2000 WGS84 0.5335 0.2868 0.5955 "TSTR" 151.500 0.000 14 13 13 11 00 00 00 33'
# parse_gps(s)


rospy.init_node('gps_parsing')
rospy.Subscriber('/nmea_sentence', Sentence, parse_gps)
rospy.spin()
