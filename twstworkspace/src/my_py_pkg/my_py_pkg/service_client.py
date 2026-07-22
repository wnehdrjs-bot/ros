import rclpy
from rclpy.node import Node
from user_interface.srv import AddAndOdd


class ServiceClient(Node):
    def __init__(self):
        super().__init__("service_client")
        self.client = self.create_client(AddAndOdd, "add_and_odd")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available")

        self.request = AddAndOdd.Request()
        self.create_timer(3.0, self.send_request)
        self.create_timer(1.0, self.update)
        self.count = 0

    def send_request(self):
        self.get_logger().info(f"시작해 요청함{self.count}")
        self.request.inta = 4
        self.request.intb = 0 + self.count
        self.count += 1

        self.future = self.client.call_async(self.request)
        self.future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        response = future.result()
        self.get_logger().info(f"{response.sum}")
        self.get_logger().info(f"{response.odd}")

    def update(self):
        self.get_logger().info("updating!!")


def main(args=None):
    rclpy.init(args=args)

    node = ServiceClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()