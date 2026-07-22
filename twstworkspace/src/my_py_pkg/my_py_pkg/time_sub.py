import rclpy
from rclpy.node import Node
# 1. Header 타입 import 추가
from std_msgs.msg import String, Header

class MassageAndHeaderSub(Node):
    def __init__(self):
        super().__init__("massage_and_header_sub")
    
        # 2. "message2" 토픽 구독 (String) -> string_callback 연결
        self.create_subscription(String, "message", self.string_callback, 10)
        
        # 3. "time" 토픽 구독 (Header) -> header_callback 연결
        self.create_subscription(Header, "time", self.header_callback, 10)
        
        self.count = 0

    # String 수신 콜백
    def string_callback(self, msg: String):
        self.get_logger().info(f"[String] {msg.data}")

    # Header 수신 콜백 (함수를 별도로 분리)
    def header_callback(self, time: Header):
        # Header는 .data 대신 frame_id와 stamp를 사용합니다.
        self.get_logger().info(f"[Header] frame_id: {time.frame_id}, stamp: {time.stamp.sec}.{time.stamp.nanosec}")


def main(args=None):
    rclpy.init(args=args) # RMW 활성화

    node = MassageAndHeaderSub()    
    try:
        rclpy.spin(node) # 루프 실행 (두 콜백 모두 대기)
    except KeyboardInterrupt:
        node.get_logger().info("키보드 인터럽트")
    finally:
        node.destroy_node()
        rclpy.shutdown() # rclpy 종료
    
    print('Hi from my_py_pkg.')

if __name__ == '__main__':
    main()