# Development Log

本文件记录 RobotNav 项目的开发过程、关键决策、遇到的问题和下一步计划。

`CHANGELOG.md` 主要记录每周完成了什么；本文件更关注为什么这样做、过程中学到了什么，以及后续如何继续。

## Week 1 - 2026-06-27

### 本周目标

完成项目第一阶段：从零开始搭建一个可运行、可交互的 Python + Pygame 2D 路径规划原型。

阶段目标不是一次性做完整机器人系统，而是先把最小闭环跑通：

```text
窗口 -> 网格地图 -> 鼠标交互 -> 起点终点 -> BFS 路径 -> 路径显示
```

### 技术路线

本项目选择：

```text
Python + Pygame
```

选择原因：

- Python 语法相对简单，适合初学者先理解路径规划和仿真逻辑。
- Pygame 可以快速创建 2D 窗口、绘制网格、处理鼠标键盘事件。
- 后续可以比较自然地加入 BFS、A*、机器人运动和 PID 控制。
- 第一阶段可以先避免复杂前端框架或大型机器人仿真工具带来的学习负担。

### 完成内容

本周完成了以下功能：

- 创建 Pygame 窗口。
- 绘制 2D 网格地图。
- 支持鼠标点击格子。
- 支持障碍物编辑：
  - 按 `1` 进入障碍物模式。
  - 点击空白格添加黑色障碍物。
  - 再次点击黑色格取消障碍物。
- 支持起点设置：
  - 按 `2` 进入起点模式。
  - 点击格子设置绿色起点。
  - 起点只有一个，后一次设置会覆盖前一次。
- 支持终点设置：
  - 按 `3` 进入终点模式。
  - 点击格子设置红色终点。
  - 终点只有一个，后一次设置会覆盖前一次。
- 支持 BFS 路径规划：
  - 按 `Space` 执行 BFS。
  - 如果存在路径，使用蓝色格子显示最终路径。

### 当前代码入口

当前主程序为：

```text
robot_path_planning/main.py
```

第一阶段为了降低理解难度，暂时采用单文件结构。后续功能变多后，再逐步拆分为地图、规划算法、渲染、控制等模块。

### 关键概念记录

#### 像素坐标到网格坐标

鼠标点击得到的是像素坐标：

```python
mouse_x, mouse_y = pygame.mouse.get_pos()
```

项目需要的是网格坐标，所以用整除转换：

```python
col = mouse_x // CELL_SIZE
row = mouse_y // CELL_SIZE
cell = (row, col)
```

含义：

```text
x 对应列 col
y 对应行 row
```

#### 绘制格子

使用 `pygame.draw.rect()` 绘制一个网格格子：

```python
pygame.draw.rect(screen, color, rect)
```

其中 `rect` 描述矩形的位置和大小，`color` 描述颜色，`screen` 是 Pygame 窗口画布。

#### BFS 广度优先搜索

BFS 的直观理解是从起点开始一圈一圈向外扩散，直到找到终点。

在当前项目中，每次只允许向上下左右移动一格，每一步代价相同，因此 BFS 可以找到最短路径之一。

关键数据结构：

```text
queue：保存待访问格子的队列
visited：保存已经访问过的格子
parent：记录每个格子从哪个上一个格子走来，用于最终还原路径
```

### 遇到的问题

#### 文件名输入错误

运行时曾出现：

```text
[Errno 2] No such file or directory
```

原因是把 `main.py` 打成了 `mian.py`。

记录这个问题是为了提醒后续排查运行错误时，先检查：

```text
当前终端目录是否正确
文件名是否输入正确
文件是否真的存在
```

#### 终端目录问题

运行：

```bash
python3 main.py
```

时，终端必须位于 `main.py` 所在目录，或者从仓库根目录使用完整路径：

```bash
python3 robot_path_planning/main.py
```

### 项目管理决策

本周开始建立 Git 版本管理。

当前策略：

```text
main 分支：保持可运行版本
每周结束：至少一次 commit
每个阶段完成：打 tag
```

Week 1 已创建：

```text
commit: 6fd8331 Week 1: initialize project structure and BFS grid planner
tag: week-1-bfs-grid-planner
```

同时补充了：

```text
README.md：当前项目说明和运行方式
CHANGELOG.md：每周成果记录
.gitignore：忽略缓存、环境和系统临时文件
requirements.txt：pip 依赖
environment.yml：Conda 环境
project.md：完整项目规划
```

### 当前项目状态

项目已经具备一个简单可用的 2D 路径规划原型：

```text
可画地图
可设置起点终点
可放置障碍物
可运行 BFS
可显示最终路径
```

这意味着项目已经完成最小功能闭环，后续可以在这个基础上逐步增强交互体验、算法能力和仿真能力。

### Week 2 建议目标

建议 Week 2 先完善当前原型，而不是马上跳到复杂算法。

优先级建议：

1. 增加 `C` 键清空地图、起点、终点和路径。
2. 增加找不到路径时的提示。
3. 当用户修改障碍物、起点或终点时，自动清空旧路径。
4. 可选：在窗口标题中显示当前状态，例如 `Path found` 或 `No path found`。
5. 为后续 BFS 搜索过程可视化做准备。

### 下次继续开发时的推荐开场

如果在新对话窗口中继续项目，可以这样开始：

```text
开始 Week 2，继续 RobotNav 项目。
请先阅读 README.md、CHANGELOG.md、docs/dev_log.md、project.md 和 robot_path_planning/main.py。
然后总结当前项目状态，并带我小步推进 Week 2 任务。
```
