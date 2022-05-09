#!/usr/bin/env python3

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
import numpy as np
import matplotlib.pyplot as plt 
from dvs_msgs.msg import EventArray
#import scipy

x_list = []
p_list = []
y_list = []
t_list = []

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    
    print(len(data.events))
    '''
    data.events[:].ts -= data.events[:].ts
    data.events[:].ts *= 1e6
    events = np.column_stack((data.events.ts, data.events.x, data.events.y, data.events.polarity))'''
    
    
    for i in range(len(data.events)):
       p_list.append(int(np.array(data.events[i].polarity)))
       x_list.append(np.array(data.events[i].x))
       y_list.append(np.array(data.events[i].y))
       t_list.append(np.array(data.events[i].ts-data.events[0].ts))
    
    '''
    x_np = np.array(x_list)
    t_np = np.array(t_list)
    y_np = np.array(y_list)
    p_np = np.array(p_list)
    #print(f"{x_list}\n{y_list}\n{p_list}\n{t_list}\n")
    
    if len(x_np)>2000: 
    
      #t_np_slice = p_np[(t_np > last_timestamp-0.001)-1]
      x_np_slice = x_np[-2000:]
      y_np_slice = y_np[-2000:]
      p_np_slice = p_np[-2000:]
      
      print(len(x_np_slice))
      sensor_size=(346, 260)
      events_frame=np.zeros((sensor_size[1],sensor_size[0]))+2
   
      for i in range(len(p_np_slice)):
         events_frame[y_np_slice[i], x_np_slice[i]]=p_np_slice[i]

      rospy.loginfo((events_frame))   
      rospy.loginfo(np.sum(events_frame))
      plt.imshow(events_frame)'''
      

    
def timer_callback(timer_event):
   

   #rospy.loginfo((np.array(t_list)))
   x_np = np.array(x_list)
   t_np = np.array(t_list)
   y_np = np.array(y_list)
   p_np = np.array(p_list)
    
   #last_timestamp = t_list[-1]
   print([(x_np[i], y_np[i], p_np[i], t_np[i]) for i in range(999)])
      #print(f"{x_list[-1000:]}\n{y_list[-1000:]}\n{p_list[-1000:]}\n{t_list[-1000:]}\n")
      #t_np_slice = p_np[(t_np > last_timestamp-0.001)-1]
   x_np_slice = x_np[-20000:]
   y_np_slice = y_np[-20000:]
   p_np_slice = p_np[-20000:]

   print(len(x_np_slice))
   sensor_size=(346, 260)
   events_frame=np.zeros((sensor_size[1],sensor_size[0]))+2

   for i in range(len(p_np_slice)):
      events_frame[y_np_slice[i], x_np_slice[i]]=p_np_slice[i]

   rospy.loginfo((events_frame))   
   rospy.loginfo(np.sum(events_frame))
   plt.imshow(events_frame)
   plt.show()
    
''' 
event_frame_query = ....

matches = scipy.dists.cdist(event_frame_query, event_frame_refs)

matches_sequence = # seq matcher

best_match = np.argmin(matches)

event_frame_ref_match = event_frame_refs[best_match]

cv2.text(event_frame_ref_match, 'match idx: %d' % best_match)

best_match_publisher.publish(event_frame_ref_match) '''
       

if __name__ == '__main__':
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    # load in references
    #event_frame_refs = np.load('precomputed.npy')
  
    rospy.init_node('listener', anonymous=True)
    
    rospy.Subscriber('/dvs/events', EventArray, callback)
    
    rospy.Timer(rospy.Duration(0.001), timer_callback)
    
	
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
'''

from std_msgs.msg import Int64
from std_srvs.srv import SetBool
class NumberCounter:
    def __init__(self):
        self.counter = 0
        self.pub = rospy.Publisher("/number_count", Int64, queue_size=10)
        self.number_subscriber = rospy.Subscriber("/number", Int64, self.callback_number)
        self.reset_service = rospy.Service("/reset_counter", SetBool, self.callback_reset_counter)
    def callback_number(self, msg):
        self.counter += msg.data
        new_msg = Int64()
        new_msg.data = self.counter
        self.pub.publish(new_msg)
    def callback_reset_counter(self, req):
        if req.data:
            self.counter = 0
            return True, "Counter has been successfully reset"
        return False, "Counter has not been reset"
if __name__ == '__main__':
    rospy.init_node('number_counter')
    NumberCounter()
    rospy.spin()
 '''   
