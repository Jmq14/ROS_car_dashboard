# ROS_car_dashboard
This is a ROS package to visualize the sensor data, control signals etc. from Berkeley DeepDrive autonomously driving car. 

## Installation
```shell
# download
cd dbw_ws/src
git clone git@github.com:Jmq14/ROS_car_dashboard.git

# rename package to 'monitor' or it won't build and run correctly
mv ROS_car_dashboard monitor

# build
cd ../
catkin_make
source devel/setup.bash
```

## Usage
To launch the dashboard, you can either use `rosrun` or `roslaunch`:
```shell
# create ros master node and play a bag file
roscore
rosbag play [bag file]

# open dashboard
rosrun ROS_car_dashboard run_gui.py
```
or
```shell
roslaunch ROS_car_dashboard run_gui.launch
```

## Components
- [x] Camera viewer
- [x] Control report
- [x] Control chart
- [x] Google map view
- [ ] 3D visualization
