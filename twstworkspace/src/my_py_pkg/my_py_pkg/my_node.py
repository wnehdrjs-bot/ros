import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# timer_callback에 node, pub, state(카운터)를 함께 전달
def timer_callback(node, pub, state):
    msg = String()
    msg.data = f"Who? {state['count']}"
    
    pub.publish(msg)  # 1. 메시지 발행
    node.get_logger().info(f"Published: {msg.data}")  # 2. 터미널 로그 출력
    state['count'] += 1

def main(args=None):
    rclpy.init(args=args) # RMW 활성화
    
    node = Node("massage_pub") # 노드 생성
    pub = node.create_publisher(String, "message", 10) # 퍼블리셔 생성
    
    # 카운터를 유지하기 위한 상태 객체 (dict)
    state = {'count': 0}
    
    # lambda로 node, pub, state를 함께 전달
    node.create_timer(1.0, lambda: timer_callback(node, pub, state))
    
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
