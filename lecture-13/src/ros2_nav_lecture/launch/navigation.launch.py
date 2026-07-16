import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('ros2_nav_lecture')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
    
    # Launch configurations
    map_yaml_file = LaunchConfiguration('map', default=os.path.join(pkg_share, 'maps', 'tb3_map.yaml'))
    params_file = LaunchConfiguration('params_file', default=os.path.join(pkg_share, 'config', 'nav2_params.yaml'))
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    autostart = LaunchConfiguration('autostart', default='true')
    
    # Declare launch arguments
    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(pkg_share, 'maps', 'tb3_map.yaml'),
        description='Full path to map file to load'
    )
    
    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(pkg_share, 'config', 'nav2_params.yaml'),
        description='Full path to the ROS2 parameters file to use'
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    # Include Nav2 Bringup
    nav2_bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart
        }.items()
    )
    
    # Start RViz
    rviz_config_dir = os.path.join(pkg_nav2_bringup, 'rviz', 'nav2_default_view.rviz')
    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    ld = LaunchDescription()
    
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(nav2_bringup_cmd)
    ld.add_action(start_rviz_cmd)
    
    return ld
