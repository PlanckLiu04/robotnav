# Project Proposal

# RobotNav：二维路径规划与 PID 导航控制仿真系统

## 1. 项目概述

**RobotNav** 是一个使用 Python 实现的二维机器人导航仿真项目。

项目中，用户可以在一个网格地图上绘制障碍物，设置起点和终点。程序会使用 BFS 和 A* 等路径规划算法寻找一条从起点到终点的路径，并将搜索过程可视化。随后，一个具有位置和朝向的小机器人会沿着规划出的路径运动。机器人运动过程中使用简单的 PID heading controller 控制朝向，使机器人能够更稳定地跟踪路径点。

这个项目的目标不是实现复杂真实机器人系统，而是通过一个难度适中、可视化强、可以在 2 个月内完成的小项目，帮助学习者理解：

* Python 项目开发；
* Miniconda 环境管理；
* 网格地图与二维数组；
* BFS / A* 路径规划；
* 队列、优先队列、图搜索；
* 机器人位姿、方向、速度；
* PID 控制器的基本思想；
* 可视化调试和项目展示。

---

## 2. 项目名称

英文名称：

**RobotNav: A 2D Path Planning and PID-based Navigation Simulator**

中文名称：

**RobotNav：二维路径规划与 PID 导航控制仿真系统**

---

## 3. 项目目标

本项目希望在 **8 周左右** 完成一个可运行、可展示、可讲清楚的小型 Python 项目。

完成后，项目应具备：

1. 可交互的二维网格地图；
2. 鼠标绘制障碍物；
3. 起点和终点设置；
4. BFS 路径规划；
5. A* 路径规划；
6. 搜索过程可视化；
7. 访问节点数、路径长度、运行时间统计；
8. 三角形机器人模型；
9. 基于 waypoint tracking 的路径跟踪；
10. PID heading controller 控制机器人转向；
11. 机器人轨迹、误差和 PID 参数可视化；
12. 完整 README、截图和演示视频。

---

## 4. 项目学习价值

### 4.1 对编程能力的帮助

通过本项目可以训练：

* Python 基础编程；
* 模块化项目结构；
* 面向对象设计；
* Pygame 图形界面；
* NumPy 数学计算；
* Git / GitHub 项目管理；
* Miniconda 环境管理；
* 使用 AI agent 辅助开发和调试。

### 4.2 对数据结构与算法的帮助

本项目会自然用到：

* 二维数组；
* 队列；
* 优先队列；
* 图搜索；
* BFS；
* A*；
* parent 回溯路径；
* 时间复杂度与空间复杂度分析。

### 4.3 对数学和控制理解的帮助

本项目会用到：

* 二维坐标；
* 向量；
* 距离；
* 角度；
* 方向误差；
* 机器人位姿；
* 线速度和角速度；
* PID 控制器；
* 反馈控制思想。

### 4.4 对项目展示的帮助

这个项目比较适合作为入门级 CS/robotics 项目展示，因为它有完整系统闭环：

```text
地图建模 → 路径规划 → 控制跟踪 → 可视化展示
```

---

## 5. 核心概念说明

### 5.1 什么是路径规划？

路径规划解决的问题是：

> 从起点到终点，机器人应该走哪一条路？

在本项目中，地图被表示成一个二维网格。每个格子可能是空地、障碍物、起点、终点、已访问节点或最终路径。

路径规划算法会在网格中搜索一条从起点到终点的可行路径。

---

### 5.2 什么是 BFS？

BFS 是 Breadth-First Search，也就是广度优先搜索。

它的直观理解是：

> 从起点开始，一圈一圈向外扩散，先访问离起点近的格子，再访问更远的格子。

BFS 的核心数据结构是队列。

在无权图中，BFS 可以找到从起点到终点的最短路径。

---

### 5.3 什么是 A*？

A* 是一种比 BFS 更有方向感的搜索算法。

BFS 会比较均匀地向四周扩散，而 A* 会估计哪些节点更接近终点，从而优先搜索更有希望的方向。

A* 的核心公式是：

```text
f(n) = g(n) + h(n)
```

其中：

```text
g(n)：从起点走到当前节点 n 的真实代价
h(n)：从当前节点 n 到终点的估计代价
f(n)：当前节点的综合评分
```

