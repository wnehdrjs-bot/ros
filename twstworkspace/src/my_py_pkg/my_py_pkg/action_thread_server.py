import time

import rclpy
from action_msgs.msg import GoalStatus
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from user_interface.action import Fibonacci


class Action_server(Node):

    def __init__(self):
        super().__init__("action_server")

        # 멀티 스레드 처리를 위한 콜백 그룹 생성
        self.callback_group = ReentrantCallbackGroup()

        # 액션 서버 생성 및 콜백 그룹 할당
        self.action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci_server",
            execute_callback=self.execute_callback,
            callback_group=self.callback_group,
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info(f"현재 상태: {goal_handle.status}")
        self.get_logger().info(
            f"GoalStatus.STATUS_EXECUTING 값: {GoalStatus.STATUS_EXECUTING}"
        )

        if goal_handle.status == GoalStatus.STATUS_EXECUTING:
            self.get_logger().info("현재 실행 중입니다.")

        goal: Fibonacci.Goal = goal_handle.request
        step = goal.step
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.temp_seq = [0, 1]

        for i in range(1, step):
            feedback_msg.temp_seq.append(
                feedback_msg.temp_seq[i] + feedback_msg.temp_seq[i - 1]
            )
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f"진행 중 상태: {goal_handle.status}")
            time.sleep(1)

        goal_handle.succeed()
        self.get_logger().info(f"완료 상태: {goal_handle.status}")

        result = Fibonacci.Result()
        result.seq = feedback_msg.temp_seq
        return result


def main(args=None):
    rclpy.init(args=args)

    node = Action_server()

    # MultiThreadedExecutor 가동
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        print("키보드 인터럽트로 종료합니다.")
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()