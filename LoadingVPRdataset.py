import tonic
import tonic.transforms as transforms
import numpy as np
import rosbag 
from tonic.datasets.davisdataset import Dataset
import time
import torch
import cv2 
import cv_bridge
from tonic.functional.slicing import (
    slice_by_time,
    slice_by_event_count,
    slice_by_time_bins,
    slice_by_event_bins,
)

sensor_size = tonic.datasets.VPR.sensor_size
print('Loading data')


class MyRecordings(Dataset):
    sensor_size = (346, 260, 2) # the sensor size of the event camera or the number of channels of the silicon cochlear that was used
    ordering = "txyp" # the order in which your event channels are provided in your recordings

    def __init__(
        self,
        transform=None,
    ):
        super(MyRecordings, self).__init__(
            transform=transform
        )

        # replace the strings with your training/testing file locations or pass as an argument
        self.filename = "./ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag"

    def __getitem__(self, index):
        with rosbag.Bag('./ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag', 'r') as bag:
            for topic, msg, t in bag.read_messages():
                if topic == '/dvs/events':

                    ''' names = ['t', 'x', 'y', 'p']
                        formats = ['f16', 'f16', 'f16','f16']
                        type2 = np.dtype({'names': names, 'formats': formats})
                    '''
                    t = (msg.events[index].ts.secs + msg.events[index].ts.nsecs / float(1e9)) * 1e6
                    events = np.vstack((float(t), float(msg.events[index].x), float(msg.events[index].y), float(1 if msg.events[index].polarity else -1))).T
                    if self.transform is not None:
                        events = self.transform(events, self.sensor_size, self.ordering)

                    '''if topic == '/dvs/image_raw':
                    image = cv_bridge.imgmsg_to_cv2(msg, "bgr8")'''
                    return events
    def __len__(self):
        with rosbag.Bag('./ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag', 'r') as bag:
            for topic, msg, t in bag.read_messages():
                if topic == '/dvs/events':
                    return len(msg.events)
        return 0

def to_frame_numpy(
    events,
    sensor_size,
    time_window=None,
    event_count=None,
    n_time_bins=None,
    n_event_bins=None,
    overlap=0.0,
    include_incomplete=False,
):
    """Accumulate events to frames by slicing along constant time (time_window),
    constant number of events (event_count) or constant number of frames (n_time_bins / n_event_bins).

    Parameters:
        events: ndarray of shape [num_events, num_event_channels]
        sensor_size: size of the sensor that was used [W,H,P]
        time_window (None): window length in us.
        event_count (None): number of events per frame.
        n_time_bins (None): fixed number of frames, sliced along time axis.
        n_event_bins (None): fixed number of frames, sliced along number of events in the recording.
        overlap (0.): overlap between frames defined either in time in us, number of events or number of bins.
        include_incomplete (False): if True, includes overhang slice when time_window or event_count is specified. Not valid for bin_count methods.

    Returns:
        numpy array with dimensions (TxPxHxW)
    """


    if not sensor_size:
        sensor_size_x = int(events[1].max() + 1)
        sensor_size_y = int(events[2].max() + 1)
        sensor_size_p = len(np.unique(events[3]))
        sensor_size = (sensor_size_x, sensor_size_y, sensor_size_p)

    if time_window:
        event_slices = slice_by_time(
            events, time_window, overlap=overlap, include_incomplete=include_incomplete
        )
    elif event_count:
        event_slices = slice_by_event_count(
            events, event_count, overlap=overlap, include_incomplete=include_incomplete
        )
    elif n_time_bins:
        event_slices = slice_by_time_bins(events, n_time_bins, overlap=overlap)
    elif n_event_bins:
        event_slices = slice_by_event_bins(events, n_event_bins, overlap=overlap)

    frames = np.zeros((len(event_slices), *sensor_size[::-1]), dtype=np.int16)
    for i, event_slice in enumerate(event_slices):
        np.add.at(
            frames,
            (i, event_slice[3].astype(int), event_slice[1], event_slice[2] ),
            1,
        )
    return frames

dataset = MyRecordings()
dataloader = torch.utils.data.DataLoader(dataset, shuffle=True)
def load_sample_pytorch():
    events = []
    for i, event in enumerate(iter(dataloader)):
        events.append(event)
        if i > 99: break
    return np.array(events)

print('Before frame transforms')

frames = to_frame_numpy(load_sample_pytorch(),sensor_size=sensor_size, n_time_bins=3)

import matplotlib.pyplot as plt

def plot_frames(frames):
    fig, axes = plt.subplots(1, len(frames))
    for axis, frame in zip(axes, frames):
        axis.imshow(frame[1]-frame[0])
        axis.axis("off")
    plt.tight_layout()
        
plot_frames(frames)