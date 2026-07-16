#!/usr/bin/env python3
import rclpy
import time
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

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

    # Checkpoints to patrol
    waypoints = [
        create_pose(navigator, -0.5, -0.5, 0.0, 1.0),      # Checkpoint 1 (center open area)
        create_pose(navigator, 1.8, 1.5, 0.707, 0.707),     # Checkpoint 2 (top right corner room)
        create_pose(navigator, 1.8, -1.2, 1.0, 0.0)         # Checkpoint 3 (bottom right corridor)
    ]

    print(f"🗺️ [Patrol] Loaded {len(waypoints)} checkpoints. Starting patrol loop!")

    rounds = 0
    max_rounds = 2

    while rounds < max_rounds:
        print(f"\n🌀 --- STARTING PATROL LAP #{rounds + 1} ---")
        
        for idx, checkpoint in enumerate(waypoints):
            print(f"📍 Heading to Checkpoint {idx + 1}/{len(waypoints)}...")
            
            # Send the robot to the checkpoint
            navigator.goToPose(checkpoint)
            
            # Monitor progress
            i = 0
            while not navigator.isTaskComplete():
                i += 1
                feedback = navigator.getFeedback()
                if feedback and i % 5 == 0:
                    print(f"   📦 Distance remaining: {feedback.distance_remaining:.2f} meters")
                    
            # Check the outcome of the navigation task
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                print(f"   🎉 Checkpoint {idx + 1} reached successfully! Initiating scanning spin...")
                
                # Perform a full 360 spin (6.28 radians)
                navigator.spin(spin_dist=6.28, time_allowance=15)
                while not navigator.isTaskComplete():
                    pass
                
                print("   😴 Spin complete. Pausing for 2 seconds to scan...")
                time.sleep(2.0)
            elif result == TaskResult.CANCELED:
                print("   🛑 Navigation was canceled! Ending patrol.")
                return
            elif result == TaskResult.FAILED:
                print("   💥 Navigation failed! Obstacle likely blocking the way. Aborting.")
                return
            
        rounds += 1

    print("\n🏆 MISSION ACCOMPLISHED! All patrol rounds completed successfully.")
    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
