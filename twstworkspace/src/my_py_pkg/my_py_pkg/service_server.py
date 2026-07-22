import rclpy
from rclpy.node import Node
from user_interface.srv import AddAndOdd 
import time

class ServiceServer(Node):
    def __init__(self):
        # 노드 이름 설정 (message_sub 등 직관적인 이름 추천)
        super().__init__("service_server")
        self.srv = self.create_service(AddAndOdd, "add_and_odd", self.add_callback)


    def add_callback(self, request, response):
        response.sum = request.inta + request.intb
        time.sleep(1)
        if response.sum % 2:
            response.odd = "Two ints sum is odd"
        else:
            response.odd = "Two ints sum is not odd"
        
        return response
        


def main(args=None):
    rclpy.init(args=args)

    node = ServiceServer()    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("키보드 인터럽트로 인한 종료")
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
    print('Hi from my_py_pkg.')


if __name__ == '__main__':
    main()