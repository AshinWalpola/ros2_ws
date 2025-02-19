# Use an official ROS 2 Jazzy image for ARM64
FROM ros:jazzy-ros-base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Update package list and install necessary dependencies for ROS 2
RUN apt update && apt install -y \
    python3-pip \
    python3-venv \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

# Install WebSockets in a separate virtual environment
RUN python3 -m venv /ros2_ws/venv
RUN /ros2_ws/venv/bin/pip install --no-cache-dir websockets

# Ensure ROS 2 setup is sourced for system-wide Python usage
RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc

# Ensure virtual environment is available but NOT overriding system Python
RUN echo "alias python_ws='/ros2_ws/venv/bin/python'" >> ~/.bashrc
RUN echo "alias pip_ws='/ros2_ws/venv/bin/pip'" >> ~/.bashrc

# Initialize rosdep (handle case where it is already initialized)
RUN rosdep init || true && rosdep update

# Set working directory for ROS 2 workspace
WORKDIR /ros2_ws
RUN mkdir -p src

# Default command to keep container interactive
CMD ["/bin/bash"]