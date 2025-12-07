---
sidebar_position: 5
---

# Packages and Workspaces

This document covers how to create and manage packages and workspaces in ROS 2.

## Creating a Package

```bash
ros2 pkg create --build-type ament_python my_robot_package
```

## Creating a Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Package.xml

The package.xml file contains metadata about the package.