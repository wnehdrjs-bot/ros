import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MPub(Node):
    def __init__(self):
        super().__init__("message_pub")
        
        # 1초마다 timer_callback 호출
        self.create_timer(1.0, self.timer_callback)
        self.pub = self.create_publisher(String, "message", 10)
        self.pub2 = self.create_publisher(String, "message2", 10)
        self.count = 0

    def timer_callback(self):
        # 1. "message" 토픽으로 전송
        msg = String()
        msg.data = f"Who? ({self.count}) msg: String"
        self.get_logger().info(f"[pub1] {msg.data}")
        self.pub.publish(msg)

        # 2. "message2" 토픽으로 전송 (pub2 사용!)
        msg2 = String()
        msg2.data = f"You? ({self.count}) msg2: String"
        self.get_logger().info(f"[pub2] {msg2.data}")
        self.pub2.publish(msg2)

        self.count += 1  # 카운터 증가

def main(args=None):
    rclpy.init(args=args)

    node = MPub()    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("키보드 인터럽트")
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
    print('Hi from my_py_pkg.')

if __name__ == '__main__':
    main()