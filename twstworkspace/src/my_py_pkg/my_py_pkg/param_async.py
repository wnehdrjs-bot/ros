import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.parameter_service import AsyncParameterClient


class ParamAsync(Node):
    def __init__(self):
        super().__init__("param_async_client")
        self.target_node_name = "/tparam"
        self.parameter_client = AsyncParameterClient(self, self.target_node_name)
        self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        if not self.parameter_client.service_is_ready():
            return

        parameter = Parameter(
            name="my_param",
            type_=Parameter.Type.STRING,
            value=f"외부 노드에서 변경한 값 {self.count}",
        )
        self.count += 1
        future = self.parameter_client.set_parameters([parameter])
        future.add_done_callback(self.parameter_result_callback)

    def parameter_result_callback(self, future):
        try:
            result = future.result()
            print(result)
        except Exception as e:
            print(e)


def main(args=None):
    rclpy.init(args=args)
    node = ParamAsync()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("키보드 인터럽트")
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()