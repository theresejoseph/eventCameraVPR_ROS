#!/usr/bin/env python

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
import numpy as np
from scipy.signal import medfilt2d
import matplotlib.pyplot as plt 
from dvs_msgs.msg import EventArray
import cv2
from cv_bridge import CvBridge, CvBridgeError
from scipy import signal
from scipy.spatial.distance import cdist 
import time
#from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Image
from matplotlib.pyplot import cm


x_list = []
p_list = []
y_list = []
t_list = []
event_frame_qry=[]


# load in references
sensor_size=(346, 260)
events_frame_ref = np.load('/home/tresjsph/Downloads/precomputed.npy')
feats_ref=np.zeros((len(events_frame_ref),sensor_size[0]*sensor_size[1]))
for i in range(0,len(events_frame_ref)):
    feats_ref[i,:]=(events_frame_ref[i].flatten())

'''
# Define a function to show the image in an OpenCV Window
def show_image(img,window_name,num,idx,pos):
	cv2.namedWindow(window_name,num)
	cv2. moveWindow(window_name, pos[0],pos[1])
	#cv2.resizeWindow(window_name, 500,500)
	
	img = np.uint8((np.array(img)/2)*128)
	imC = cv2.applyColorMap(img, cv2.COLORMAP_TWILIGHT_SHIFTED)
	
	imRz=cv2.resize(imC, (int(346*1.5),int(260*1.5)), interpolation = cv2.INTER_AREA)

	font = cv2.FONT_HERSHEY_SIMPLEX  
	org = (20, 20)
	fontScale = 0.75
	color = (0, 0, 0)
	thickness = 2
	
	if idx != None:
		cv2.putText(imRz,"Index: "+idx,org,font,fontScale,color,thickness)
		
	cv2.imshow(window_name, imRz)
	cv2.waitKey(1)
'''	
theta = np.linspace( 0 , 2 * np.pi , len(feats_ref) )
radius = 4
x = radius * np.cos( theta )
y = radius * np.sin( theta )

plt.ion()
fig, ax = plt.subplots()
ax.set_aspect("equal")
#ax.plot(x,y,'.')
ax.axis([-5, 5, -5, 5])
color = iter(cm.rainbow(np.linspace(0, 1, len(events_frame_ref))))

def callback(data):
    global t_list, x_list, y_list, p_list
    for i in range(len(data.events)):
       p_list.append(int(data.events[i].polarity))
       x_list.append(data.events[i].x)
       y_list.append(data.events[i].y)
       t_list.append(data.events[i].ts.to_sec())
      
 
def timer_callback(timer_event):
	global t_list, x_list, y_list, p_list, event_frame_qry
    	#time duration of callback fucntion 
	t_start = time.time()
	t_np = np.array(t_list)
	if len(t_list)>0: 
		last_timestamp=(np.array(t_list)[-1])
		idx= [x for x, val in enumerate(t_np) if ((val > last_timestamp-0.1) & (val < last_timestamp))]

		if len(idx)>0:
			x_np_slice = np.array(x_list)[idx]
			y_np_slice = np.array(y_list)[idx]
			p_np_slice = np.array(p_list)[idx]

			events_frame=np.zeros((sensor_size[1],sensor_size[0]))+2

			for i in range(len(p_np_slice)):
				events_frame[y_np_slice[i], x_np_slice[i]]=p_np_slice[i]
			event_frame_filter=medfilt2d(events_frame, 3)
			event_frame_qry.append(event_frame_filter)
			
			
			seq_len=10
			if len(event_frame_qry)>seq_len:
				event_frame_qry=event_frame_qry[-10:]
				#flattening query image 
				feats_qry=np.zeros((seq_len,sensor_size[0]*sensor_size[1]))
				events_frame_query_seq=event_frame_qry[-seq_len:]
				for i in range(seq_len):    
					feats_qry[i,:]=events_frame_query_seq[i].flatten()
				
				#sequence matching 	
				dMat = cdist(feats_ref,feats_qry,'euclidean')
				convdMat=np.array(signal.convolve2d(dMat,np.identity(seq_len,dtype=int), mode='valid'))
				mIndSeqs = np.argmin(convdMat,axis=0)
				

				#show_image(events_frame_ref[mIndSeqs[-1]],"match Window",2,str(mIndSeqs[-1]), [600,30])
				#Publish Matched Images 
				img = np.uint8((np.array(events_frame_ref[mIndSeqs[-1]])/2)*128)
				imC = cv2.applyColorMap(img, cv2.COLORMAP_TWILIGHT_SHIFTED)
				msg_frame = CvBridge().cv2_to_imgmsg(imC,"bgr8")
				pubMatch.publish(msg_frame)
				
				x_match=x[mIndSeqs[-1]]
				y_match=y[mIndSeqs[-1]]
				dx=np.cos(theta[mIndSeqs[-1]])
				dy=np.sin(theta[mIndSeqs[-1]])
				
				
				cmap=cm.rainbow
				a = ax.quiver(x_match,y_match,dx,dy,color=cmap(float(mIndSeqs[-1]/len(events_frame_ref))))
				fig.canvas.draw_idle()
				plt.pause(0.004)


			#show_image(np.array(event_frame_filter),"query Window",1,str(len(event_frame_qry)),[20,30])
			#Publish Query Images 
			img_q = np.uint8((np.array(event_frame_filter)/2)*128)
			imC_q = cv2.applyColorMap(img_q, cv2.COLORMAP_TWILIGHT_SHIFTED)
			msg_frame_query = CvBridge().cv2_to_imgmsg(imC_q,"bgr8")
			pubQuery.publish(msg_frame_query)
				
			
			#Storing only last frame within the list 
			p_list = p_list[np.min(idx):]
			x_list = x_list[np.min(idx):]
			y_list = y_list[np.min(idx):]
			t_list = t_list[np.min(idx):]
			print(len(event_frame_qry))
	end_time = time.time()
	print('Time: %.2f' % (end_time-t_start))
	

if __name__ == '__main__':

    rospy.init_node('listener', anonymous=True)
    
    rospy.Subscriber('/dvs/events', EventArray, callback)
    
    rospy.Timer(rospy.Duration(1), timer_callback)
    
    pubQuery = rospy.Publisher('query', Image, queue_size=10)
    
    pubMatch = rospy.Publisher('match', Image, queue_size=10) 
    
    plt.show(block=True)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    

    

