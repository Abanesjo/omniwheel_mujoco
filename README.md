# omniwheel_mujoco

Docker-based MuJoCo simulator for the omniwheel robot. The container uses ROS 2 Humble and CycloneDDS; the host ROS install is not used.

## Run

```bash
./build_and_run.sh
```

The script builds the image and starts the MuJoCo viewer with ROS 2 publishers/subscribers active.
It uses host networking and CycloneDDS on multicast-enabled loopback, matching the
`omniwheel_ros` Docker setup.

## Control Input

Publish direct wheel torques:

```bash
ros2 topic pub /omni/wheel_torques std_msgs/msg/Float64MultiArray "{data: [0.5, -0.5, 0.0]}"
```

Order is `[left, right, back]` in Nm. Commands are saturated to `+/-7.1 Nm` and decay to zero after a `0.2s` timeout.

## Published Interfaces

- `/odometry/filtered` (`nav_msgs/msg/Odometry`), localization-equivalent MuJoCo truth in `odom -> base_footprint`
- `/tf`, including dynamic `odom -> base_footprint`
- `/omni/wheel_odometry` (`geometry_msgs/msg/TwistWithCovarianceStamped`)
- `/joint_states` (`sensor_msgs/msg/JointState`)
- `/omni/encoder_angles` (`std_msgs/msg/Float32MultiArray`)
- `/clock` (`rosgraph_msgs/msg/Clock`)

The sim does not publish camera or LiDAR topics and does not run `robot_localization`.
