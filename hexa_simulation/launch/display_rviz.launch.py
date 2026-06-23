from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'hexa_simulation'
    share_dir = Path(get_package_share_directory(package_name))
    urdf_file = share_dir / 'urdf' / 'hexapode.urdf'
    rviz_file = share_dir / 'rviz' / 'hexapode.rviz'

    robot_description = {'robot_description': urdf_file.read_text(encoding='utf-8')}

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
            output='screen',
        ),

        Node(
            package='hexa_simulation',
            executable='sim_hexa',
            output='screen',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', str(rviz_file)],
            output='screen',
        ),
    ])
