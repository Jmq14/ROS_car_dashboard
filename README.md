# ROS_car_dashboard
This is a ROS package to visualize the sensor data, control signals etc. from Berkeley DeepDrive autonomously driving car. 

## Requirements
- [ROS kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)
- [dbw_mkz_ros](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/30b70190e8560d501b761b59c0ca508b57e69133/ROS_SETUP.md?at=default&fileviewer=file-view-default)
- [pyqt4](https://www.saltycrane.com/blog/2008/01/how-to-install-pyqt4-on-ubuntu-linux/)
```shell
apt-cache search pyqt
sudo apt-get install python-qt4
```

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
rosrun monitor run_gui.py
```
or
```shell
# change the path to bag file in launch/run_gui.lauch first
roslaunch monitor run_gui.launch
```

## Components
- [x] Camera viewer
- [x] Control report
- [x] Control chart
- [x] Google map view
- [ ] 3D visualization
