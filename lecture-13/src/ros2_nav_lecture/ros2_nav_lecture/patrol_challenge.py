#!/usr/bin/env python3
import rclpy
import time
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

"""
🕵️‍♂️ MISSION: THE PERIMETER PATROL GUARD
=========================================
Hey Tinkerer! Welcome to your self-guided challenge.
Your goal is to program your TurtleBot3 Waffle to autonomously patrol
a series of checkpoints in the Gazebo simulator.

🛠️ Instructions:
1. Complete the TODO blocks below to write the patrol script.
2. Compile your edits in the docker container:
   colcon build --symlink-install
3. Make sure Gazebo & Nav2 are running!
4. Launch the patrol:
   ros2 run ros2_nav_lecture patrol_challenge

Let's get tinkering!
"""

def create_pose(navigator, x, y, yaw_z, yaw_w):
    """Helper function to create a 2D navigation pose."""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = yaw_z
    pose.pose.orientation.w = yaw_w
    return pose

def main():
    rclpy.init()
    navigator = BasicNavigator()
    navigator.set_parameters([rclpy.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])

    print("🛰️ [Patrol] Connecting to Nav2 servers...")
    navigator.waitUntilNav2Active()
    print("🛰️ [Patrol] Connection established! Preparing route planner.")

    # ==========================================
    # TODO 1: Define your patrol checkpoints!
    # Tip: Use 'create_pose(navigator, x, y, yaw_z, yaw_w)'
    # Here are some coordinates you can try on the map:
    #   - Center Open Area: [x=0.0, y=0.0]
    #   - Top-Right Room: [x=1.8, y=1.5]
    #   - Bottom-Right Zone: [x=1.8, y=-1.2]
    #   - Middle-Left Corridor: [x=-1.5, y=1.2]
    # ==========================================
    waypoints = [
        # 🧪 Add your waypoints below:
        # e.g. create_pose(navigator, -0.5, -0.5, 0.0, 1.0),
    ]

    if not waypoints:
        print("❌ ERROR: You haven't added any waypoints yet! Open the code and complete TODO 1.")
        return

    print(f"🗺️ [Patrol] Loaded {len(waypoints)} checkpoints. Starting patrol loop!")

    rounds = 0
    max_rounds = 2  # How many laps the patrol should run

    while rounds < max_rounds:
        print(f"\n🌀 --- STARTING PATROL LAP #{rounds + 1} ---")
        
        for idx, checkpoint in enumerate(waypoints):
            print(f"📍 Heading to Checkpoint {idx + 1}/{len(waypoints)}...")
            
            # ==========================================
            # TODO 2: Command the robot to navigate to the current checkpoint
            # Hint: Use navigator.goToPose(...)
            # ==========================================
            
            
            # ==========================================
            # TODO 3: Create a feedback loop to monitor progress
            # Print the remaining distance as the robot drives.
            # Hint: Keep looping while not navigator.isTaskComplete().
            #       Print the feedback using navigator.getFeedback().
            # ==========================================
            
            
            # ==========================================
            # TODO 4: Act on completion!
            # If the robot reached the checkpoint successfully:
            #   1. Print a success message.
            #   2. Perform a 360-degree celebration spin!
            #      (Hint: use navigator.spin(spin_dist=6.28, time_allowance=15)
            #       and wait for that task to complete).
            # If it failed or was canceled, print a warning and exit.
            # Hint: Use navigator.getResult() to check.
            # ==========================================
            pass

        rounds += 1

    print("\n🏆 MISSION ACCOMPLISHED! All patrol rounds completed successfully.")
    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
