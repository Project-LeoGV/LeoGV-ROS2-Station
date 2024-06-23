# Copyright (c) 2021 Juan Miguel Jimeno
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():
    video_path = '/home/nadamamdouh/Videos/Screencasts/RP_Robot.webm' #'/dev/video0'

#    sensors_launch_path = PathJoinSubstitution(
#        [FindPackageShare('leogv_bringup'), 'launch', 'sensors.launch.py']
#    )

#    joy_launch_path = PathJoinSubstitution(
#        [FindPackageShare('leogv_bringup'), 'launch', 'joy_teleop.launch.py']
#    )

    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('leogv_description'), 'launch', 'description.launch.py']
    )

    ekf_config_path = PathJoinSubstitution(
        [FindPackageShare("leogv_base"), "config", "ekf.yaml"]
    )

#    default_robot_launch_path = PathJoinSubstitution(
#        [FindPackageShare('leogv_bringup'), 'launch', 'default_robot.launch.py']
#    )

#    custom_robot_launch_path = PathJoinSubstitution(
#        [FindPackageShare('leogv_bringup'), 'launch', 'custom_robot.launch.py']
#    )

    extra_launch_path = PathJoinSubstitution(
        [FindPackageShare('leogv_bringup'), 'launch', 'extra.launch.py']
    )
    lidar_launch_path = PathJoinSubstitution(
        [FindPackageShare('rplidar_ros'),'launch', 'rplidar_a1_launch.py']
    )

    return LaunchDescription([
    #    DeclareLaunchArgument(
    #        name='custom_robot', 
    #        default_value='false',
    #        description='Use custom robot'
    #    ),

        DeclareLaunchArgument(
            name='extra', 
            default_value='false',
            description='Launch extra launch file'
        ),

        DeclareLaunchArgument(
            name='description', 
            default_value='true',
            description='Launch description launch file'
        ),

        DeclareLaunchArgument(
            name='frame_id', 
            default_value='laser',
            description='rplidar frame id'
        ),

    #    DeclareLaunchArgument(
    #        name='base_serial_port', 
    #        default_value='/dev/ttyACM0',
    #        description='Linorobot Base Serial Port'
    #    ),

    #   DeclareLaunchArgument(
    #        name='micro_ros_transport',
    #        default_value='serial',
    #        description='micro-ROS transport'
    #    ),

    #    DeclareLaunchArgument(
    #        name='micro_ros_port',
    #        default_value='8888',
    #        description='micro-ROS udp/tcp port number'
    #    ),

        DeclareLaunchArgument(
            name='odom_topic', 
            default_value='/odom',
            description='EKF out odometry topic'
        ),
        
    #    DeclareLaunchArgument(
    #        name='joy', 
    #        default_value='false',
    #        description='Use Joystick'
    #    ),

        DeclareLaunchArgument(
            name='lidar', 
            default_value='false',
            description='Launch lidar'
        ),

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                ekf_config_path
            ],
            remappings=[("odometry/filtered", LaunchConfiguration("odom_topic"))]
        ),

        Node(
            package='odrive_driver',
            executable='odrive_node',
            output='screen'
        ),

        Node(
            package='two_wheel_demo',
            executable='run_demo',
            output='screen'
        ),

    #    Node(
    #        package='camera_simulator',
    #        executable='camera_simulator',
    #        output='screen',
    #        arguments=[
    #            '--type', 'video',
    #            '--path', video_path,
    #            '--loop'
    #        ],
    #    ),

    #    IncludeLaunchDescription(
    #        PythonLaunchDescriptionSource(default_robot_launch_path),
    #        condition=UnlessCondition(LaunchConfiguration("custom_robot")),
    #        launch_arguments={
    #            'base_serial_port': LaunchConfiguration("base_serial_port")
    #        }.items()
    #    ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(extra_launch_path),
            condition=IfCondition(LaunchConfiguration("extra")),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch_path),
            condition=IfCondition(LaunchConfiguration("description")),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(lidar_launch_path),
            condition=IfCondition(LaunchConfiguration("lidar")),
            launch_arguments={
                'frame_id': LaunchConfiguration("frame_id")
            }.items()
        )
        
    ])
