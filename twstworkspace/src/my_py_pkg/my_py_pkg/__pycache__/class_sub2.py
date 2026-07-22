import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class M_pub(Node):
    def __init__(self):
        super().__init__("massage_sub2")
    
       #subscripsun callback
        self.create_subscription(String, "message2", self.sub_callback, 10)
        self.count = 0

    def sub_callback(self,msg2: String):
        self.get_logger().info(msg2.data)
        
def main(args=None):
    rclpy.init(args=args) # RMW 활성화

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