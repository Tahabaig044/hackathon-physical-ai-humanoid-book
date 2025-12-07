---
sidebar_position: 2
---

# ROS 2 Installation

This document provides instructions for installing ROS 2 on different platforms.

## System Requirements

- Ubuntu 22.04 (Jammy) or Windows 10/11 or macOS
- At least 5GB of free disk space
- Internet connection for downloading packages

## Ubuntu Installation

```bash
# Add the ROS 2 GPG key and repository
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install ros-humble-desktop
```

## Windows Installation

Follow the instructions at the official ROS 2 documentation for Windows installation.

## macOS Installation

Follow the instructions at the official ROS 2 documentation for macOS installation.