import math
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Color, Pose


class Move_tutle(Node):
    def __init__(self):
        super().__init__("move_turtle")  # 노드 이름
        
        # 0.1초(10Hz) 타이머 설정
        self.create_timer(0.1, self.timer_callback)
        self.pub = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        
        # 센서 및 위치 구독
        self.create_subscription(Pose, "turtle1/pose", self.pose_callback, 10)
        self.create_subscription(Color, "turtle1/color_sensor", self.color_callback, 10)
        
        self.count = 0.0
        self.pose = Pose()
        self.color = Color()
        
        # 패턴 상태 관리 ("ZIGZAG", "STAR", "SPIRAL")
        self.mode = "ZIGZAG"
        self.mode_timer = 0.0
        
        # 별 그리기용 세부 상태
        self.star_step = 0
        self.star_sub_timer = 0.0

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def color_callback(self, msg: Color):
        self.color = msg

    def timer_callback(self):
        msg = Twist()
        self.mode_timer += 0.1

        # -------------------------------------------------------------
        # 1. 안전 장치 (Wall Safety Check)
        # turtlesim의 맵 크기는 약 0 ~ 11.1 범위입니다.
        # 벽 경계(1.5 이하, 9.5 이상)에 접근하면 급회전하여 탈출합니다.
        # -------------------------------------------------------------
        if self.pose.x < 1.5 or self.pose.x > 9.5 or self.pose.y < 1.5 or self.pose.y > 9.5:
            msg.linear.x = 1.0
            msg.angular.z = 2.5  # 벽 반대편으로 빠르게 회전
            self.pub.publish(msg)
            self.get_logger().warn("⚠️ 벽 접근! 경계 회피 구동 중...", throttle_duration_sec=1.0)
            return

        # -------------------------------------------------------------
        # 2. 패턴 모드 자동 전환 (10초 주기 또는 특정 색상 감지 시)
        # -------------------------------------------------------------
        if self.mode_timer > 10.0:
            self.mode_timer = 0.0
            # 모드 순환: ZIGZAG -> STAR -> SPIRAL -> ZIGZAG
            if self.mode == "ZIGZAG":
                self.mode = "STAR"
                self.star_step = 0
                self.star_sub_timer = 0.0
            elif self.mode == "STAR":
                self.mode = "SPIRAL"
            else:
                self.mode = "ZIGZAG"
            self.get_logger().info(f"🔄 패턴 변경: [{self.mode}] 모드")

        # -------------------------------------------------------------
        # 3. 각 모드별 이동 로직
        # -------------------------------------------------------------
        if self.mode == "ZIGZAG":
            # [지그재그 패턴]
            # 앞으로 가면서 삼각함수(Sin)로 좌우 회전을 빠르게 교대
            msg.linear.x = 2.2
            msg.angular.z = 3.0 * math.sin(self.mode_timer * 4.0)

        elif self.mode == "STAR":
            # [별 모양 패턴]
            # 직진(0.8초) -> 제자리 급회전(144도에 맞춘 타이밍) 반복
            self.star_sub_timer += 0.1
            if self.star_step % 2 == 0:
                # 변 그리기 (직진)
                msg.linear.x = 2.5
                msg.angular.z = 0.0
                if self.star_sub_timer >= 0.8:
                    self.star_step += 1
                    self.star_sub_timer = 0.0
            else:
                # 꼭짓점 꺾기 (회전)
                msg.linear.x = 0.0
                msg.angular.z = 2.5
                if self.star_sub_timer >= 0.6:  # 약 144도 회전 주기
                    self.star_step += 1
                    self.star_sub_timer = 0.0

        elif self.mode == "SPIRAL":
            # [소라빵/나선형 패턴]
            # 곡선 회전을 유지하면서 직진 속도를 조금씩 늘림
            self.count += 0.02
            if self.count > 2.5:
                self.count = 0.2
            
            msg.linear.x = 0.8 + self.count
            msg.angular.z = 2.0

        # 발행
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Move_tutle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("키보드 인터럽트로 종료되었습니다.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()