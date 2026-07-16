#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.set_parameters([rclpy.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])
        
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription_ = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        
        self.declare_parameter('safe_distance', 0.6) # meters
        self.declare_parameter('linear_speed', 0.15) # m/s
        self.declare_parameter('angular_speed', 0.5) # rad/s
        
        self.get_logger().info('🟢 Obstacle Avoidance Node Online! Subscribed to /scan, publishing to /cmd_vel.')
        
    def scan_callback(self, msg):
        safe_distance = self.get_parameter('safe_distance').get_parameter_value().double_value
        linear_speed = self.get_parameter('linear_speed').get_parameter_value().double_value
        angular_speed = self.get_parameter('angular_speed').get_parameter_value().double_value
        
        # Look at the front sector of the lidar (from -30 degrees to +30 degrees)
        # LaserScan contains ranges array. 0 is front-center, positive angles are counter-clockwise.
        # Turtlebot3 lidar has 360 beams, 1 per degree.
        # Front sector indexes: 0 to 30 and 330 to 359
        front_ranges = msg.ranges[0:30] + msg.ranges[330:360]
        
        # Filter out invalid values (inf, nan)
        valid_ranges = [r for r in front_ranges if r > 0.0]
        
        if not valid_ranges:
            return
            
        min_front_distance = min(valid_ranges)
        
        cmd_vel_msg = Twist()
        
        if min_front_distance < safe_distance:
            self.get_logger().warn(f'⚠️ Obstacle detected! Distance: {min_front_distance:.2f}m. Turning to avoid collision...')
            # Stop moving forward and pivot
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = angular_speed
        else:
            # Drive forward in a straight line
            cmd_vel_msg.linear.x = linear_speed
            cmd_vel_msg.angular.z = 0.0
            
        self.publisher_.publish(cmd_vel_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
