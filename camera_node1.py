#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def camera_node_1():
    rospy.init_node('camera_node_1', anonymous=True)
    rate = rospy.Rate(10)  

    cap = cv2.VideoCapture(0)

    image_pub = rospy.Publisher('/camera1/image_raw', Image, queue_size=10)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            image_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            image_pub.publish(image_msg)
        rate.sleep()
    cap.release()

if __name__ == '__main__':
    try:
        camera_node_1()
    except rospy.ROSInterruptException:
        pass
