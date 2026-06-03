import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = get_package_share_directory("omniwheel_mujoco_sim")
    urdf_file = os.path.join(package_dir, "urdf", "omniwheel_sim.urdf")

    with open(urdf_file, "r", encoding="utf-8") as file:
        robot_description = file.read()

    config_file = LaunchConfiguration("config_file")
    scene_file = LaunchConfiguration("scene_file")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "config_file",
                default_value="/workspace/omniwheel_mujoco/simulate/config.yaml",
            ),
            DeclareLaunchArgument(
                "scene_file",
                default_value="/workspace/omniwheel_mujoco/mujoco/scene.xml",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "robot_description": robot_description,
                        "use_sim_time": True,
                    }
                ],
            ),
            Node(
                package="omniwheel_mujoco_sim",
                executable="omniwheel_mujoco_sim",
                name="omniwheel_mujoco_sim",
                output="screen",
                arguments=["--config", config_file, "--scene", scene_file],
                parameters=[{"use_sim_time": True}],
            ),
        ]
    )
