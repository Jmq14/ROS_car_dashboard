import rospy
from sensor_msgs.msg import *
from dbw_mkz_msgs.msg import *

def left_camera_sender(data):
    print 'left camera: ' + str(data.header.stamp.secs) + ', ' + str(data.header.stamp.nsecs)

def steer_sender(data):
    print 'steering   : ' + str(data.header.stamp.secs) + ', ' + str(data.header.stamp.nsecs)



rospy.init_node('monitor', anonymous=True) 
left_camera_name  = '/left_camera/pg_16492265/image_color_flipped/compressed'
right_camera_name = '/right_camera/pg_16492281/image_color_flipped/compressed'
compressed = True

brake_name        = '/vehicle/brake_report'
throttle_name     = '/vehicle/throttle_report'
gear_name         = '/vehicle/gear_report'
steer_name        = '/vehicle/steering_report'
wheel_speed_name  = '/vehicle/wheel_speed_report'


# reports

rospy.Subscriber(left_camera_name, 
        CompressedImage, left_camera_sender)

rospy.Subscriber(steer_name, 
        SteeringReport, steer_sender)

rospy.spin()