在二维网格中，常用的估计代价是曼哈顿距离：

```text
h = |x1 - x2| + |y1 - y2|
```

A* 的核心数据结构是优先队列。

---

### 5.4 为什么路径规划之后还需要控制？

路径规划只告诉我们：

> 应该走哪条路。

但它没有告诉我们：

> 机器人具体怎么动过去。

例如，A* 输出的路径可能是一串离散的点：

```text
[(5, 5), (6, 5), (7, 5), (8, 5), ...]
```

但机器人不是一个会瞬移的点。它有自己的位置、朝向、速度和角速度。它需要不断调整方向，逐步靠近当前目标点。

所以完整导航系统通常包含：

```text
路径规划器 Planner：决定走哪条路
路径跟踪器 Tracker：决定当前跟踪哪个路径点
控制器 Controller：决定如何转向和前进
机器人模型 Robot：根据控制输入更新位置和朝向
```

---

### 5.5 什么是 PID 控制器？

PID 是一种经典反馈控制器。

它根据当前误差计算控制输出，让系统逐渐接近目标。

PID 包含三部分：

```text
P：Proportional，比例项
I：Integral，积分项
D：Derivative，微分项
```

在本项目中，PID 控制器主要用于控制机器人朝向。

机器人当前朝向是：

```text
theta
```

机器人应该朝向目标点的方向是：

```text
theta_target
```

角度误差是：

```text
error = theta_target - theta
```

PID 控制器根据这个角度误差输出角速度：

```text
omega = Kp * error + Ki * integral(error) + Kd * derivative(error)
```

直观理解：

```text
P：误差越大，转得越快
I：如果长期有偏差，就慢慢补偿
D：如果变化太快，就抑制震荡
```

对于本项目，建议先从比较简单的版本开始：

```text
角速度 omega：由 PID 控制
线速度 v：由距离误差简单控制
```

---

## 6. 技术栈

### 6.1 开发语言

```text
Python
```

### 6.2 环境管理

使用：

```text
Miniconda
```

原因：

* 可以创建独立 Python 环境；
* 不容易污染系统 Python；
* 方便安装和管理依赖包；
* 后续项目多了也便于维护。

### 6.3 Python 依赖

建议使用：

```text
pygame
numpy
matplotlib
```

作用分别是：

```text
Pygame：图形窗口、鼠标交互、动画显示
NumPy：向量、距离、角度等数学计算
Matplotlib：后期绘制算法对比图
```

---

## 7. Miniconda 环境配置

### 7.1 创建项目环境

建议环境名叫：

```text
robotnav
```

创建环境：

```bash
conda create -n robotnav python=3.11
```

激活环境：

```bash
conda activate robotnav
```

安装依赖：

```bash
pip install pygame numpy matplotlib
```

或者使用 conda-forge：

```bash
conda install -c conda-forge pygame numpy matplotlib
```

### 7.2 生成依赖文件

项目中建议保留一个 `requirements.txt`：

```bash
pip freeze > requirements.txt
```

后续别人可以用：

```bash
pip install -r requirements.txt
```

安装依赖。

### 7.3 推荐的开发流程

每次开发前：

```bash
conda activate robotnav
```

运行项目：

```bash
python main.py
```

退出环境：

```bash
conda deactivate
```

### 7.4 可选：创建 environment.yml

也可以创建一个 `environment.yml` 文件：

```yaml
name: robotnav
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy
  - matplotlib
  - pygame
```

别人可以用：

```bash
conda env create -f environment.yml
conda activate robotnav
```

复现环境。

---

## 8. 项目整体架构

项目可以理解成一个从用户输入到机器人运动的流程：

```text
用户交互
   ↓
地图 GridMap
   ↓
路径规划 Planner
   ↓
路径 Path
   ↓
路径跟踪 PathTracker
   ↓
PID 控制器 PIDController
   ↓
机器人模型 Robot
   ↓
渲染器 Renderer
   ↓
屏幕显示
```

更具体地说：

```text
用户画地图
→ 程序得到障碍物矩阵
→ BFS / A* 搜索路径
→ 得到一串路径点
→ PathTracker 选择当前目标点
→ PIDController 计算机器人应该怎么转
→ Robot 根据线速度 v 和角速度 omega 更新位置
→ Renderer 把地图、路径、机器人、误差画出来
```

