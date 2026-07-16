#!/usr/bin/env python3
import rclpy
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def main():
    rclpy.init()

    # Create our navigation commander
    navigator = BasicNavigator()
    navigator.set_parameters([rclpy.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])

    print("🤖 [Navigator] Booting up Nav2 simple commander...")

    # 1. Set initial pose (Where the robot spawns in Gazebo: x = -2.0, y = -0.5)
    # This aligns the robot's localization grid with the simulation world.
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = -2.0
    initial_pose.pose.position.y = -0.5
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 1.0
    
    print("📍 [Navigator] Setting initial pose to [-2.0, -0.5]...")
    navigator.setInitialPose(initial_pose)

    # Wait for Navigation2 stack to start up and be ready
    print("⏳ [Navigator] Waiting for Nav2 servers to activate (this can take a few seconds)...")
    navigator.waitUntilNav2Active()
    print("✅ [Navigator] Nav2 is active and ready to plan paths!")

    # 2. Define the navigation target (Goal)
    # Let's send the robot to the upper-right corner of the map
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.5
    goal_pose.pose.position.y = 1.5
    goal_pose.pose.orientation.z = 0.707
    goal_pose.pose.orientation.w = 0.707

    print("🚀 [Navigator] Sending goal command: Navigate to [x=1.5, y=1.5]!")
    navigator.goToPose(goal_pose)

    # 3. Monitor navigation progress in a loop
    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(f"📦 [Nav Feedback] Distance left: {feedback.distance_remaining:.2f} meters | "
                  f"⏱️ Est. Time: {Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9:.1f} sec")

    # 4. Handle navigation completion
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("🎉 [Navigator] Success! The robot has reached the destination!")
    elif result == TaskResult.CANCELED:
        print("🛑 [Navigator] Navigation was canceled by the user!")
    elif result == TaskResult.FAILED:
        print("💥 [Navigator] Uh-oh! Navigation failed. Check for obstacles blockages!")
    else:
        print("❓ [Navigator] Received unknown status code.")

    # Shutdown the navigator nodes cleanly
    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
