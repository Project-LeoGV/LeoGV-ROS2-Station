cmake_minimum_required(VERSION 3.5)
project(leogv_gazebo)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
ament_python_install_package(Scripts)

install(
  DIRECTORY launch rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  Scripts/command_timeout.py
  DESTINATION lib/${PROJECT_NAME}
)
ament_package()