项目最重要的一句话是：

```text
路径规划决定走哪条路，PID 控制决定怎么稳定地沿着这条路走。
```

---

## 9. 推荐项目目录结构

```text
robotnav/
├── main.py
├── config.py
├── requirements.txt
├── environment.yml
├── README.md
│
├── core/
│   ├── grid_map.py
│   ├── robot.py
│   └── geometry.py
│
├── planning/
│   ├── bfs.py
│   └── astar.py
│
├── control/
│   ├── pid.py
│   └── path_tracker.py
│
├── rendering/
│   ├── renderer.py
│   ├── draw_grid.py
│   ├── draw_robot.py
│   ├── draw_path.py
│   └── draw_ui.py
│
├── experiments/
│   └── compare_algorithms.py
│
├── assets/
│   └── screenshots/
│
└── docs/
    ├── project_intro.md
    ├── algorithm_notes.md
    ├── controller_notes.md
    └── demo_script.md
```

---

## 10. 模块设计

### 10.1 `main.py`

程序入口。

负责：

* 初始化 Pygame；
* 创建地图对象；
* 创建机器人对象；
* 创建 PID 控制器；
* 处理主循环；
* 处理用户输入；
* 调用路径规划算法；
* 调用机器人更新；
* 调用渲染器绘制画面。

`main.py` 不应该写太多具体算法，具体功能应放在对应模块中。

---

### 10.2 `config.py`

存放全局参数。

例如：

```python
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

GRID_ROWS = 25
GRID_COLS = 30
CELL_SIZE = 24

FPS = 60

ROBOT_MAX_SPEED = 80.0
ROBOT_MAX_OMEGA = 3.0

PID_KP = 4.0
PID_KI = 0.0
PID_KD = 0.8
```

---

### 10.3 `core/grid_map.py`

负责地图数据结构。

地图可以用二维数组表示：

```python
grid[row][col]
```

每个格子的状态可以是：

```text
0：空地
1：障碍物
```

需要提供的功能：

```text
判断某个格子是否在地图范围内
判断某个格子是否是障碍物
设置障碍物
删除障碍物
清空地图
获取某个格子的邻居
grid 坐标转 world/screen 坐标
world/screen 坐标转 grid 坐标
```

---

### 10.4 `planning/bfs.py`

负责 BFS 算法。

输入：

```text
grid_map
start
goal
```

输出：

```text
visited_order：搜索访问顺序
path：最终路径
```

BFS 需要使用队列，并记录 parent，以便从终点回溯出完整路径。

---

### 10.5 `planning/astar.py`

负责 A* 算法。

输入：

```text
grid_map
start
goal
```

输出：

```text
visited_order
path
metrics
```

metrics 可以包括：

```text
visited_count
path_length
runtime
```

A* 需要使用优先队列。Python 中可以使用标准库：

```python
heapq
```

---

### 10.6 `core/robot.py`

负责机器人模型。

机器人状态包括：

```text
x
y
theta
v
omega
```

含义：

```text
x, y：机器人位置
theta：机器人朝向角
v：线速度
omega：角速度
```

机器人运动更新公式：

```text
x = x + v * cos(theta) * dt
y = y + v * sin(theta) * dt
theta = theta + omega * dt
```

这个模块只负责机器人状态和运动，不负责绘图。

---

### 10.7 `control/pid.py`

负责 PID 控制器。

建议实现一个通用类：

```python
class PIDController:
    def __init__(self, kp, ki, kd, output_limit=None):
        ...

    def reset(self):
        ...

    def update(self, error, dt):
        ...
```

输入：

```text
error
dt
```

输出：

```text
control_output
```

在本项目中，control output 主要是机器人角速度：

```text
omega
```

---

### 10.8 `control/path_tracker.py`

负责路径跟踪。

A* 输出的是一整条路径，但机器人每一刻只需要跟踪其中一个目标点。

PathTracker 的任务：

```text
保存路径点列表
记录当前目标点编号
判断机器人是否到达当前目标点
如果到达，就切换到下一个目标点
如果全部到达，就停止
```

