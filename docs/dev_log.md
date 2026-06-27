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

## Week 2 - 2026-06-27

### 本周目标

Week 2 的重点有两个：

1. 项目模块化：把 Week 1 的单文件原型拆成更清晰的功能模块。
2. 交互 UI 界面：在 Pygame 窗口中增加右侧控制面板，让用户可以通过按钮操作项目。

### 模块化设计

当前采用的项目结构：

```text
robot_path_planning/
├── __init__.py
├── config.py
├── main.py
├── core/
│   ├── __init__.py
│   ├── app_state.py
│   └── grid_map.py
├── planning/
│   ├── __init__.py
│   ├── astar.py
│   └── bfs.py
├── rendering/
│   ├── __init__.py
│   └── renderer.py
└── ui/
    ├── __init__.py
    └── panel.py
```

各模块职责：

```text
config.py：
    保存窗口尺寸、网格尺寸、颜色、FPS 等配置。

core/grid_map.py：
    保存地图数据，包括障碍物、起点、终点。
    负责判断格子是否合法、是否可通行、获取上下左右邻居。

core/app_state.py：
    保存应用交互状态，包括当前编辑模式、路径、访问节点和状态文字。

planning/bfs.py：
    保存 BFS 路径规划算法。
    输入 GridMap、start、goal，输出 SearchResult。

planning/astar.py：
    保存 A* 路径规划算法。
    使用曼哈顿距离作为启发函数。

rendering/renderer.py：
    负责绘制启动主界面、网格、障碍物、起点、终点、路径、访问过的节点、机器人和轨迹。

ui/panel.py：
    负责绘制启动主界面、右侧 UI 面板、按钮、算法选择、状态信息和统计信息。

ui/fonts.py：
    负责跨平台字体匹配。
    优先使用 macOS、Windows、Linux 常见清晰字体，找不到时回退到 Pygame 默认字体。

main.py：
    负责程序入口、Pygame 初始化、事件分发、调用算法、记录统计、更新机器人模拟和调用渲染。
```

这样拆分后，后续扩展会更清楚：

```text
新增 A*：
    添加 planning/astar.py
    在 main.py 或后续 planner registry 中调用。

新增机器人：
    添加 core/robot.py
    添加 rendering/draw_robot.py 或扩展 renderer.py。

新增 PID：
    添加 control/pid.py
    添加 control/path_tracker.py。

新增算法统计：
    扩展 SearchResult，加入 visited_count、path_length、elapsed_ms。
```

### UI 界面设计

本周先使用 Pygame 内置绘制能力实现右侧交互面板，不引入额外 GUI 框架。

原因：

- 当前项目已经使用 Pygame，继续使用同一技术栈更容易理解。
- 右侧面板足够支持按钮、状态、图例和后续算法选择。
- 后续如果界面需求变复杂，再考虑单独 GUI 框架也不迟。

### UI 清晰度优化

运行界面文字曾出现偏糊、偏挤的问题。当前采用的解决方案：

```text
1. 右侧面板从 260px 加宽到 320px。
2. 窗口调整为 1160 x 780，降低被桌面菜单栏或 Dock 遮挡的概率，同时给底部信息区留出空间。
3. 地图区为 840 x 780，刚好对应 28 列 x 26 行的 30px 网格。
4. 新增 ui/fonts.py，使用跨平台字体候选列表。
5. 运行界面字体调整为更紧凑但清晰的字号。
6. 编辑模式和寻路算法改为浮层下拉选择，减少按钮数量。
7. 主界面删去大段说明，只保留简短过渡引导。
8. 状态消息最多显示两行，超出后截断，避免遮挡底部信息栏。
```

字体候选优先级：

```text
PingFang SC：macOS 中文
Microsoft YaHei / SimHei：Windows 中文
Noto Sans CJK / WenQuanYi Micro Hei：Linux 中文
Arial / Helvetica / DejaVu Sans：通用回退
```

这样做的好处是：不需要把字体文件放进项目，也能在 macOS、Windows、Linux 上尽量使用本机清晰字体。

当前 UI 包含：

```text
Start Lab [Enter]：从启动主界面进入运行界面
Edit Mode：下拉选择 Obstacle / Start / Goal
Path Planner：下拉选择 BFS / A*
Run Planner [Space]：执行当前算法
Start Robot [S]：让机器人沿当前路径移动
Random Map [R]：随机生成障碍物、起点和终点
Clear [C]：清空地图和搜索结果
Home [H]：返回启动主界面
```

状态区域显示：

```text
当前模式
当前算法
障碍物数量
起点和终点状态
算法运行时间
访问节点数
路径长度
机器人模拟状态
状态消息
```

颜色图例显示：

```text
Start：绿色
Goal：红色
Path：蓝色
Visited：浅蓝色
Wall：深色
```

### 行为变化

相比 Week 1，本周新增或调整了这些行为：

- 修改障碍物、起点或终点后，会自动清空旧路径和访问节点。
- 障碍物模式支持按住鼠标拖动连续编辑：
  - 从空白格开始拖动，会连续添加障碍物。
  - 从障碍物开始拖动，会连续擦除障碍物。
- 按 `R` 或点击 `Random` 可以随机生成障碍物、起点和终点。
- 按 `Tab` 或点击算法按钮可以切换 BFS / A*。
- 按 `Space` 或点击 `Run Planner` 会执行当前选择的算法。
- 搜索完成后会记录运行时间、访问节点数和路径长度。
- 按 `S` 或点击 `Start Robot` 可以让机器人沿规划路径移动。
- 按 `C` 或点击 `Clear` 可以清空地图。
- 如果没有设置起点和终点就运行搜索，会显示提示。
- 如果 BFS 找不到路径，会显示 `No path found`。
- BFS 运行后会显示访问过的节点，为后续搜索动画做准备。

### 当前验证

已运行：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

验证结果：

```text
所有 Python 模块编译通过。
```

第一次直接运行 `python3 -m compileall robot_path_planning` 时，macOS Python 尝试把缓存写入 `~/Library/Caches`，受当前沙箱限制失败。后来通过 `PYTHONPYCACHEPREFIX=.pycache` 把缓存写入项目目录，检查通过。已将 `.pycache/` 加入 `.gitignore`。

### Week 2 总结

本周完成了 RobotNav 从单文件原型到模块化交互平台的升级：

```text
单文件 main.py
→ core / planning / rendering / ui 分层
→ BFS 与 A* 双算法
→ 右侧运行控制面板
→ 随机地图和拖动编辑
→ 运行时间、访问节点数、路径长度统计
→ 基础机器人路径跟随动画
```

当前项目已经适合进入 Week 3：继续增强搜索过程动画、算法对比和机器人控制。

### Week 3 建议

1. 把 BFS 访问节点从一次性显示改成逐帧动画。
2. 把 A* 访问节点也做成逐帧动画。
3. 增加算法对比历史表，记录多次 BFS / A* 运行结果。
4. 可选：增加“生成可通行随机地图”，确保随机地图至少存在一条路径。
5. 把机器人圆点升级为有朝向的三角形模型。
6. 加入 PID heading controller，让机器人转向更接近真实控制。
