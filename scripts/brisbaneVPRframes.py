import numpy as np
import rosbag 
import time
import torch
import cv2 
import cv_bridge
import PIL.Image as Image
import matplotlib.pyplot as plt

def eventFromRosbagTxt(index_s, index_e):
    with open('ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.txt', 'r') as bag:
        line = bag.readline()
        #w,h = (int(a) for a in line.split(" "))
        line = bag.readline()
        lines_read = 0
        events = []
        while len(line) > 0 and lines_read <= index_e:
            if lines_read >= index_s and lines_read <= index_e:
                t, x, y, p = (float(a) for a in line.split(" "))
                #t = (msg.events[index].ts.secs + msg.events[index].ts.nsecs / float(1e9)) * 1e6
                event = np.vstack((t,x,y,p))
                events.append(event)
            line = bag.readline()
            lines_read += 1
    return events


import os
t_prev = None
for f in os.listdir("ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21/frames"):
    t = float(f.split(".png")[0])
    if t_prev != None:
        img = Image.open(f)
    #events = eventsForImage(t_prev, t)

events=eventFromRosbagTxt(0, 20000)
n_events = len(events)
spike_count = int(n_events // 10)
stride = int(spike_count)

indices_start = np.arange(10) * stride
indices_end = indices_start + spike_count
event_slices= [events[indices_start[i] : indices_end[i]] for i in range(10)]
image=Image.open('ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21/frames/1587540261.544863462448.png')

print(event_slices[1][1])
sensor_size=(346, 260, 2)
frames = np.zeros((len(event_slices), *sensor_size[::-1]), dtype=np.int16)
for i, event_slice in enumerate(event_slices):
    np.add.at(
        frames,
        (i, event_slice[i][3].astype(int), event_slice[i][2].astype(int), event_slice[i][1].astype(int)),
        1,
    )
def plot_frames(frames):
    fig, axes = plt.subplots(1, len(frames))
    for axis, frame in zip(axes, frames):
        axis.imshow(frame[1])
        axis.axis("off")
    plt.tight_layout()
    plt.show()
    
