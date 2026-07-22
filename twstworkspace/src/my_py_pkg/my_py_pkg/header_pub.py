import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class M_pub(Node):
    def __init__(self):
        super().__init__("header_pub")
        
        # 1/10초 (0.1초 = 10Hz) 마다 timer_callback 호출
        self.create_timer(1 , self.timer_callback)
        self.pub = self.create_publisher(Header, "time", 10)
        self.count = 0

    def timer_callback(self):
        msg = Header()
        msg.frame_id = f"time_test_{self.count}"
        
        # 1. 점(.) 추가하여 올바른 함수 호출
        msg.stamp = self.get_clock().now().to_msg()
        
        # 2. Header 메시지 구조에 맞춰 로그 출력 (msg.data 제거)
        self.get_logger().info(f"Published Header - frame_id: {msg.frame_id}, stamp: {msg.stamp.sec}.{msg.stamp.nanosec}")
        
        self.pub.publish(msg)
        self.count += 1  # 카운터 증가

def main(args=None):
    rclpy.init(args=args) # RMW 활성화

    # 3. 선언된 클래스 이름(M_pub)과 동일하게 맞춤
    node = M_pub()    
    try:
        rclpy.spin(node) # 루프 실행
    except KeyboardInterrupt:
        node.get_logger().info("키보드 인터럽트")
    finally:
        node.destroy_node()
        rclpy.shutdown() # rclpy 종료
    
    print('Hi from my_py_pkg.')

if __name__ == '__main__':
    main()