输出：

```text
当前目标 waypoint
```

---

### 10.9 `core/geometry.py`

负责几何计算。

可以包括：

```python
distance(p1, p2)
normalize_angle(angle)
angle_to_target(position, target)
grid_to_world(row, col)
world_to_grid(x, y)
```

其中 `normalize_angle` 很重要。

角度误差应控制在：

```text
[-pi, pi]
```

否则机器人可能会绕远路转一圈。

---

### 10.10 `rendering/renderer.py`

负责整体绘制流程。

每一帧绘制顺序建议为：

```text
1. 清空屏幕
2. 绘制地图
3. 绘制访问节点
4. 绘制最终路径
5. 绘制机器人轨迹
6. 绘制机器人
7. 绘制方向箭头
8. 绘制右侧信息面板
9. 更新屏幕
```

---

### 10.11 `rendering/draw_ui.py`

负责右侧信息面板。

建议显示：

```text
当前模式
当前算法
访问节点数
路径长度
运行时间

机器人位置
机器人朝向
当前目标点
距离误差
角度误差

PID 参数
Kp
Ki
Kd
线速度 v
角速度 omega
```

---

## 11. 关键类设计

### 11.1 GridMap

```python
class GridMap:
    def __init__(self, rows, cols, cell_size):
        ...

    def set_obstacle(self, row, col):
        ...

    def remove_obstacle(self, row, col):
        ...

    def is_obstacle(self, row, col):
        ...

    def in_bounds(self, row, col):
        ...

    def neighbors(self, row, col):
        ...

    def grid_to_world(self, row, col):
        ...

    def world_to_grid(self, x, y):
        ...
```

---

### 11.2 Robot

```python
class Robot:
    def __init__(self, x, y, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta
        self.v = 0.0
        self.omega = 0.0

    def update(self, v, omega, dt):
        ...
```

---

### 11.3 PIDController

```python
class PIDController:
    def __init__(self, kp, ki, kd, output_limit=None):
        ...

    def reset(self):
        ...

    def update(self, error, dt):
        ...
```

---

### 11.4 PathTracker

```python
class PathTracker:
    def __init__(self, path, waypoint_threshold):
        ...

    def current_target(self):
        ...

    def update(self, robot_position):
        ...
```

---

## 12. 控制逻辑

每一帧中，机器人控制流程大致如下：

```text
1. 获取机器人当前位置
2. 从 PathTracker 获取当前目标 waypoint
3. 计算机器人到目标点的距离
4. 计算机器人应该朝向的角度
5. 计算当前朝向和目标朝向之间的角度误差
6. 将角度误差输入 PID
7. PID 输出角速度 omega
8. 根据距离误差计算线速度 v
9. 更新机器人状态
10. 绘制结果
```

伪代码：

```python
target = path_tracker.current_target()

if target is not None:
    dx = target.x - robot.x
    dy = target.y - robot.y

    distance_error = sqrt(dx * dx + dy * dy)
    target_theta = atan2(dy, dx)

    angle_error = normalize_angle(target_theta - robot.theta)

    omega = heading_pid.update(angle_error, dt)
    v = min(max_speed, distance_gain * distance_error)

    if abs(angle_error) > large_angle_threshold:
        v *= 0.3

    robot.update(v, omega, dt)

    path_tracker.update(robot.position)
```

---

## 13. PID 参数建议

初始参数建议：

```text
Kp = 4.0
Ki = 0.0
Kd = 0.8
```

一开始可以先不使用积分项，即：

```text
Ki = 0.0
```

这样更容易观察 P 和 D 的效果。

可以支持按键调节：

```text
Q / A：增大 / 减小 Kp
W / S：增大 / 减小 Ki
E / D：增大 / 减小 Kd
```

观察现象：

```text
Kp 太小：机器人转向很慢
Kp 太大：机器人容易左右摆动
Kd 增大：机器人运动更稳定
Ki 增大：可以消除长期偏差，但可能导致过冲
```

---

## 14. 界面设计

窗口建议分成两部分：

```text
左侧：地图与机器人动画
右侧：信息面板
```

左侧显示：

```text
网格地图
障碍物
起点
终点
搜索访问节点
最终路径
机器人
机器人轨迹
当前目标点
方向箭头
```

