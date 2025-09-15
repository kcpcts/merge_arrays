#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')
        
        # Create subscribers for input arrays
        self.subscription1 = self.create_subscription(
            Int32MultiArray,
            '/input/array1',
            self.array1_callback,
            10
        )
        
        self.subscription2 = self.create_subscription(
            Int32MultiArray,
            '/input/array2',
            self.array2_callback,
            10
        )
        
        # Create publisher for merged output
        self.publisher = self.create_publisher(
            Int32MultiArray,
            '/output/array',
            10
        )
        
        # Store the latest arrays
        self.array1_data = None
        self.array2_data = None
        
        self.get_logger().info('Merge Arrays Node has been started')
    
    def array1_callback(self, msg):
        """Callback for first input array"""
        self.array1_data = msg.data
        self.get_logger().debug(f'Received array1: {self.array1_data}')
        self.merge_and_publish()
    
    def array2_callback(self, msg):
        """Callback for second input array"""
        self.array2_data = msg.data
        self.get_logger().debug(f'Received array2: {self.array2_data}')
        self.merge_and_publish()
    
    def merge_and_publish(self):
        """Merge two sorted arrays and publish if both are available"""
        if self.array1_data is not None and self.array2_data is not None:
            # Merge the two sorted arrays using two-pointer technique
            merged_data = self.merge_sorted_arrays(list(self.array1_data), list(self.array2_data))
            
            # Create output message
            output_msg = Int32MultiArray()
            output_msg.data = merged_data
            
            # Publish merged array
            self.publisher.publish(output_msg)
            self.get_logger().info(f'Published merged array with {len(merged_data)} elements: {merged_data}')
    
    def merge_sorted_arrays(self, arr1, arr2):
        """
        Merge two sorted arrays into one sorted array
        Uses two-pointer technique for O(n+m) time complexity
        """
        merged = []
        i, j = 0, 0
        
        # Compare elements from both arrays and add smaller one
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                merged.append(arr1[i])
                i += 1
            else:
                merged.append(arr2[j])
                j += 1
        
        # Add remaining elements from arr1 (if any)
        while i < len(arr1):
            merged.append(arr1[i])
            i += 1
        
        # Add remaining elements from arr2 (if any)
        while j < len(arr2):
            merged.append(arr2[j])
            j += 1
        
        return merged


def main(args=None):
    rclpy.init(args=args)
    
    merge_arrays_node = MergeArraysNode()
    
    try:
        rclpy.spin(merge_arrays_node)
    except KeyboardInterrupt:
        pass
    finally:
        merge_arrays_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
