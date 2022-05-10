#!/usr/bin/env python

import os

filenames = [
# "dvs_vpr_2020-04-21-17-03-03.bag",
#              "dvs_vpr_2020-04-22-17-24-21.bag",
#              "dvs_vpr_2020-04-24-15-12-03.bag",
             " dvs_vpr_2020-04-22-17-24-21.bag"
            #  "dvs_vpr_2020-04-28-09-14-11.bag",
            #  "dvs_vpr_2020-04-29-06-20-23.bag"
            ]

for filename in filenames:
    os.system("extract_events_from_rosbag.py " + str(filename) + " --output_folder=./ --event_topic=/dvs/events")

# python extract_events_from_rosbag.py dvs_vpr_2020-04-22-17-24-21.bag --output_folder=./ --event_topic=/dvs/events