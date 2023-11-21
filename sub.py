#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading

class CameraSubscriber:
    def __init__(self):
        rospy.init_node('camera_subscriber', anonymous=True)

        self.bridge = CvBridge()
        rospy.Subscriber('/camera1/image_raw', Image, self.camera1_callback)
        rospy.Subscriber('/camera2/image_raw', Image, self.camera2_callback)

        cv2.namedWindow('Camera 1', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Camera 2', cv2.WINDOW_NORMAL)
        
        self.lock = threading.Lock()

    def camera1_callback(self, msg):
        with self.lock:
            self.camera1_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    
    def camera2_callback(self, msg):
        with self.lock:
            self.camera2_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

    def display_images(self):
        while not rospy.is_shutdown():
            with self.lock:
                if hasattr(self, 'camera1_image'):
                    cv2.imshow('Camera 1', self.camera1_image)
            
                if hasattr(self, 'camera2_image'):
                    cv2.imshow('Camera 2', self.camera2_image)
            cv2.waitKey(1)

    def run(self):
        display_thread = threading.Thread(target=self.display_images)
        display_thread.start()
        rospy.spin()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        subscriber = CameraSubscriber()
        subscriber.run()
    except rospy.ROSInterruptException:
        pass
