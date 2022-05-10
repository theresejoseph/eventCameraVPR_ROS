import tonic
import tonic.transforms as transforms
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import scipy.signal
from numpy import sin,cos,pi
from scipy.spatial.distance import cdist 
# import torch 
from scipy.integrate import cumtrapz
import pandas as pd 

# Loading datasets 

dataset = tonic.datasets.VPR(save_to='./VPR_dataset')

query, query_targets = dataset[0]
query_events, query_imu, query_images = query  #680 images

reference, ref_targets = dataset[1]
ref_events, ref_imu, ref_images = reference #1487 images 

ref_and_query=[ref_events, query_events]
len_smaller_data=len(ref_and_query[np.argmin([len(ref_events),len(query_events)])])

indoor_events_query=np.asarray(pd.read_feather('/Users/theresejoseph/Documents/VRES/VPR_dataset/bags_2021-08-19-08-25-42_denoised.feather'))
indoor_events_ref=np.asarray(pd.read_feather('/Users/theresejoseph/Documents/VRES/VPR_dataset/bags_2021-08-19-08-28-43_denoised.feather'))


##########################################################################################
# Handling IMU data 
def imu_processing():
    accelX,accelY,accelZ=ref_imu['acc'][:,0],ref_imu['acc'][:,1],ref_imu['acc'][:,2]
    magReadX,magReadY,magReadZ=ref_imu['mag'][:,0],ref_imu['mag'][:,1],ref_imu['mag'][:,2]
    angVX,angVY,angVZ=ref_imu['angV'][:,0],ref_imu['angV'][:,1],ref_imu['angV'][:,2]

    roll, pitch, yaw = np.empty(accelX.shape),np.empty(accelX.shape),np.empty(accelX.shape)
    for i in range(len(accelX)):
        pitch[i] = 180 * math.atan2(accelX[i], math.sqrt(accelY[i]*accelY[i] + accelZ[i]*accelZ[i]))/pi
        roll[i] = 180 * math.atan2(accelY[i], math.sqrt(accelX[i]*accelX[i] + accelZ[i]*accelZ[i]))/pi

        mag_x = magReadX[i]*cos(pitch[i]) + magReadY[i]*sin(roll[i])*sin(pitch[i]) + magReadZ[i]*cos(roll[i])*sin(pitch[i])
        mag_y = magReadY[i] * cos(roll[i]) - magReadZ[i] * sin(roll[i])
        yaw [i]= 180 * math.atan2(-mag_y,mag_x)/pi

    dt=ref_imu['ts'][1]-ref_imu['ts'][0]
    x =cumtrapz(cumtrapz(accelX,dx=dt),dx=dt)
    y =cumtrapz(cumtrapz(accelY,dx=dt),dx=dt)
    z =cumtrapz(cumtrapz(accelZ,dx=dt),dx=dt)

    angX=cumtrapz(angVX,dx=dt)
    angY=cumtrapz(angVY,dx=dt)
    angZ=cumtrapz(angVZ,dx=dt)
    #print(ref_imu)
    return x,y,z,angX,angY,angZ

'''fig1,ax = plt.subplots()
fig1.suptitle('3D Trajectory of Events',fontsize=10)
ax = plt.axes(projection='3d')
ax.plot3D(x,y,z,c='red',lw=5)
ax.set_xlabel('X position (m)')
ax.set_ylabel('Y position (m)')


fig2, ax = plt.subplots()
fig1.suptitle('3D Trajectory of Events',fontsize=10)
ax1 = plt.axes(projection='3d')
ax1.plot3D(angX,angY,angZ,c='blue',lw=5)
ax1.set_xlabel('X angle (rad)')
ax1.set_ylabel('Y angle (rad)')'''