右侧显示：

```text
Algorithm:
BFS / A*

Planning:
visited nodes
path length
runtime

Robot:
x, y
theta
target waypoint
distance error
angle error

PID:
Kp, Ki, Kd
v
omega
```

---

## 15. 8 周执行计划

总周期：8 周。
每周投入：1 天。
每周目标：完成一个可运行功能，并写一点说明。

---

### Week 1：环境配置与网格地图

目标：

* 安装 Miniconda；
* 创建 `robotnav` 环境；
* 安装依赖；
* 创建项目结构；
* 打开 Pygame 窗口；
* 绘制二维网格；
* 实现基础坐标转换。

完成标准：

```text
运行 python main.py 后，可以看到一个二维网格地图。
```

需要理解：

```text
什么是 Conda 环境？
为什么要管理项目依赖？
什么是网格地图？
什么是二维数组？
屏幕坐标和地图坐标有什么区别？
```

---

### Week 2：地图编辑器

目标：

* 鼠标绘制障碍物；
* 鼠标删除障碍物；
* 设置起点；
* 设置终点；
* 清空地图。

完成标准：

```text
用户可以自己画出一张障碍物地图，并设置起点和终点。
```

需要理解：

```text
地图如何用数组保存？
鼠标点击如何转换成地图格子？
地图状态如何更新？
```

---

### Week 3：BFS 路径搜索

目标：

* 实现 BFS；
* 显示访问过的节点；
* 显示最终路径；
* 处理无路径情况。

完成标准：

```text
按下运行键后，BFS 可以找到从起点到终点的路径。
```

需要理解：

```text
为什么 BFS 使用队列？
为什么 BFS 可以找到无权图最短路径？
parent 是如何帮助回溯路径的？
```

---

### Week 4：A* 路径搜索与指标统计

目标：

* 实现 A*；
* 使用曼哈顿距离作为启发式函数；
* 统计访问节点数；
* 统计路径长度；
* 统计运行时间；
* 对比 BFS 和 A*。

完成标准：

```text
用户可以选择 BFS 或 A*，并看到两者搜索过程和指标差异。
```

需要理解：

```text
什么是启发式函数？
A* 为什么通常比 BFS 搜索更少节点？
f = g + h 分别代表什么？
优先队列在 A* 中起什么作用？
```

---

### Week 5：机器人模型与基础运动

目标：

* 定义机器人状态 `x, y, theta`；
* 用三角形绘制机器人；
* 实现机器人基础运动；
* 让机器人可以朝一个目标点移动。

完成标准：

```text
屏幕上出现一个有朝向的三角形机器人，并且可以朝目标点移动。
```

需要理解：

```text
机器人状态是什么？
为什么机器人需要朝向 theta？
线速度 v 和角速度 omega 是什么？
机器人为什么不能直接瞬移到目标点？
```

---

### Week 6：PID 朝向控制器

目标：

* 实现 PIDController；
* 计算机器人朝向误差；
* 用 PID 输出角速度 omega；
* 显示 angle error、omega、Kp、Ki、Kd。

完成标准：

```text
机器人可以通过 PID 控制朝向当前目标点。
```

需要理解：

```text
什么是误差？
什么是反馈控制？
P、I、D 分别在做什么？
为什么 Kp 太大会震荡？
为什么 Kd 可以抑制震荡？
```

---

### Week 7：路径跟踪与完整导航

目标：

* 将 A* 路径转换成 waypoints；
* 实现 PathTracker；
* 机器人逐点跟踪路径；
* 到达当前点后切换到下一个点；
* 支持 PID 参数调整；
* 显示机器人轨迹。

完成标准：

```text
画地图 → A* 规划路径 → PID 控制机器人沿路径运动到终点。
```

需要理解：

```text
路径规划和路径跟踪有什么区别？
为什么机器人不是直接瞬移到终点？
为什么需要一个一个 waypoint 跟踪？
PID 参数变化会如何影响机器人轨迹？
```

---

### Week 8：整理与展示

目标：

* 清理代码；
* 完善 README；
* 添加截图；
* 录制 1–2 分钟 demo；
* 写项目介绍；
* 写算法说明；
* 写 PID 控制说明；
* 整理项目结构。

