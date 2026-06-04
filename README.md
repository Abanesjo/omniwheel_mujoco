# omniwheel_mujoco

Docker-based MuJoCo simulator for the omniwheel robot. The container uses ROS 2 Humble and CycloneDDS;

## Run

```bash
./build_and_run.sh
```

The script builds the image and starts the MuJoCo viewer with ROS 2 publishers/subscribers active.
It uses host networking and CycloneDDS on multicast-enabled loopback, matching the
`omniwheel_ros` Docker setup.

## Control Input

Publish a base-frame wrench, matching the real `omni/` motor torque controller:

```bash
ros2 topic pub -r 100 /omni/cmd_wrench geometry_msgs/msg/Wrench \
"{force: {x: 1.0, y: 0.0, z: 0.0}, torque: {x: 0.0, y: 0.0, z: 0.0}}"
```

The simulator uses `force.x`, `force.y`, and `torque.z`, converts them to wheel torques
with the same Jacobian constants as `omni_motor_bulkctrl_torque.cpp`, saturates each
wheel to `+/-4.7 Nm`, and decays to zero after a `0.2s` timeout.

## Published Interfaces

- `/odometry/filtered` (`nav_msgs/msg/Odometry`), localization-equivalent MuJoCo truth in `odom -> base_footprint`
- `/tf`, including dynamic `odom -> base_footprint`
- `/omni/wheel_odometry` (`geometry_msgs/msg/TwistWithCovarianceStamped`)
- `/joint_states` (`sensor_msgs/msg/JointState`)
- `/omni/encoder_angles` (`std_msgs/msg/Float32MultiArray`)
- `/clock` (`rosgraph_msgs/msg/Clock`)

The sim does not publish camera or LiDAR topics and does not run `robot_localization`.
