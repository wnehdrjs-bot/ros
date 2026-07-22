import rclpy
from rclpy.node import Node
# 1. std_msge import 제거 및 커스텀 메시지(UserInt) 사용
from user_interface.msg import UserInt 

class MPub(Node):
    def __init__(self):
        super().__init__("_pub")
        
        # 1초마다 timer_callback 호출
        self.create_timer(1.0, self.timer_callback)
        self.pub = self.create_publisher(UserInt, "message", 10)
        
        self.count = 0

    def timer_callback(self):
        # 2. String() 대신 UserInt() 객체 생성
        msg = UserInt()
        msg.header.frame_id = "timetest"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.user_int = 12
        msg.user_int2 = 23
        msg.user_int3 = 53
        
        # 3. msg.data 대신 커스텀 메시지의 필드값 로깅
        self.get_logger().info(f"[pub1] {msg.user_int}, {msg.user_int2}, {msg.user_int3}")
        
        self.pub.publish(msg)

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