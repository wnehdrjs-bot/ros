import time
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup  # 1. callback_groups로 오타 수정
from user_interface.srv import AddAndOdd 
# 2. 불필요하고 잘못된 import thread 제거


class ServiceServer(Node):
    def __init__(self):
        super().__init__("service_server")
        
        # 병렬 처리를 허용하는 ReentrantCallbackGroup 생성
        self.callback_group = ReentrantCallbackGroup()
        
        # 서비스 생성 시 callback_group 지정
        self.srv = self.create_service(
            AddAndOdd, 
            "add_and_odd", 
            self.add_callback,
            callback_group=self.callback_group
        )

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

    # MultiThreadedExecutor 인스턴스 생성 및 노드 추가
    executor = MultiThreadedExecutor()
    node = ServiceServer()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        # 안전한 자원 해제
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()