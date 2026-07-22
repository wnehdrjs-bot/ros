import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSProfile, QoSReliabilityPolicy

class Qos_M_Pub(Node):
    def __init__(self):
        super().__init__("message_pub")
        
        # QoS 프로필 설정
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_ALL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        
        # 퍼블리셔 생성
        self.pub = self.create_publisher(String, "message", self.qos_profile)
        
        # 1초마다 timer_callback 호출
        self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        # "message" 토픽으로 전송
        msg = String()
        msg.data = f"Who? ({self.count}) msg: String"
        self.get_logger().info(f"[pub1] {msg.data}")
        self.pub.publish(msg)

        self.count += 1  # 카운터 증가

def main(args=None):
    rclpy.init(args=args)

    node = Qos_M_Pub()  # 클래스 이름에 맞게 MPub() -> Qos_M_Pub() 수정   
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("키보드 인터럽트")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()