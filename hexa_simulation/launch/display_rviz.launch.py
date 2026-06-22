from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'hexa_simulation'
    share_dir = Path(get_package_share_directory(package_name))
    urdf_file = share_dir / 'urdf' / 'hexapode.urdf'
    rviz_file = share_dir / 'rviz' / 'hexapode.rviz'

    robot_description = {'robot_description': urdf_file.read_text(encoding='utf-8')}

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
            output='screen',
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            parameters=[robot_description, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', str(rviz_file)],
            output='screen',
        ),
    ])
