FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
# Basic tools
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common \
    git \
    vim \
    build-essential \
    python3-pip \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Locale
RUN locale-gen en_US en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# ROS 2 repository
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    > /etc/apt/sources.list.d/ros2.list

RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'

RUN curl -sSL https://packages.osrfoundation.org/gazebo.key | apt-key add -

# Install ROS 2 Humble Desktop
RUN apt-get update && apt-get install -y \
    ros-humble-desktop

RUN apt-get install -y ros-dev-tools

# Initialize rosdep
RUN rosdep init || true

RUN apt-get update && apt-get install -y \
    zsh\
    curl

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN apt-get install -y micro

RUN apt-get update && apt-get install -y gazebo libgazebo-dev ros-humble-gazebo-ros-pkgs

# Install Nav2, SLAM Toolbox, TurtleBot3, and DDS
RUN apt-get update && apt-get install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-turtlebot3 \
    ros-humble-turtlebot3-msgs \
    ros-humble-turtlebot3-gazebo \
    ros-humble-turtlebot3-simulations \
    ros-humble-rmw-cyclonedds-cpp \
    ros-humble-xacro \
    && rm -rf /var/lib/apt/lists/*

# Source ROS automatically and set DDS & Turtlebot3 environment variables
RUN echo "source /opt/ros/humble/setup.zsh" >> /root/.zshrc && \
    echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models" >> /root/.zshrc

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models" >> /root/.bashrc

# Global system environment variables (active for both interactive and non-interactive sessions)
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ENV ROS_LOCALHOST_ONLY=1
ENV GAZEBO_MODEL_DATABASE_URI=""
ENV TURTLEBOT3_MODEL=waffle
ENV GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/humble/share/turtlebot3_gazebo/models





WORKDIR /workspace

CMD ["/bin/zsh"]

