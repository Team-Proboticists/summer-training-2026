import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Get directories
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_tb3_desc = get_package_share_directory('turtlebot3_description')
    
    # Model configuration
    tb3_model = os.getenv('TURTLEBOT3_MODEL', 'waffle')
    urdf_file_name = f'turtlebot3_{tb3_model}.urdf'
    print(urdf_file_name)
    urdf_path = os.path.join(pkg_tb3_desc, 'urdf', urdf_file_name)
    
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')
    z_pose = LaunchConfiguration('z_pose', default='0.01')
    
    # Declare launch arguments
    declare_x_pose_cmd = DeclareLaunchArgument('x_pose', default_value='-2.0')
    declare_y_pose_cmd = DeclareLaunchArgument('y_pose', default_value='-0.5')
    
    # Gazebo World
    world_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'turtlebot3_world.world'
    )
    
    # Start Gazebo Server
    start_gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={
            'world': world_path,
            'verbose': 'true'
        }.items()
    )

    
    # Start Gazebo Client
    start_gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )
    
    # Robot State Publisher node
    # Reads the URDF file and publishes robot joint states / tf
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()
        
    # Remove ${namespace} template variable to match standard TF frame names
    robot_desc = robot_desc.replace('${namespace}', '')

    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_desc
        }]
    )
    
    # SDF Model path containing Gazebo plugins
    model_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        'turtlebot3_' + tb3_model,
        'model.sdf'
    )

    # Spawn Robot Node
    spawn_robot_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', tb3_model,
            '-file', model_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose,
            '-timeout', '300'
        ],
        output='screen'
    )


    
    ld = LaunchDescription()
    
    # Add actions
    ld.add_action(declare_x_pose_cmd)
    ld.add_action(declare_y_pose_cmd)
    ld.add_action(start_gzserver_cmd)
    ld.add_action(start_gzclient_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(spawn_robot_cmd)
    
    return ld
