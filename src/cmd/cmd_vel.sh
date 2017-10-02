rostopic pub -r 10 /vehicle/dbw_enabled std_msgs/Bool 'True'
rostopic pub -r 10 /vehicle/cmd_vel geometry_msgs/Twist  '{linear:  {x: 10, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 5.0}}'