完成标准：

```text
项目可以作为 GitHub 项目展示。
```

最终材料：

```text
README
运行说明
项目截图
演示视频
算法说明
PID 控制说明
项目结构说明
```

---

## 16. README 建议结构

```text
# RobotNav

## 1. Project Overview
介绍项目目标和最终效果。

## 2. Features
列出地图编辑、路径规划、PID 控制、可视化等功能。

## 3. Environment Setup
说明 Miniconda 环境创建和依赖安装方式。

## 4. Usage
说明如何运行和操作。

## 5. Path Planning
解释 BFS 和 A*。

## 6. PID-based Navigation Control
解释机器人模型、waypoint tracking 和 PID heading controller。

## 7. Demo
放截图和视频链接。

## 8. Project Structure
说明代码目录。

## 9. What I Learned
总结学到的数据结构、算法、数学和控制知识。

## 10. Future Work
写后续可以扩展的方向。
```

---

## 17. AI Agent 使用建议

不要让 AI Agent 一次性生成完整项目。

更好的方式是每次只问一个小任务。

### 17.1 任务拆解类 Prompt

```text
我正在做一个 Python Pygame 项目 RobotNav。
本周目标是实现网格地图编辑器。
请帮我把任务拆成 5 个适合初学者完成的小步骤。
每一步都要说明输入、输出和测试方式。
```

### 17.2 概念解释类 Prompt

```text
我不太理解 A* 中的 f = g + h。
请用二维网格地图的例子解释 g、h、f 分别是什么意思。
然后给我一个 5x5 地图上的手算例子。
```

```text
我不太理解为什么路径规划之后还需要 PID 控制。
请用“小车沿路径移动”的例子解释 planner、tracker、controller 的区别。
```

```text
我第一次接触 PID。
请用机器人转向目标点的例子解释 P、I、D 三项分别做什么。
不要直接给复杂公式，先讲直觉，再给公式。
```

### 17.3 代码实现类 Prompt

```text
请只帮我实现 planning/bfs.py。
输入是 grid_map、start、goal。
输出是 visited_order 和 path。
不要修改其他文件。
请在代码后解释 BFS 为什么需要队列。
```

```text
请只帮我实现 control/pid.py 中的 PIDController 类。
要求包含 kp、ki、kd、integral、prev_error 和 output_limit。
请给出一个简单测试例子。
```

### 17.4 Debug 类 Prompt

```text
下面是我的 PathTracker 代码。
机器人到达 waypoint 后没有切换到下一个点。
请帮我找 bug。
请只指出必要修改，不要重构整个项目。
```

### 17.5 README 类 Prompt

```text
请根据我当前实现的功能，帮我写 README 中的 Path Planning 部分。
要求解释 BFS 和 A* 的区别，适合放在 GitHub 项目主页。
```

---

## 18. 每周复盘问题

每周结束后，回答以下问题：

```text
1. 本周实现了什么功能？
2. 这个功能对应哪个计算机、数学或控制概念？
3. 我遇到了什么 bug？
4. 我是怎么解决的？
5. 如果别人问这个功能，我应该怎么解释？
```

项目不是只要能运行，还要能讲清楚。

---

## 19. 项目成功标准

这个项目成功的标准不是功能很多，而是能讲清楚：

1. 地图为什么可以用二维数组表示；
2. BFS 为什么用队列；
3. A* 为什么用优先队列；
4. A* 中 `f = g + h` 的含义；
5. 路径规划和路径跟踪有什么区别；
6. 为什么机器人需要控制器；
7. PID 中 P、I、D 分别起什么作用；
8. PID 参数变化如何影响机器人轨迹；
9. Python 项目如何组织模块；
10. 如何使用 Miniconda 管理项目环境。

---

## 20. 最终项目闭环

项目最终应形成以下闭环：

```text
用户绘制地图
→ BFS / A* 规划路径
→ 机器人选择当前 waypoint
→ PID 控制朝向
→ 机器人沿路径运动
→ 界面实时显示搜索、路径、轨迹和控制信息
```

最重要的一句话：

```text
路径规划决定机器人应该走哪条路，PID 控制器决定机器人如何稳定地沿着这条路走。
```
