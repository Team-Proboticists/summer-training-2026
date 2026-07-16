#!/bin/bash
set -e

echo "=========================================================="
echo "          ROS2 / Gazebo / Nav2 Workspace Init            "
echo "=========================================================="

WORKSPACE_DIR="/workspace"
PKG_DIR="${WORKSPACE_DIR}/src/ros2_nav_lecture"
MAPS_DIR="${PKG_DIR}/maps"
CONFIG_DIR="${PKG_DIR}/config"

# Create directories
mkdir -p "${MAPS_DIR}"
mkdir -p "${CONFIG_DIR}"

# Check if ROS is installed/available
if [ ! -d "/opt/ros/humble" ]; then
    echo "ERROR: /opt/ros/humble not found! Please run this script INSIDE the docker container."
    exit 1
fi

echo "[1/3] Copying standard TurtleBot3 maps..."
cp /opt/ros/humble/share/turtlebot3_navigation2/map/map.yaml "${MAPS_DIR}/tb3_map.yaml"
cp /opt/ros/humble/share/turtlebot3_navigation2/map/map.pgm "${MAPS_DIR}/tb3_map.pgm"

# Update map.yaml image path reference
sed -i 's|image: map.pgm|image: tb3_map.pgm|g' "${MAPS_DIR}/tb3_map.yaml"

echo "[2/3] Copying standard TurtleBot3 Nav2 configuration parameters..."
cp /opt/ros/humble/share/turtlebot3_navigation2/param/waffle.yaml "${CONFIG_DIR}/nav2_params.yaml"
# Fix plugin names from :: to / for planner and behavior server (required in Humble)
sed -i 's|nav2_navfn_planner::NavfnPlanner|nav2_navfn_planner/NavfnPlanner|g' "${CONFIG_DIR}/nav2_params.yaml"
sed -i 's|nav2_behaviors::|nav2_behaviors/|g' "${CONFIG_DIR}/nav2_params.yaml"

# Inject use_sim_time: True programmatically into every node's ros__parameters block
python3 -c "
import yaml
fpath = '${CONFIG_DIR}/nav2_params.yaml'
data = yaml.safe_load(open(fpath))
def inject(d):
    if not isinstance(d, dict): return
    for k, v in d.items():
        if k == 'ros__parameters' and isinstance(v, dict):
            v['use_sim_time'] = True
        elif isinstance(v, dict):
            inject(v)
inject(data)
# Automatically set AMCL initial pose to match simulation spawn coordinates
data['amcl']['ros__parameters']['set_initial_pose'] = True
data['amcl']['ros__parameters']['initial_pose']['x'] = -2.0
data['amcl']['ros__parameters']['initial_pose']['y'] = -0.5
yaml.dump(data, open(fpath, 'w'), default_flow_style=False)
"

echo "[3/3] Setting executable permissions on python nodes..."
chmod +x ${PKG_DIR}/ros2_nav_lecture/simple_navigator.py
chmod +x ${PKG_DIR}/ros2_nav_lecture/patrol_challenge.py
chmod +x ${PKG_DIR}/ros2_nav_lecture/patrol_challenge_solution.py
chmod +x ${PKG_DIR}/ros2_nav_lecture/obstacle_avoidance.py

echo ""
echo "Workspace Initialization Complete!"
echo "Now you can compile the workspace inside your container container using:"
echo "  colcon build"
echo "=========================================================="