##########################################################################################
#Creating event frames 
sensor_size = tonic.datasets.VPR.sensor_size
'''ref_mean_diff = np.diff(list(zip(ref_images["ts"], ref_images["ts"][1:]))).mean()
print("Mean reference difference is " + str(ref_mean_diff))
query_mean_diff = np.diff(list(zip(query_images["ts"], query_images["ts"][1:]))).mean()
print("Mean query difference is " + str(query_mean_diff))'''
def gpsForEvents(events,targets):
    eventsPerGPS=len(events)//len(targets)
    lat_longR=np.add([elem[0] for elem in targets],[elem[1] for elem in targets])

    gps=[0]*((len(events)))
    for i in range(0,len(events),eventsPerGPS):
        if (i+eventsPerGPS)>len(events)-1:
                break 
        gps[i:i+eventsPerGPS]=lat_longR[i//eventsPerGPS]*np.ones((eventsPerGPS))
    return gps

def event_slice(start, end, events):
    events_frame=np.zeros((sensor_size[1],sensor_size[0]))+2
    for i in range(start, end):
        events_frame[events[i][2], events[i][1]]=events[i][3]
    event_frame_filter=scipy.signal.medfilt2d(events_frame, 3)
    return event_frame_filter

def eventSlicedForImages(events, image_len):
    events_per_Frame=int(len(events)/image_len)
    events_frame_all=[0]*680
    for num in range(0, len(events),events_per_Frame):
        if (num//events_per_Frame)>679:
            break 
        events_frame_all[(num//events_per_Frame)]=event_slice(num, num+events_per_Frame, events)
    return events_frame_all

#print('There are %d images and %d events producing %d events per image' % (len(images["frames"]), len(events), int((len(events)/len(images["frames"])))))
def eventSliceTime(events,sliceTime):
    #lat_long=gpsForEvents(events,target)
    n_slices = int(np.floor(((events[-1][0] - events[0][0]) - sliceTime) / sliceTime) + 1)
    eventsPerFrame=len(events)//n_slices

    events_frame_all=[0]*n_slices
    #frame_gps=[0]*n_slices

    for num in range(0, len(events),eventsPerFrame):
        times=events[num][1]
        if (num//eventsPerFrame)>n_slices-1:
            break 
        events_frame_all[(num//eventsPerFrame)]=event_slice(num, num+eventsPerFrame, events)
        #frame_gps[(num//eventsPerFrame)]=lat_long[num]

    return events_frame_all


##########################################################################################
'''events_frame_ref=eventSlicedForImages(ref_events, len(ref_images["frames"]))
events_frame_query=eventSlicedForImages(query_events, len(query_images["frames"]))'''
sliceTime=200000
events_frame_ref=eventSliceTime(indoor_events_ref, sliceTime)
events_frame_query=eventSliceTime(indoor_events_query, sliceTime)

print("Currently used slice time for frames is "+ str(sliceTime) +" microseconds")

feats_ref=np.zeros((len(events_frame_ref),sensor_size[0]*sensor_size[1]))
feats_qry=np.zeros((len(events_frame_ref),sensor_size[0]*sensor_size[1]))
for i in range(0,len(events_frame_ref)):
    feats_ref[i,:]=(events_frame_ref[i].flatten())
    feats_qry[i,:]=(events_frame_query[i].flatten())

print("Done flattening and joining frames")
dMat = cdist(feats_ref,feats_qry,'euclidean')
# mInds = np.argsort(dMat,axis=0)[0] # shape: K x ft_qry.shape[0]

# plt.imshow(dMat)
# plt.xlabel("Reference Frames")
# plt.ylabel("Query Frames")
# plt.show()

# def seq_matching(feats_ref,qry_seq,seq_len):
#     diagOnes=np.identity(seq_len,dtype=int)
#     modSeq=seq_len*(len(feats_ref)//seq_len)
#     dMat_new = cdist(qry_seq,feats_ref,'euclidean')

#     #diag_dMat=np.zeros((seq_len,modSeq-seq_len))
#     sum_diag=np.zeros(modSeq-seq_len+1)
#     for i in range(0,modSeq):
#         #diag_dMat[:,i:i+seq_len]=(dMat_new[:,i:i+seq_len]*diagOnes)
#         sum_diag[i]=np.sum(dMat_new[:,i:i+seq_len]*diagOnes)
#         if i+seq_len==modSeq:
#             break
#     minIdx=np.argmin(sum_diag)
#     return minIdx

# def matching_dataset(feats_ref,feats_qry,seq_len):
#     indexes=np.zeros(seq_len*(len(feats_qry)//seq_len))
#     for i in range(0,seq_len*(len(feats_qry)//seq_len),seq_len):
#         idx=seq_matching(feats_ref,np.array(feats_qry)[i:i+seq_len,:],seq_len)
#         indexes[i:i+seq_len]=np.array(range(idx,idx+seq_len), dtype=int)
#     return indexes
seq_len=3
print("Currently used sequence length for frames is "+ str(seq_len))
from scipy import signal
convdMat=np.array(signal.convolve2d(dMat, np.identity(seq_len,dtype=int), mode='valid'))
mIndSeqs = np.argmin(convdMat,axis=0)
print("Done compiling indexes")

blank=np.zeros((sensor_size[1],sensor_size[0]))
fig4, (ax1, ax2, ax3, ax4)= plt.subplots(4,1)
fig4.set_tight_layout(True)
ax1.imshow(blank, animated=True)
ax2.imshow(blank, animated=True)
ax3.imshow(blank, animated=True)


def processSeqTraverses(i):
    qry=events_frame_query[i]
    gndt=events_frame_ref[i]
    match=events_frame_ref[mIndSeqs[i]]
    ax1.set_title("Query Event: "+ str(i))
    ax2.set_title( " Match: " +str(mIndSeqs[i]))
    ax3.set_title("Ground Truth")

    ax1.imshow(qry, animated=True)
    ax2.imshow(match, animated=True)
    ax3.imshow(gndt, animated=True)

    theta = np.linspace( 0 , 2 * np.pi , len(feats_ref) )
    radius = 0.4
    a = radius * np.cos( theta )
    b = radius * np.sin( theta )
    ax4.set_xlim([-0.5, 0.5])
    ax4.set_ylim([-0.5, 0.5])
    ax4.plot(a[:i], b[:i])

anim = animation.FuncAnimation(fig4, processSeqTraverses, frames=len(events_frame_query), interval = 20)

plt.show()

# Matching query and refenernce with visualisation 
def matchEvents(qry_Idx, events_frame_ref,events_frame_query):
    #Sum of differences for each individual frame
    '''sumDiff=np.zeros(len(events_frame_ref))
    dMat=np.zeros(len(events_frame_ref))
    for j in range(0,len(events_frame_ref)):
        sumDiff[j]=np.sum(np.abs(events_frame_ref[j]-events_frame_query[qry_Idx]))
    minIdx=np.argmin(sumDiff)

    qry=events_frame_query[qry_Idx]
    gndt=events_frame_ref[qry_Idx]
    match=events_frame_ref[minIdx]
    idx_diff = abs(qry_Idx - minIdx)'''

    #Indexes for ground truth and match 
    #gndtIdx = (np.abs(gps_ref - gps_query[qry_Idx])).argmin()

    #Final query reference, match and index difference
    qry=events_frame_query[qry_Idx]
    gndt=events_frame_ref[qry_Idx]
    match=events_frame_ref[mInds[qry_Idx]]

    # SeqSLAM
    '''dist_matrix_seqslam=apply_seqSLAM(5, dMat)
    mInds_seqSlam = np.argsort(dist_matrix_seqslam,axis=0)[0] # shape: K x ft_qry.shape[0]
    '''
    return qry, gndt, match

# blank=np.zeros((sensor_size[1],sensor_size[0]))
# fig3, (ax1, ax2, ax3)= plt.subplots(1,3)
# fig3.set_tight_layout(True)
# ax1.imshow(blank, animated=True)
# ax2.imshow(blank, animated=True)
# ax3.imshow(blank, animated=True)

# def processTraverses(i):
#     qry, gndt, match= matchEvents(i, events_frame_ref,events_frame_query)
#     ax1.set_title("Query Event: "+ str(i))
#     if abs(i - mInds[i]) <= 20:
#         ax2.set_title( "Correct Match: " +str(mInds[i]))
#     else:
#         ax2.set_title( "Incorrect Match: " + str(mInds[i]))

#     ax3.set_title("Ground Truth")

#     ax1.imshow(qry, animated=True)
#     ax2.imshow(match, animated=True)
#     ax3.imshow(gndt, animated=True)

# anim = animation.FuncAnimation(fig3, processTraverses, frames=len_smaller_data)
# plt.show()


'''fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(events_frame_all[100], animated=True)
ax1.set_title("event frame")
ax2.imshow(images["frames"][100], cmap=mpl.cm.gray, animated=True)
ax2.set_title("grey level image")
plt.show()'''

'''fig, (ax1, ax2)= plt.subplots(1,2)
fig.set_tight_layout(True)
ax1.imshow(events_frame_ref[0], animated=True)
ax2.imshow(events_frame_query[0], animated=True)

def update(i):
    ax1.set_title("Reference event frame")
    ax2.set_title("Query event frames")
    ax1.imshow(events_frame_ref[i], animated=True)
    ax2.imshow(events_frame_query[i], animated=True)
anim = animation.FuncAnimation(fig, update, frames=1487, interval = 20)
plt.show()'''


#####################################################################

'''
rosbag info ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag

rosbag play ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag

path:        ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag
version:     2.0
duration:    10:51s (651s)
start:       Apr 22 2020 17:24:21.55 (1587540261.55)
end:         Apr 22 2020 17:35:12.83 (1587540912.83)

rosbag filter ROSbags_BrisbaneVPRdata/dvs_vpr_2020-04-22-17-24-21.bag output.bag "t.secs >= 1587975210.04 and t.secs <= 1587975300"

dvs_vpr_2020-04-27-18-13-29.bag
'''

'''
path:        VPR_dataset/VPR/dvs_vpr_2020-04-21-17-03-03-filtered.bag
version:     2.0
duration:    17.0s
start:       Apr 21 2020 17:03:04.00 (1587452584.00)
end:         Apr 21 2020 17:03:20.99 (1587452600.99)
'''



