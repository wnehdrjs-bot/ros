cmake_minimum_required(VERSION 3.8)
project(user_interface)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Action 생성에 필요한 action_msgs 추가
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(action_msgs REQUIRED)

# 2. 인터페이스(메시지, 서비스, 액션) 생성
rosidl_generate_interfaces(${PROJECT_NAME}     # ${twstworkspace} -> ${PROJECT_NAME}으로 수정
  "msg/UserInt.msg"
  "srv/AddAndOdd.srv"
  "action/Fibonacci.action"                     # axtion -> action 오타 수정
  DEPENDENCIES std_msgs action_msgs             # action_msgs 의존성 추가
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()