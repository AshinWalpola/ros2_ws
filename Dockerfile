# Use an official ROS 2 Jazzy image for ARM64 (auto-detects architecture)
FROM ros:jazzy-ros-base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Update package list and install dependencies
RUN apt update && apt install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep (handle case where it is already initialized)
RUN rosdep init || true && rosdep update

# Ensure ROS 2 setup is sourced in every new shell
RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc

# Set working directory for ROS 2 workspace
WORKDIR /ros2_ws
RUN mkdir -p src

# Default command to keep container interactive
CMD ["/bin/bash"]
