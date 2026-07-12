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

## Week 3 - 2026-07-04

### 本周目标

Week 3 的重点是把 RobotNav 从“运行一次、直接看到最终结果”的路径规划演示，升级为更适合观察算法过程和做算法对比的学习工具。

本周围绕三条主线推进：

```text
搜索过程动画
→ 多算法扩展
→ 最近运行记录与地图复现
```

同时继续优化右侧 UI，让新增信息不会挤在固定高度里。

### 搜索动画

Week 2 中，BFS 只是在搜索结束后一次性显示所有访问节点。Week 3 增加了 `visited_order`，让每个算法都能记录节点被访问的先后顺序：

```text
visited：
    set[Cell]，用于快速判断某个节点是否被访问过。

visited_order：
    list[Cell]，用于按顺序播放搜索动画。
```

当前搜索流程变为：

```text
1. 用户点击 Run Planner 或按 Space。
2. main.py 调用当前选择的 planner。
3. planner 一次性完成搜索，并返回 path、visited、visited_order。
4. AppState.search_animation 保存 visited_order 和最终结果。
5. 主循环每一帧调用 _update_search_animation()。
6. 按 SEARCH_ANIMATION_CELLS_PER_SECOND 逐个 reveal 访问节点。
7. 动画结束后显示最终 path，并把本次运行写入 Recent Runs。
```

这样实现的好处是：算法代码仍然保持简单，不需要先改成 generator；但 UI 已经能逐帧展示 BFS、A*、DFS、Dijkstra 和 Greedy 的搜索差异。

相关代码：

```text
robot_path_planning/planning/bfs.py
robot_path_planning/planning/astar.py
robot_path_planning/planning/dfs.py
robot_path_planning/planning/dijkstra.py
robot_path_planning/planning/greedy.py
robot_path_planning/core/app_state.py
robot_path_planning/main.py
```

### 新增算法

本周在 BFS 和 A* 基础上新增三个算法：

```text
DFS：
    使用 stack 深度优先探索。
    不保证最短路径，但适合观察“先往一个方向走到底”的搜索风格。

Dijkstra：
    使用优先队列，根据起点到当前节点的累计距离扩展。
    在当前每一步代价都为 1 的网格里，路径长度通常与 BFS 一致。

Greedy Best-First Search：
    使用曼哈顿距离作为优先级。
    更激进地靠近终点，访问节点可能更少，但不保证最短路径。
```

算法注册集中在 `main.py` 的 `PLANNERS` 字典中：

```text
BFS
A*
DFS
Dijkstra
Greedy
```

右侧 `Path Planner` 下拉框和 `Tab` 快捷键都会基于这组算法切换。

### 运行历史与地图编号

Week 3 增加了 Recent Runs。每次搜索动画结束后，程序会记录一条运行历史：

```text
地图编号 Mi
算法名称
是否找到路径
运行时间
访问节点数
路径长度
障碍物快照
起点和终点
visited 和 path
```

用户点击某条历史记录时，左侧地图会恢复到当时的障碍物、起点、终点、访问区域和最终路径。

地图编号不是每次地图编辑就变化，而是“运行记录产生时”才确定。当前使用地图指纹：

```text
signature = (sorted(obstacles), start, goal)
```

如果这张地图之前出现过，就复用原来的 `Mi`；如果是第一次出现，就分配新的编号。

这样可以避免“每次小改地图就跳号”，也能让同一张地图上的不同算法运行结果自然归到同一个 `Mi` 下。

### UI 调整

本周右侧面板做了几项调整：

```text
1. 删除运行界面顶部的 RobotNav / Run interface 标题，节省垂直空间。
2. 使用更接近 macOS 的浅色背景、系统蓝强调色和柔和边框。
3. 字体尺寸略微收紧，并优先匹配系统清晰字体。
4. 右侧面板改为可滚动内容区。
5. Recent Runs 每条记录使用小横条样式。
6. 点击历史记录可以复现当时结果。
```

滚动实现思路：

```text
1. 先创建一个比窗口更高的 content Surface。
2. 把右侧面板所有内容画到 content Surface 上。
3. 根据 state.panel_scroll_y 截取其中一段 blit 到真实屏幕。
4. 鼠标滚轮只在右侧面板区域内生效。
5. 根据 content 高度和窗口高度绘制滚动条。
```

### 本周暂缓的功能

“保证随机地图至少有一条路径”本周先暂缓，没有替换现有 `Random Map`。

原因是当前普通随机地图也有学习价值：

```text
有路径：
    可以观察不同算法如何搜索和找到路径。

无路径：
    可以观察算法如何扩散、如何确认不可达。
```

后续更合适的做法是新增一个独立按钮，例如 `Solvable Map`，通过重复生成随机地图并用 BFS 检查可达性来保证至少有路，同时保留当前可能无路的 `Random Map`。

### 当前验证

已完成以下验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
所有 Python 模块编译通过。
```

并完成 planner smoke test：

```text
BFS：找到路径，路径长度与访问节点正常
A*：找到路径，访问节点少于 BFS
DFS：找到路径，但路径不一定最短
Dijkstra：找到路径，路径长度与 BFS 一致
Greedy：找到路径，访问节点较少但不保证最短
```

地图编号逻辑也已验证：

```text
同一张地图重复运行 → 复用同一个 M 编号
新地图首次运行 → 分配新的 M 编号
回到旧地图运行 → 继续复用旧编号
```

### Week 3 总结

Week 3 完成后，RobotNav 已经从“双算法路径显示工具”升级为“五算法搜索过程可视化工具”：

```text
BFS / A* / DFS / Dijkstra / Greedy
→ visited_order 搜索动画
→ Recent Runs 历史记录
→ M1 / M2 地图编号
→ 点击历史记录复现运行结果
→ 可滚动右侧控制面板
```

当前项目已经适合进入 Week 4：在现有五种算法基础上做更系统的对比，并开始推进机器人模型和 PID 控制。

### Week 4 建议

1. 设计同一地图上的算法对比视图或对比流程。
2. 可选新增 `Solvable Map`，但保留普通 `Random Map`。
3. 把机器人圆点升级为有朝向的三角形模型。
4. 加入 PID heading controller。
5. 增加暂停、继续、重置机器人模拟。
6. 整理项目截图和演示材料。

## Week 4 - 2026-07-11

### 本周阶段目标

Week 4 开始把 RobotNav 从“离散网格路径动画”推进到“连续空间刚体仿真 + 路径跟踪 + 控制”的方向。

核心变化是：

```text
规划算法仍然在 grid cell 上运行
→ 机器人运动改为连续 world position
→ Pymunk 负责刚体位置、速度、角度和碰撞积分
→ PathTracker 把离散 path 转成连续 waypoint
→ Controller 根据 waypoint 偏差输出 force / torque
→ PID heading controller 控制机器人朝向
```

这意味着机器人任意时刻的位置不再必须落在整数格子上，而是可以是类似：

```text
(x, y) = (3.42, 8.17)
```

这更接近真实机器人运动，也带来了新的控制和仿真问题。

### 阶段推进记录

#### 阶段 1：统一连续坐标系统

新增：

```text
robot_path_planning/core/coordinates.py
```

用于统一三类坐标：

```text
grid cell：离散格子坐标，用于地图编辑和路径规划，例如 (row, col)
world position：连续世界坐标，用于机器人真实运动，例如 (x, y)
screen pixel：屏幕像素坐标，用于 Pygame 绘制
```

关键函数：

```text
cell_center_to_world(cell)
world_to_screen(position)
cell_to_screen_rect(cell)
distance(a, b)
```

这样后续物理引擎、路径跟踪和控制器都可以基于连续坐标工作。

#### 阶段 2：引入 Pymunk 最小物理世界

新增：

```text
robot_path_planning/physics/
robot_path_planning/physics/physics_world.py
```

当前 `PhysicsWorld` 负责：

```text
创建 Pymunk Space
创建圆形动态机器人刚体
把障碍物 cell 转成静态方块刚体
接收 force / torque
执行 step(dt)
返回机器人连续状态 position / velocity / angle / angular_velocity
```

依赖文件也加入了：

```text
pymunk
```

初始 smoke test 验证了：

```text
创建 PhysicsWorld
→ 创建动态机器人
→ 施加外力
→ step 多帧
→ 机器人连续位置发生变化
```

#### 阶段 3：PathTracker 连续 waypoint 跟踪

新增：

```text
robot_path_planning/control/path_tracker.py
```

`PathTracker` 负责把规划算法输出的离散路径：

```text
[(row, col), (row, col), ...]
```

转换成连续 waypoint：

```text
[(x, y), (x, y), ...]
```

并维护当前应该追踪哪个 waypoint。

重要设计：

```text
终点仍然由 goal cell 表示
机器人中心进入 goal cell 内部时，判定任务成功
```

这比“必须到达终点中心”更合理，因为真实机器人只要进入目标区域即可。

#### 阶段 4：基础 waypoint force controller

新增：

```text
robot_path_planning/control/waypoint_controller.py
```

`WaypointForceController` 根据机器人当前物理状态和 `TrackingTarget` 输出：

```text
ControlCommand(force, torque)
```

第一版主要做：

```text
朝 waypoint 方向施加驱动力
根据当前速度施加阻尼
```

这样 `main.py` 不再直接计算控制力，而只负责：

```text
读取 PhysicsWorld 状态
→ PathTracker 给出目标 waypoint
→ Controller 输出 force / torque
→ PhysicsWorld 应用控制并 step
```

#### 阶段 5：PID heading controller

新增：

```text
robot_path_planning/control/pid.py
```

`PIDController` 是通用一维 PID 控制器，支持：

```text
Kp / Ki / Kd
输出限幅
积分限幅
reset()
```

当前用于机器人朝向控制：

```text
desired_heading = atan2(target_y - y, target_x - x)
heading_error = desired_heading - robot.angle
torque = PID(heading_error)
```

同时 `RobotState` 增加：

```text
angle
```

渲染器中的机器人朝向线也改为使用真实物理角度，而不是简单根据路径段方向绘制。

### 关键问题记录：机器人在路径上卡死

#### 问题现象

引入 Pymunk、PathTracker 和 PID heading controller 后，用户实际运行程序时发现：

```text
机器人沿规划路径运动时，经常会在路径上卡住，无法继续前进。
```

一开始容易把这个问题误认为是“动画卡顿”或“帧率不稳定”，但实际观察后发现：

```text
机器人不是显示帧率低，而是控制逻辑让机器人卡在某个 waypoint 或拐点附近。
```

也就是说，问题本质不是 UI 渲染，而是连续物理仿真和离散路径跟踪之间的耦合问题。

#### 如何发现

问题来自真实交互运行，而不是 compile check。

编译检查和简单直线 smoke test 都能通过：

```text
compileall：通过
直线路径 smoke test：机器人可以从起点移动到终点
```

但用户在 Pygame 界面中实际运行更复杂路径时，发现机器人会停在路径中间。

随后用专门的折线路径测试复现：

```text
path = [(1,1), (1,2), (1,3), (2,3), (3,3), (4,3)]
```

调试输出显示机器人在 90 度转弯后会冲出路径，之后被控制器反复拉向旧 waypoint 或拐点附近，形成绕圈或卡住。

典型调试现象：

```text
机器人已经越过某个 waypoint
但距离没有进入 waypoint_tolerance
PathTracker 仍然认为旧 waypoint 是当前目标
Controller 继续把机器人拉回旧目标点
机器人带着惯性又冲出去
最终在拐点附近来回拉扯或绕圈
```

#### 根本原因

这个问题来自三个变化叠加：

1. **离散路径变成连续运动后，机器人不一定经过每个 cell center**

   以前的机器人是沿路径点插值运动，必然经过每个格子中心。

   引入物理引擎后，机器人位置由力、速度和积分决定：

   ```text
   position(t + dt) = physics_step(position, velocity, force, torque)
   ```

   因此它可能从 waypoint 附近掠过，但不一定刚好进入很小的容差范围。

2. **PathTracker 第一版只靠距离容差切换 waypoint**

   原逻辑类似：

   ```text
   如果 distance(robot, waypoint) <= tolerance
       切换到下一个 waypoint
   否则
       继续追当前 waypoint
   ```

   当机器人冲过 waypoint，但没有进入 tolerance，就会继续追旧点，导致控制方向反转。

3. **力控制存在惯性和过冲**

   机器人是刚体，有速度和质量，不会像网格点一样瞬间停住。

   旧控制器主要是：

   ```text
   force = direction_to_waypoint * drive_force - velocity * damping
   ```

   这会让机器人像被弹簧拉向目标点。如果 waypoint 很密、转弯很急，就容易在拐点附近过冲。

#### 解决方案

本次修复不是单点修改，而是从 PathTracker、Controller 和 PhysicsWorld 三层一起处理。

##### 1. PathTracker 支持“越过 waypoint 后也推进”

新增记录：

```text
previous_distance_to_target
```

如果机器人距离目标点已经先变小、后变大，并且最近曾经足够接近目标点，就认为它已经越过该 waypoint，可以进入下一个目标。

核心思想：

```text
不仅“进入 tolerance”算到达
“接近后开始远离”也可以算越过 waypoint
```

这样可以避免机器人因为没有精确踩中 cell center 而被旧目标点拉住。

##### 2. Controller 增加 force 限幅

新增参数：

```text
ROBOT_MAX_FORCE
```

控制器输出后会对 force 做向量长度限制：

```text
force = clamp_vector(force, max_force)
```

作用：

```text
避免控制器在偏差较大时给出过大拉力
降低过冲和震荡
```

##### 3. PhysicsWorld 增加速度限幅

新增：

```text
PhysicsWorld.limit_robot_speed(max_speed)
```

配置：

```text
ROBOT_MAX_SPEED_CELLS_PER_SECOND = 2.2
```

作用：

```text
限制机器人最大线速度
避免它在短距离 waypoint 之间冲太远
```

##### 4. Controller 增加 arrival slowdown

新增：

```text
ROBOT_ARRIVAL_SLOWDOWN_RADIUS_CELLS = 1.0
```

机器人越接近 waypoint，前进驱动力越小。

这样可以让机器人在拐点附近先减速，而不是高速冲过拐点。

##### 5. Controller 增加 heading gate

新增：

```text
ROBOT_HEADING_GATE_POWER = 2.0
```

如果机器人当前朝向和目标方向差距较大，则降低前进力，让 PID 有时间先把朝向转过去。

直观理解：

```text
没转向前，少往前冲；
先对准，再加速。
```

这对 90 度转弯尤其重要。

##### 6. PID 参数调得更保守

调整为：

```text
ROBOT_HEADING_PID_KP = 14.0
ROBOT_HEADING_PID_KD = 3.0
ROBOT_MAX_TORQUE = 90.0
```

目标是降低转向过猛导致的震荡。

#### 验证结果

修复后完成了三类验证。

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

直线路径 anti-stuck test：

```text
path = [(1,1), (1,2), (1,3), (1,4), (1,5)]
```

结果：

```text
Straight anti-stuck smoke test passed
```

折线路径 anti-stuck test：

```text
path = [(1,1), (1,2), (1,3), (2,3), (3,3), (4,3)]
```

结果：

```text
Turning anti-stuck smoke test passed
```

这说明机器人至少在直线和 90 度折线两类基础路径上不会再因为 waypoint 跟踪逻辑卡死。

#### 本次收获

这个问题是 RobotNav 从“路径显示项目”升级到“机器人仿真项目”的一个关键分水岭。

主要收获：

1. **离散规划路径不能直接等同于连续可跟踪轨迹**

   BFS / A* 给出的路径是一串 cell，而真实机器人有半径、速度、惯性和朝向。

   即使路径在网格上可行，机器人也可能因为转弯半径、速度或碰撞边界而跟踪失败。

2. **物理仿真后，控制逻辑必须允许误差**

   机器人不可能每一帧都精确经过 waypoint 中心。

   PathTracker 必须支持：

   ```text
   接近 waypoint
   越过 waypoint
   进入目标区域
   ```

   而不能只依赖“距离小于某个阈值”。

3. **PID 不是单独解决所有问题的魔法**

   PID 可以控制朝向，但如果前进力太大、速度过高或 waypoint 切换逻辑不合理，机器人仍然会震荡或卡死。

   控制系统需要和路径跟踪、速度限制、力限制一起设计。

4. **smoke test 需要覆盖折线路径**

   直线路径测试太容易通过，无法发现转弯处的问题。

   后续所有机器人运动相关改动，至少应测试：

   ```text
   直线路径
   90 度折线路径
   靠近障碍物的窄通道路径
   ```

5. **下一步需要考虑机器人半径和路径安全裕度**

   当前规划算法仍然把机器人当成一个点。

   但物理世界里机器人有半径：

   ```text
   ROBOT_RADIUS_CELLS = 0.35
   ```

   所以后续如果路径贴着障碍物边缘，机器人仍可能碰撞或卡住。

   下一阶段可以考虑：

   ```text
   obstacle inflation
   clearance-aware planning
   smoothing / lookahead tracking
   ```

这次问题说明，RobotNav 已经进入真正的“机器人导航仿真”难点：不只是找到路，还要让有物理属性的机器人稳定地沿着路走。

### 阶段 6：仿真稳定性改进

在修复 waypoint 卡死问题后，继续推进阶段 6 的稳定性工作。本阶段的目标不是新增规划算法，而是让连续刚体仿真更可靠、更可重复。

#### 固定物理时间步长

之前 `_update_robot()` 每帧直接使用当前帧的 `dt` 调用：

```text
physics_world.step(dt)
```

这种方式的问题是，Pygame 主循环的帧间隔可能会波动。如果某一帧较慢，物理引擎会突然收到一个更大的 `dt`，机器人就可能出现更明显的速度跳变、过冲或碰撞不稳定。

因此本阶段新增固定物理时间步：

```text
PHYSICS_TIME_STEP = 1 / 120
MAX_PHYSICS_STEPS_PER_FRAME = 5
```

实现方式：

```text
每帧把真实 dt 累加到 robot.physics_accumulator
只要 accumulator >= PHYSICS_TIME_STEP，就执行一次固定步长物理更新
每帧最多补 MAX_PHYSICS_STEPS_PER_FRAME 次
最后把机器人显示状态从 PhysicsWorld 同步回 AppState
```

这样 Pymunk 的积分输入更稳定：

```text
渲染帧率可以波动
但物理仿真尽量以固定小步长推进
```

相关改动：

```text
robot_path_planning/config.py：
    PHYSICS_TIME_STEP
    MAX_PHYSICS_STEPS_PER_FRAME

robot_path_planning/core/app_state.py：
    RobotState.physics_accumulator

robot_path_planning/main.py：
    _update_robot()
    _step_robot_physics()
    _sync_robot_from_physics()
```

#### 为什么这一步重要

固定 timestep 是游戏和物理仿真中常见的稳定性做法。

对当前项目来说，它可以降低以下问题发生概率：

```text
帧率波动导致机器人突然跳远
物理积分误差放大
机器人高速穿过 waypoint
机器人在拐点处过冲更严重
```

它不能单独解决所有路径跟踪问题，但它为后续控制器调参、碰撞处理和路径平滑提供了更稳定的基础。

#### 当前验证

本阶段完成后重新运行：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

直线路径验证：

```text
path = [(1,1), (1,2), (1,3), (1,4), (1,5)]
Straight fixed-timestep smoke test passed
```

折线路径验证：

```text
path = [(1,1), (1,2), (1,3), (2,3), (3,3), (4,3)]
Turning fixed-timestep smoke test passed
```

这说明固定 timestep 接入后，直线和 90 度折线路径仍然能够完成，不会破坏前面阶段已经修复的 anti-stuck 行为。

#### 下一步方向

阶段 6 后续可以继续完善：

```text
Pause / Resume / Reset 仿真状态
窄通道和靠近障碍物路径测试
考虑机器人半径的 obstacle inflation
更平滑的 lookahead tracking
```

其中最重要的是 obstacle inflation。因为当前 planner 仍把机器人看作点，而物理世界中的机器人有半径；如果路径贴着障碍物边缘，机器人仍可能在真实碰撞体上卡住。

### 阶段 6-B：可靠运动闭环第一步

#### 新发现

用户再次实际运行程序后反馈：

```text
机器人路径卡死问题并没有被修复，实际运行时还是会卡死。
```

这说明上一轮 anti-stuck 修复只能通过直线、90 度折线等简单 smoke test，不能代表真实交互地图中的运动闭环已经可靠。

因此本阶段不再把问题简单归因于 PID 参数，而是重新定义为系统功能不完整：

```text
离散网格路径
→ 连续 waypoint 跟踪
→ 力 / torque 控制
→ Pymunk 刚体积分与碰撞
→ 运行时诊断反馈
```

这几个模块之间还缺少足够稳定的协作。

#### 本阶段目标

阶段 6-B 先不追求一次性实现完整局部避障，而是完成一个更小、更可验证的目标：

```text
让机器人不再死追每一个 cell center
让系统能显示当前追踪目标和卡死诊断信息
为后续真实地图调试提供可观测信号
```

#### 实现内容

##### 1. PathTracker 路径压缩

原先 `PathTracker` 会把规划路径中的每个 cell center 都当作 waypoint。

例如：

```text
[(1,1), (1,2), (1,3), (1,4), (2,4), (3,4), (4,4)]
```

会变成每一格都追踪一次。

这在离散动画中没问题，但在刚体仿真中会导致：

```text
waypoint 太密
机器人不断被短距离目标拉扯
转弯附近更容易过冲和回拉
```

本阶段新增 `_compress_path()`：

```text
保留起点
保留方向变化处的拐点
保留终点
删除同一直线段中的中间 cell center
```

压缩后，上面的路径会变成：

```text
[(1,1), (1,4), (4,4)]
```

机器人追踪的是更长的安全段端点，而不是每个网格中心。

##### 2. 保守处理 lookahead

实现时曾测试过：

```text
ROBOT_LOOKAHEAD_STEPS = 2
```

但小测试马上暴露问题：路径压缩后如果再向前看两步，机器人可能直接跳过拐点，朝终点斜向拉动。

这会带来新风险：

```text
路径本来要求先横向再纵向
lookahead 直接把目标设到终点
机器人可能试图走斜线
在有障碍物时可能穿过不安全区域
```

因此本阶段把默认值收回为：

```text
ROBOT_LOOKAHEAD_STEPS = 1
```

也就是先采用“压缩后的当前安全段端点追踪”，不跨过拐点。

##### 3. RobotState 增加卡死诊断字段

新增运行时诊断状态：

```text
tracking_target_index
tracking_target_distance
stuck_timer
stuck_warnings
last_target_distance
```

这些字段用于记录：

```text
当前正在追踪第几个目标点
距离当前目标还有多远
是否长时间低速且没有接近目标
发生过几次卡死警告
```

##### 4. 主循环增加 stuck diagnostics

在每次物理 step 后，新增 `_update_robot_stuck_diagnostics()`。

判断逻辑是：

```text
如果机器人速度很低
并且距离目标没有明显变小
持续超过 ROBOT_STUCK_TIMEOUT_SECONDS
则记录一次 stuck warning
```

当前参数：

```text
ROBOT_STUCK_SPEED_THRESHOLD_CELLS_PER_SECOND = 0.08
ROBOT_STUCK_PROGRESS_EPSILON_CELLS = 0.02
ROBOT_STUCK_TIMEOUT_SECONDS = 1.5
```

注意：这一阶段只做诊断和状态反馈，不自动强行重置机器人。

原因是如果立刻自动“救援”，反而会掩盖真实问题。当前更需要先知道机器人是：

```text
追错目标
速度过低
碰撞卡住
还是路径本身不适合物理机器人
```

##### 5. UI 面板显示诊断信息

右侧 `Simulation` 区域新增：

```text
Target
Distance
Stuck warnings
```

这样实际运行时可以直接观察：

```text
机器人是否一直卡在同一个 target
距离是否长期不下降
是否已经触发 stuck warning
```

#### 当前验证

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

直线路径仿真：

```text
straight finished seconds=1.78 warnings=0 target=1
```

折线路径仿真：

```text
turn finished seconds=4.12 warnings=0 target=2
```

主循环链路仿真：

```text
planner_case finished seconds=3.15 warnings=0 path_len=8 target=1
```

该测试覆盖：

```text
运行 planner
结束搜索动画
启动物理机器人
执行固定 timestep 仿真
进入目标单元格完成任务
```

#### 当前结论

阶段 6-B 不是宣称“卡死问题彻底解决”，而是完成了可靠运动闭环的第一步：

```text
路径跟踪目标更合理
简单场景保持通过
真实运行时有了可见诊断信号
后续可以根据 Target / Distance / Stuck warnings 判断下一步修复方向
```

#### 下一步建议

如果真实运行仍然卡死，下一阶段应该根据 UI 诊断信息分情况处理：

```text
Target 不变、Distance 不下降、Stuck warnings 增加：
    优先检查是否碰撞卡住，需要局部恢复策略或更强 clearance 规划。

Target 不变、Distance 上下震荡：
    优先检查控制器阻尼、速度限制和目标切换策略。

Target 正常推进，但靠近障碍物卡住：
    优先检查 obstacle inflation、起终点 clearance、通道宽度是否适合机器人半径。

机器人斜向靠近障碍物：
    后续不能简单增加 lookahead，需要做 line-of-sight 安全检查后才能跨 waypoint。
```

阶段 6-C 更适合继续做：

```text
基于碰撞/低速的局部恢复
line-of-sight 安全 lookahead
起点和终点 clearance 检查
把 robot-safe path 与普通 path 在 UI 上区分显示
```

### 阶段 6-C：撤回整格膨胀，改为软性 clearance 诊断

#### 新问题

阶段 6 前面尝试过：

```text
PLANNING_OBSTACLE_INFLATION_CELLS = 1
```

也就是在路径规划前，把每个障碍物向周围膨胀一整格，然后在膨胀后的地图上搜索。

用户实际检查后指出这个策略不太可行：

```text
这样一格宽的路径都会被认为是 no path，
但实际上机器人半径是 0.35 cell，一格通道是可行的。
```

这个判断是正确的。对于一格宽通道，机器人沿通道中心线运动时，到上下障碍物边界的距离是：

```text
0.5 cell
```

而当前机器人半径是：

```text
ROBOT_RADIUS_CELLS = 0.35
```

因此理论 clearance 还有：

```text
0.5 - 0.35 = 0.15 cell
```

所以一格通道不应该被直接判定为无路。

#### 根本原因

整格 obstacle inflation 是一种过粗的离散近似。

它把连续几何问题：

```text
机器人圆形半径是否会碰到障碍物方块
```

简化成了：

```text
障碍物周围一整圈 cell 都不可走
```

这对安全性很保守，但副作用很明显：

```text
1-cell corridor 被误杀
起点/终点附近路径很容易被封死
规划器会频繁报告 no path
用户看到的可行通道和算法判断不一致
```

因此它不适合作为当前阶段的硬性规划规则。

#### 修正策略

本阶段撤回硬性整格膨胀：

```text
_run_search() 恢复在原始 GridMap 上运行 planner
```

也就是说，网格规划仍然按用户看到的 cell 可通行性判断：

```text
空白 cell 可走
障碍 cell 不可走
```

然后增加一个更温和的连续 clearance 诊断：

```text
规划成功后，计算路径中心线到障碍物方块边界的最小距离
```

如果 clearance 小于：

```text
ROBOT_RADIUS_CELLS + PLANNING_CLEARANCE_WARNING_MARGIN_CELLS
```

则不判 no path，而是在状态栏提示：

```text
tracking may be tight
```

这样做的好处：

```text
不会把一格通道误判为 no path
仍然能提醒用户某条路径对物理机器人可能比较贴边
把“是否有网格路径”和“物理跟踪是否安全”分开处理
```

#### 实现内容

配置变化：

```text
删除 PLANNING_OBSTACLE_INFLATION_CELLS
新增 PLANNING_CLEARANCE_WARNING_MARGIN_CELLS = 0.05
```

`main.py` 中新增：

```text
_path_min_clearance()
_segment_to_cell_rect_distance()
_point_to_rect_distance()
_planner_success_status()
```

其中 `_path_min_clearance()` 会把 path 转成连续 cell center 线段，并估算这些线段到所有障碍物方块的最小距离。

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

一格宽通道测试：

```text
one_cell_corridor found=True
path_len=8
clearance=0.5
path=[(13,1), (13,2), (13,3), (13,4), (13,5), (13,6), (13,7), (13,8)]
```

完整封死墙测试：

```text
blocked_wall found=False
status=A*: no path found.
```

这说明新的策略满足两个要求：

```text
一格宽但几何上可通行的路径：保留
真正被障碍物封死的路径：仍然 no path
```

#### 本次收获

这次修正很重要，因为它说明：

```text
连续机器人半径问题不能简单用整数 cell 膨胀代替
```

对于当前项目，更合理的阶段性策略是：

```text
Planner 负责找用户可理解的网格路径
Clearance diagnostics 负责提示物理跟踪风险
Controller / recovery 后续负责处理实际运动偏差
```

后续如果要做真正可靠的 robot-safe planning，应该考虑：

```text
亚格级 clearance 计算
line-of-sight 安全检查
基于机器人半径的连续碰撞检测
必要时再做更细粒度的配置空间搜索
```

而不是简单把所有障碍物膨胀一整格。

### 阶段 6-D：从 waypoint 点追踪升级到路径段跟踪

#### 阶段目标

在撤回整格膨胀策略后，继续处理机器人真实运行中可能卡住的问题。

本阶段的核心判断是：

```text
继续追单个 waypoint / 拐点 endpoint 仍然不够平滑。
```

因为机器人是连续刚体，有速度、朝向、角速度和惯性。如果控制目标只是一个离散点，机器人在长直道和拐点附近仍可能出现：

```text
接近目标点前减速过多
拐点附近被 endpoint 拉扯
偏离路径中心线后不容易判断偏差来源
```

所以阶段 6-D 的目标是把 `PathTracker` 从：

```text
追踪下一个 waypoint 点
```

升级为：

```text
追踪当前路径段上的前视目标点
```

#### 核心思路

路径规划仍然输出离散 cell path。

`PathTracker` 先保留阶段 6-B 的路径压缩逻辑：

```text
保留起点
保留转弯点
保留终点
删除同一直线段中的中间 cell center
```

然后每次更新时，不直接返回当前段终点，而是：

```text
1. 找到当前路径段 segment_start -> segment_end
2. 把机器人当前位置投影到该路径段上
3. 从投影点沿路径段方向向前推进 lookahead_distance
4. 把这个段内点作为控制器追踪目标
```

这样做有两个重要约束：

```text
lookahead target 必须留在当前路径段内
不能跨过拐点
```

这避免了阶段 6-B 测试中发现的风险：如果 lookahead 直接跳到更远 waypoint，机器人可能斜向穿过本来应该绕开的区域。

#### 实现内容

配置变化：

```text
删除 ROBOT_LOOKAHEAD_STEPS
新增 ROBOT_SEGMENT_LOOKAHEAD_CELLS = 0.75
```

`PathTrackerConfig` 从：

```text
lookahead_steps
```

改为：

```text
lookahead_distance
```

`TrackingTarget` 新增段诊断字段：

```text
segment_start
segment_end
segment_progress
cross_track_error
```

其中：

```text
segment_progress：机器人投影点在当前路径段上的进度
cross_track_error：机器人到当前路径段中心线的横向偏差
```

新增辅助结构与函数：

```text
SegmentProjection
_project_point_to_segment()
_interpolate()
```

主循环继续使用同一个控制器接口：

```text
WaypointForceController.compute_command(robot_state, target, dt)
```

因为控制器只需要 `target.waypoint`，所以这次改动主要集中在 tracker，不需要大改控制器。

#### UI 诊断增强

`RobotState` 新增：

```text
segment_progress
cross_track_error
```

右侧 `Simulation` 面板新增显示：

```text
Seg
XErr
```

实际运行时可以观察：

```text
Seg 是否持续增加：判断机器人是否沿当前段推进
XErr 是否变大：判断机器人是否偏离路径中心线
Stuck warnings 是否增加：判断是否低速且无进展
```

这比只看机器人是否停止更有帮助。

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

直线路径：

```text
straight_segment finished seconds=1.88 warnings=0 target=1 seg=1.0 xerr=0.0
```

90 度折线路径：

```text
turn_segment finished seconds=4.18 warnings=0 target=2 seg=1.0 xerr=0.0
```

一格宽通道：

```text
one_cell_corridor_segment finished seconds=3.23 warnings=0 path_len=8 target=1 seg=1.0 xerr=0.0
```

这些测试说明：

```text
段跟踪没有破坏直线、折线和一格通道
没有触发 stuck warning
主循环 planner -> animation finish -> start robot -> physics update 链路仍然可用
```

#### 当前结论

阶段 6-D 完成了一个更合理的连续跟踪基础：

```text
规划路径仍是网格路径
跟踪目标变成路径段上的前视点
前视点不跨拐点
UI 可以观察段进度和横向误差
```

这一步仍然不是完整局部避障，但它比单点 waypoint 追踪更接近真实机器人导航中的 path following。

#### 下一步建议

阶段 6-E 可以继续做：

```text
基于 cross_track_error 的横向纠偏控制
line-of-sight 安全 lookahead
碰撞/低速后的局部恢复动作
起点和终点 clearance 检查
把 stuck case 做成可重复的测试地图
```

其中最自然的下一步是：

```text
利用 cross_track_error 做更明确的路径段纠偏，而不是只靠追 lookahead target。
```

### 阶段 6-E：基于 cross-track error 的路径段横向纠偏

#### 阶段目标

阶段 6-D 已经把 `PathTracker` 从 waypoint 点追踪升级为路径段前视点追踪。

但仅追踪段内 lookahead target 仍然有一个不足：

```text
如果机器人因为惯性或碰撞偏离路径段中心线，
控制器主要还是朝前视点拉动，
没有明确使用 cross_track_error 把机器人拉回当前路径段。
```

阶段 6-E 的目标是补上这层横向纠偏：

```text
前视点牵引负责沿路径前进
cross-track correction 负责把机器人拉回当前路径段中心线
PID heading controller 继续负责朝向控制
```

#### 实现思路

`TrackingTarget` 在阶段 6-D 中已经包含：

```text
segment_start
segment_end
cross_track_error
```

因此控制器可以直接利用当前路径段信息。

本阶段在 `WaypointForceController` 中新增横向纠偏力：

```text
1. 将机器人当前位置投影到当前路径段上
2. 计算 position -> projected_position 的向量
3. 按 cross_track_gain 放大为纠偏力
4. 使用 max_cross_track_force 限幅
5. 将纠偏力叠加到原来的 waypoint/lookahead 牵引力中
```

直观理解：

```text
机器人沿段方向前进时，如果偏离中心线，
控制器会给一个温和的侧向力，把它拉回路径段。
```

#### 配置变化

新增：

```text
ROBOT_CROSS_TRACK_GAIN = 10.0
ROBOT_MAX_CROSS_TRACK_FORCE = 12.0
```

这两个值先采用保守设置：

```text
gain 不过高，避免横向震荡
force 有上限，避免纠偏力压过主驱动力
```

#### 代码改动

`WaypointForceControllerConfig` 新增：

```text
cross_track_gain
max_cross_track_force
```

`WaypointForceController` 新增：

```text
_cross_track_correction()
_project_point_to_segment()
```

控制器总力从：

```text
force = drive_force_to_target - damping_force
```

升级为：

```text
force = drive_force_to_lookahead
      + cross_track_correction
      - damping_force
```

最后仍然经过：

```text
_clamp_vector(force, max_force)
```

防止输出力过大。

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

直线路径：

```text
straight_cross_track finished seconds=1.88 warnings=0 target=1 seg=1.0 xerr=0.0
```

90 度折线路径：

```text
turn_cross_track finished seconds=4.27 warnings=0 target=2 seg=1.0 xerr=0.0
```

一格宽通道：

```text
one_cell_corridor_cross_track finished seconds=3.23 warnings=0 path_len=8 target=1 seg=1.0 xerr=0.0
```

这些结果说明：

```text
横向纠偏没有破坏已有直线、折线、一格通道场景
没有触发 stuck warning
现有 PID heading controller 和 fixed timestep 仍然正常工作
```

#### 当前结论

阶段 6-E 让控制系统从：

```text
只追前方目标点
```

变成：

```text
追前方目标点 + 主动回到当前路径段
```

这更接近真实路径跟踪中的组合控制逻辑。

它仍然不是完整局部避障，也不能保证所有复杂地图都不卡住；但当机器人偏离当前路径段时，系统现在有了明确的横向恢复趋势，而不是完全依赖前视点牵引。

#### 下一步建议

阶段 6-F 建议优先做可重复 stuck case：

```text
把用户实际遇到的卡死地图保存成测试用例
在测试里记录 Target / Dist / Seg / XErr / Stuck warnings
确认卡死究竟来自碰撞、过冲、路径 clearance 太紧，还是控制器参数问题
```

随后再根据诊断结果选择：

```text
碰撞/低速局部恢复
line-of-sight 安全 lookahead
起点/终点 clearance 检查
更细粒度连续 collision checking
```

### 阶段 6-F：物理参数可视化与保守调参

#### 新问题

用户实际运行后反馈：

```text
机器人几乎都不能正常沿着路径走。
```

并进一步提出一个关键判断：

```text
可能不是路径规划本身的问题，
而是物理属性、PID 参数、驱动力和阻尼不匹配。
```

这个判断很重要。因为此前 UI 主要显示：

```text
Target
Distance
Seg
XErr
Stuck warnings
```

这些能说明机器人有没有沿路径段推进，但看不到：

```text
机器人质量
半径
速度
受力大小
扭矩大小
驱动力
阻尼
PID 参数
最大速度限制
```

因此用户无法判断：

```text
是路径跟踪策略错了
还是力太大
还是速度太快
还是 PID 转向太猛
还是阻尼不足
```

#### 本阶段目标

阶段 6-F 的目标不是继续盲目调参，而是先让物理与控制参数可见：

```text
运行时能看到机器人实际速度
运行时能看到控制器输出力和扭矩
运行时能看到关键物理 / PID 参数
默认参数先调得更保守，降低过冲和撞墙概率
```

#### 实现内容

##### 1. RobotState 新增物理遥测字段

新增：

```text
speed
angular_velocity
force
torque
```

主循环在每次物理 step 前后同步：

```text
robot.speed
robot.angular_velocity
robot.force
robot.torque
```

这样 UI 可以直接显示当前机器人运动状态和控制输入。

##### 2. UI Simulation 面板增加物理与控制参数

右侧 `Simulation` 面板现在显示：

```text
Robot status + Speed
Target + Dist
Seg + XErr
Force + Torque
Mass + Radius
Drive + Damping
PID Kp/Kd + Max Torque
Max Velocity + Stuck warnings
```

这样实际运行时可以观察：

```text
Speed 是否长期顶到 MaxV
Force 是否经常接近 MaxForce
Torque 是否经常打满 MaxT
XErr 是否不断变大
Stuck 是否持续增加
```

##### 3. 默认参数改为更保守

旧参数偏激进：

```text
ROBOT_DRIVE_FORCE = 35.0
ROBOT_DAMPING_FORCE = 8.0
ROBOT_CROSS_TRACK_GAIN = 10.0
ROBOT_MAX_CROSS_TRACK_FORCE = 12.0
ROBOT_MAX_FORCE = 45.0
ROBOT_MAX_SPEED_CELLS_PER_SECOND = 2.2
ROBOT_HEADING_PID_KP = 14.0
ROBOT_HEADING_PID_KD = 3.0
ROBOT_MAX_TORQUE = 90.0
```

阶段 6-F 调整为：

```text
ROBOT_DRIVE_FORCE = 24.0
ROBOT_DAMPING_FORCE = 12.0
ROBOT_CROSS_TRACK_GAIN = 7.0
ROBOT_MAX_CROSS_TRACK_FORCE = 8.0
ROBOT_MAX_FORCE = 32.0
ROBOT_MAX_SPEED_CELLS_PER_SECOND = 1.6
ROBOT_HEADING_PID_KP = 10.0
ROBOT_HEADING_PID_KD = 2.5
ROBOT_MAX_TORQUE = 60.0
```

调参方向：

```text
降低驱动力
提高阻尼
降低最大速度
降低转向 PID 强度
降低最大扭矩
降低横向纠偏力
```

目的是减少：

```text
过冲
急转
撞墙
贴障碍物时的抖动
```

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

直线路径：

```text
straight_tuned finished seconds=2.75 warnings=0 max_speed=1.5 max_force=17.6
```

90 度折线路径：

```text
turn_tuned finished seconds=4.63 warnings=0 max_speed=1.6 max_force=22.8
```

一格宽通道：

```text
one_cell_corridor_tuned finished seconds=4.75 warnings=0 path_len=8 max_speed=1.5 max_force=17.6
```

结果说明：

```text
保守参数没有破坏基础场景
机器人速度被控制在更低范围
测试中没有触发 stuck warning
```

#### 当前结论

这一步确认了一个很重要的方向：

```text
机器人实际运行不稳定，不能只从路径规划和 tracker 解释。
必须把物理参数和控制参数暴露出来，才能调试。
```

阶段 6-F 后，用户运行程序时可以直接观察：

```text
力是否太大
速度是否太快
扭矩是否太猛
PID 是否可能过激
是否发生低速无进展 stuck
```

#### 下一步建议

下一步应该基于 UI 中的实际数值调参，而不是继续猜。

推荐观察规则：

```text
Speed 经常等于 MaxV：
    最大速度仍偏高，或驱动力偏大。

Force 经常接近 MaxForce：
    驱动力 / 横向纠偏力可能偏大。

Torque 经常接近 MaxT：
    PID Kp 或 Max Torque 可能偏大。

XErr 越来越大：
    横向纠偏不足，或者路径 clearance 太紧。

Speed 很低、Force 很大、Stuck 增加：
    可能已经碰撞卡住，需要局部恢复或更好的 collision handling。
```

后续阶段可以做：

```text
UI 参数滑条 / 输入框
运行中暂停/重置机器人
保存 stuck 地图作为测试用例
更系统的 PID 和力参数调参表
```

### 阶段 6-G：路径外偏离保护与路径段重捕获

#### 新问题

用户实际运行并提供截图后发现：

```text
机器人被推到了规划路径外面。
```

截图中的 UI 数值非常关键：

```text
Speed: 0.01
Target: 1
Dist: 3.51
Seg: -1.85
XErr: 3.51
Force: 26.5
Torque: -4.9
```

这些数值说明：

```text
机器人几乎不动
距离当前目标很远
投影进度 Seg 为负数，而且小于 -1
横向误差 XErr 很大
控制器仍在输出较大的 force
```

这不是普通“走得不够准”，而是：

```text
机器人已经明显偏离当前路径段，
但 tracker 仍然锁定旧 segment，
controller 还在继续硬推。
```

#### 根本原因

阶段 6-D 的路径段跟踪只会向前推进 segment：

```text
如果机器人接近当前段尾，进入下一段
```

但它没有处理一种真实物理仿真中很常见的情况：

```text
机器人被碰撞、惯性或控制力推出当前路径段附近
```

这时当前段投影会出现：

```text
segment_progress < 0
或者 segment_progress > 1
或者 cross_track_error 很大
```

如果 tracker 不重捕获最近路径段，controller 会继续对旧段施力。

结果就是：

```text
越偏离，越被错误目标拉扯
越可能撞墙或卡在障碍物附近
```

#### 修复策略

本阶段新增两层保护。

##### 1. PathTracker 最近路径段重捕获

新增配置：

```text
ROBOT_SEGMENT_RECAPTURE_DISTANCE_CELLS = 0.9
ROBOT_SEGMENT_RECAPTURE_PROGRESS_MARGIN = 0.35
```

当当前段满足任一条件：

```text
cross_track_error > recapture_distance
segment_progress < -recapture_progress_margin
segment_progress > 1 + recapture_progress_margin
```

就扫描压缩路径中的所有 segment，选择离机器人最近的路径段作为新的当前段。

这样可以避免机器人偏离后还一直追旧路径段。

##### 2. 偏离路径过大时降低前进驱动力

新增配置：

```text
ROBOT_PATH_DEVIATION_SLOWDOWN_CELLS = 0.8
ROBOT_PATH_DEVIATION_STOP_CELLS = 1.4
```

控制器新增逻辑：

```text
XErr <= 0.8：
    正常前进

0.8 < XErr < 1.4：
    逐渐降低前进驱动力

XErr >= 1.4：
    前进驱动力降为 0，只保留回线纠偏和阻尼
```

这样机器人偏离路径很远时，不会继续朝前视目标硬冲，而是优先回到路径段附近。

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

截图式偏离单元测试：

```text
recapture_unit target=2 seg=1.125 xerr=4.727 waypoint=(17.5, 13.5)
```

这说明 tracker 不再停留在旧的 `target=1 / seg=-1.85` 一类状态，而是会切到更接近机器人的后续 segment。

基础回归测试：

```text
straight_recapture_regression finished seconds=2.75 warnings=0 max_xerr=0.0
turn_recapture_regression finished seconds=4.63 warnings=0 max_xerr=0.519
one_cell_corridor_recapture_regression finished seconds=4.75 warnings=0 max_xerr=0.0
```

说明新增重捕获逻辑没有破坏基础直线、折线和一格通道。

#### 当前结论

阶段 6-G 修复的是一个关键系统缺陷：

```text
机器人偏离路径后，不能继续盲目追旧 segment。
```

现在系统具备：

```text
偏离检测
最近 segment 重捕获
大偏离时停止前冲
基础路径回归稳定
```

这仍然不等于完整局部避障，但已经避免了截图中最危险的行为：

```text
XErr 很大时仍用较大 force 继续推机器人离开路径。
```

#### 下一步建议

如果真实运行仍然出现偏离，需要继续观察：

```text
Seg 是否回到 0~1 附近
XErr 是否下降
Force 是否明显小于之前的 26.5
Speed 是否不再长期接近 0
Stuck warnings 是否增加
```

如果：

```text
XErr 很大、Speed 很低、Force 不大但仍无法回线
```

说明机器人可能已经被障碍物物理卡住，下一阶段应做：

```text
碰撞后局部恢复动作
暂停/重置机器人按钮
保存当前地图为 stuck test case
```

### 阶段 6-H：物理阻塞 blocked 状态与停止硬推

#### 新问题

用户再次实际运行后反馈：

```text
机器人卡死。
```

这次截图中的关键信号与上一轮不同：

```text
Speed: 0.00
Target: 1
Dist: 0.77
Seg: 0.19
XErr: 0.15
Force: 18.0
```

这说明机器人并没有严重偏离当前路径段：

```text
Seg 在 0~1 内
XErr 只有 0.15
```

也就是说，tracker 认为机器人仍贴近当前路径段；但刚体速度为 0，控制器仍在输出明显的 force。

因此这次问题不是“追错 segment”，而是：

```text
机器人贴着路径，但物理上走不动。
```

更像是机器人被障碍物、拐角、窄通道或碰撞体卡住。

#### 根本原因

此前 `_update_robot_stuck_diagnostics()` 只做提示：

```text
Robot may be stuck
```

但并不会停止控制器继续施力。

结果是：

```text
机器人已经低速无进展
控制器仍然持续 apply force
刚体可能被持续顶在障碍物或角落上
UI 只显示 stuck，但系统没有进入明确故障状态
```

#### 修复策略

本阶段新增明确的物理阻塞状态：

```text
blocked
```

触发条件从单纯“低速无进展”升级为：

```text
速度低于 ROBOT_STUCK_SPEED_THRESHOLD_CELLS_PER_SECOND
距离目标没有明显变小
控制输出 force 高于 ROBOT_BLOCKED_FORCE_THRESHOLD
持续超过 ROBOT_STUCK_TIMEOUT_SECONDS
```

新增配置：

```text
ROBOT_BLOCKED_FORCE_THRESHOLD = 8.0
```

当触发 blocked 后：

```text
robot.active = False
robot.blocked = True
robot.force = (0, 0)
robot.torque = 0
physics_world.stop_robot()
```

并显示明确状态：

```text
Robot blocked: low speed despite force.
The physical robot may be wedged against an obstacle or the path is too tight.
```

#### 实现内容

`RobotState` 新增：

```text
blocked
```

`PhysicsWorld` 新增：

```text
stop_robot()
```

用于清空：

```text
velocity
angular_velocity
force
torque
```

右侧 `Simulation` 面板现在会区分：

```text
running
blocked
finished
idle
```

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

阻塞检测单元测试：

```text
blocked_detection_unit blocked=True active=False warnings=1
```

基础回归：

```text
straight_blocked_regression finished seconds=2.75 blocked=False warnings=0
turn_blocked_regression finished seconds=4.63 blocked=False warnings=0
one_cell_corridor_blocked_regression finished seconds=4.75 blocked=False warnings=0 path_len=8
```

说明：

```text
真实 blocked 条件可以触发停止硬推
正常直线、折线、一格通道不会误触发 blocked
```

#### 当前结论

阶段 6-H 不是让机器人自动脱困，而是先避免更糟的行为：

```text
不要在物理卡住时继续施力。
```

现在系统能区分：

```text
偏离路径：Seg / XErr 异常，触发 segment recapture 和前进力削弱
物理卡住：Seg / XErr 正常但 Speed 低、Force 高、无进展，触发 blocked
```

这为下一步真正的局部恢复打基础。

#### 下一步建议

阶段 6-I 可以做：

```text
Reset Robot 按钮：把机器人放回当前路径最近安全点
Pause / Resume Robot
Save Stuck Case：保存当前地图、路径、机器人位置和诊断数据
局部恢复动作：blocked 后先后退/侧移一点，再尝试继续
```

其中最适合先做的是：

```text
Reset Robot 按钮
```

因为目前系统已经能识别 blocked，但用户还缺少一个方便的恢复操作。

### 阶段 6-I：起步朝向对齐

#### 问题背景

用户在一段很短的直线路径中观察到：

```text
机器人起步阶段几乎偏出目标路径
并且在终点前卡住
```

这说明问题不只发生在复杂拐角。即使路径本身是一条简单直线，如果机器人刚开始运动时朝向和第一段路径方向不一致，控制器也可能在尚未对准方向时就施加前进力，导致机器人先产生横向偏移。

在窄通道或障碍物靠近路径中心线时，这种起步偏移会被放大成碰撞或 blocked。

#### 设计目标

本阶段先解决一个小而明确的问题：

```text
机器人启动后，先检查当前朝向是否与路径第一段方向一致。
如果不一致，则先原地转向。
只有朝向误差进入容差后，才允许施加前进推力。
```

这一步不试图一次性解决所有窄通道卡死问题，而是把运动流程拆成更合理的状态：

```text
startup alignment
→ normal path tracking
→ goal completion / blocked detection
```

#### 实现内容

##### 1. RobotState 增加起步对齐状态

新增字段：

```text
aligning_heading
heading_error
```

其中：

```text
aligning_heading：当前是否处于起步朝向对齐阶段
heading_error：当前机器人朝向与目标路径方向之间的角度误差
```

右侧 Simulation 面板同步显示：

```text
Robot: aligning / running / blocked / finished / idle
HeadErr
Align
```

这样用户可以直接看到机器人是在“先转向”，还是已经开始正常路径跟踪。

##### 2. 启动时不再直接把角度设成路径方向

之前 `_start_robot()` 会把机器人初始角度直接设为第一段路径方向。

这虽然能减少偏移，但它绕过了真实仿真流程：

```text
机器人没有经历从初始朝向转到路径方向的过程
也无法验证起步对齐控制是否正确
```

现在启动时保留默认初始朝向：

```text
robot.angle = 0.0
robot.aligning_heading = True
```

后续由物理世界中的 torque 真实完成转向。

##### 3. 起步对齐阶段只转向，不前进

新增 `_align_robot_heading_before_drive()`。

每个物理 step 中，正常 waypoint force controller 之前先执行：

```text
desired_heading = atan2(target_y - robot_y, target_x - robot_x)
heading_error = normalize(desired_heading - robot.angle)
```

如果还没有对齐：

```text
force = (0, 0)
torque = heading_pid.update(heading_error, dt)
只推进角度，不施加前进力
```

只有当角度误差进入容差后：

```text
aligning_heading = False
reset heading PID
进入正常路径跟踪
```

新增配置：

```text
ROBOT_START_HEADING_TOLERANCE_RADIANS = 0.12
ROBOT_START_ALIGNMENT_SPEED_THRESHOLD_CELLS_PER_SECOND = 0.05
```

##### 4. 修复对齐阶段“只产生角速度、不改变角度”的问题

第一次实现中，对齐阶段使用了：

```text
physics_world.stop_robot()
```

用于防止机器人平移。

但这个方法会同时清空：

```text
velocity
angular_velocity
force
torque
```

Pymunk 中 torque 会先改变 angular_velocity，角度变化需要后续 step 积累。如果每一步都清空 angular_velocity，机器人就会一直停在原角度，永远无法真正完成转向。

因此新增：

```text
PhysicsWorld.stop_robot_translation()
```

它只清空线速度和线性 force：

```text
velocity
force
```

保留 angular_velocity，让原地转向可以在物理世界中真实发生。

对齐完成瞬间再调用：

```text
physics_world.stop_robot()
```

用于清掉残留角速度，避免刚开始前进时仍带着转动惯性。

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

起步对齐 smoke test：

```text
vertical_startup_alignment alignment_steps=59 first_drive_step=58 finished=True blocked=False max_alignment_drift=0.0000 angle=-1.472 heading_error=0.015 xerr=0.000
horizontal_startup_alignment alignment_steps=1 first_drive_step=0 finished=True blocked=False max_alignment_drift=0.0000 angle=0.000 heading_error=0.000 xerr=0.000
```

解释：

```text
竖直路径：初始朝向与路径方向不一致，因此先经历 59 个物理步的原地对齐，然后开始前进。
水平路径：初始朝向已经与路径方向一致，因此几乎立即进入正常跟踪。
max_alignment_drift = 0.0000，说明对齐阶段没有产生可见平移。
两个 case 都没有 blocked。
```

#### 当前结论

阶段 6-I 修复的是一个明确的起步控制问题：

```text
不要在机器人还没有面向路径方向时就给前进力。
```

它能减少直线路径起步阶段的横向偏移，尤其对窄通道和靠近障碍物的路径更重要。

但这还不是完整的窄通道解决方案。后续如果机器人已经进入路径后仍然因为横向误差或障碍物边界卡住，还需要继续做：

```text
狭窄通道感知的速度控制
路径段 signed cross-track error
切向 / 法向分解控制
终点接近低速模式
当前目标点和投影点可视化
```

#### 本次收获

这次调试说明了一个重要经验：

```text
“停止移动”不等于“清空所有物理状态”。
```

在刚体仿真中，线速度、角速度、force 和 torque 是不同的状态量。为了让机器人原地转向，应当只禁止平移，而不能把角速度也一起清掉。

这也是 RobotNav 进入物理仿真阶段后的核心变化之一：每个控制动作都必须明确它影响的是平移、旋转，还是两者都影响。

### 阶段 6-J：修复推力坐标系错误

#### 问题背景

用户在实际运行中继续观察到：

```text
机器人在拐弯处仍然容易卡住
起步阶段依然存在漂移
```

用户提出了一个关键判断：

```text
到达拐点后，目标方向切换到下一个路径段；
但小车自身速度仍然沿旧路径段方向；
因此在拐点处容易撞到障碍物或卡住。
```

这个判断是成立的：物理机器人有质量和速度，不能像离散路径点一样瞬间改变运动方向。拐点处如果不先减速和消除旧方向速度，就会出现过冲。

但在继续设计拐点减速策略前，本阶段先发现了一个更底层的问题：

```text
WaypointForceController 计算的是 world-space force
PhysicsWorld.apply_robot_force 却使用了 apply_force_at_local_point()
```

这意味着控制器认为自己在世界坐标中施力，例如“向上推”或“向右推”，但 Pymunk 实际会把这个 force 当成机器人本地坐标中的方向。

当机器人角度不是 0 时，推力方向会被机器人朝向再次旋转。

#### 如何发现

通过最小 Pymunk 验证：

```text
local_point angle=0.00 velocity=(1.000,0.000)
local_point angle=1.57 velocity=(0.000,1.000)
world_point angle=0.00 velocity=(1.000,0.000)
world_point angle=1.57 velocity=(1.000,0.000)
```

解释：

```text
apply_force_at_local_point((10, 0)) 会随 body.angle 改变世界方向
apply_force_at_world_point((10, 0), body.position) 才始终表示世界坐标中的向右推力
```

而当前控制器的 force 是根据：

```text
world position
world velocity
segment_start / segment_end
cross_track_error
```

计算出来的，所以它必须按 world-space force 施加。

#### 修复方案

修改：

```text
robot_path_planning/physics/physics_world.py
```

从：

```text
self.robot_body.apply_force_at_local_point(force)
```

改为：

```text
self.robot_body.apply_force_at_world_point(force, self.robot_body.position)
```

这样控制器输出的世界坐标推力和物理引擎实际接收到的推力方向一致。

#### 为什么这会影响起步漂移

起步对齐后，如果机器人朝向已经变成竖直方向，而控制器输出一个竖直方向的世界推力，旧实现会再次按机器人本地坐标旋转这个推力。

结果就是：

```text
控制器想沿路径中心线推
物理引擎实际推到了偏离中心线的方向
```

这会让用户看到：

```text
明明 HeadErr 很小
Align 也已经 False
但机器人起步仍然偏出路径
```

修复后，起步漂移应明显减少，因为 force 方向不再被错误旋转。

#### 为什么这会影响拐点卡住

拐点处本来就存在一个真实控制难点：

```text
路径目标方向已经切到下一段
机器人线速度还沿上一段方向
```

旧实现还额外叠加了坐标系错误：

```text
机器人转向越明显
推力方向越可能偏离控制器预期
```

这会让拐点附近的纠偏力、阻尼力和前进力都不可靠，增加撞墙和 blocked 的概率。

#### 验证结果

编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

结果：

```text
通过
```

运动 smoke test：

```text
horizontal_straight finished=True blocked=False align_steps=1 max_align_drift=0.0000 max_xerr=0.000 max_speed=1.497
vertical_straight finished=True blocked=False align_steps=59 max_align_drift=0.0000 max_xerr=0.000 max_speed=1.497
turn_case finished=True blocked=False align_steps=1 max_align_drift=0.0000 max_xerr=0.345 max_speed=1.485
one_cell_corridor finished=True blocked=False align_steps=1 max_align_drift=0.0000 max_xerr=0.000 max_speed=1.497
```

这些结果说明：

```text
起步对齐阶段没有平移漂移
直线和竖直路径可以完成
简单 90 度拐弯可以完成
一格直线通道仍然可通过
```

#### 当前结论

阶段 6-J 修复的是一个根因级 bug：

```text
控制器输出 world-space force
物理层必须按 world-space force 施加
```

这个修复应优先于继续调 PID 或增加复杂转弯策略。

但用户提出的拐点速度惯性问题仍然是真实存在的。修复坐标系后，如果复杂地图拐点仍然卡住，下一阶段应该继续做：

```text
拐点接近减速
切向速度 / 法向速度分解
进入新 segment 前先消除旧方向速度
拐点处先对齐新方向，再恢复前进力
```

#### 本次收获

这次问题说明：在物理仿真项目中，先确认坐标系非常重要。

尤其是以下几类量必须明确：

```text
world-space position
world-space velocity
world-space force
body-local force
body angle
screen coordinate
grid coordinate
```

如果坐标系混用，表面现象会像是 PID 参数不合适、机器人太重、推力太大或阻尼太小，但真正原因可能是力的方向从一开始就错了。

### Week 4 收尾总结 - 2026-07-12

#### 本周项目状态

Week 4 已完成从“离散路径动画”到“连续物理机器人仿真”的第一版闭环。

当前 RobotNav 已经具备：

```text
网格地图编辑
BFS / A* / DFS / Dijkstra / Greedy 路径规划
搜索过程动画
运行历史复现
Pymunk 连续刚体物理世界
动态圆形机器人与静态方块障碍物
连续 world position
PathTracker 路径段跟踪
WaypointForceController 力控制
PID heading controller
起步朝向对齐
cross-track error 诊断与纠偏
blocked 状态检测与停止硬推
Simulation 物理诊断面板
Week 4 QA 文档
```

本周最重要的变化不是新增一个独立按钮，而是完成了导航系统的核心架构升级：

```text
路径规划：决定哪里可以走
PathTracker：决定当前应该追踪哪一段路径
Controller：决定施加什么 force / torque
PhysicsWorld：决定机器人在真实物理约束下实际怎么运动
UI diagnostics：暴露卡死、偏离、朝向和物理参数问题
```

#### 本周关键成果

1. **Pymunk 物理世界接入**

   机器人不再是沿路径插值移动的动画点，而是具有质量、半径、速度、角度和碰撞体的动态刚体。

2. **连续坐标系统**

   项目明确区分：

   ```text
   grid cell
   world position
   screen pixel
   ```

   这为路径规划和物理仿真之间建立了稳定接口。

3. **路径段跟踪**

   `PathTracker` 不再要求机器人精确踩中每个 cell center，而是把路径压缩成起点、拐点和终点，并基于当前 segment 生成 lookahead target。

4. **PID 朝向控制**

   PID 负责根据 heading error 输出 torque，让机器人逐渐朝向目标方向。

5. **力控制和横向纠偏**

   `WaypointForceController` 综合：

   ```text
   forward drive
   velocity damping
   cross-track correction
   heading gate
   arrival slowdown
   max force
   ```

   输出世界坐标系下的线性 force。

6. **卡死诊断与 blocked 状态**

   当机器人低速、无进展且控制器持续施力时，系统会进入 blocked 状态，清空 force / torque，避免继续硬推。

7. **起步朝向对齐**

   机器人启动后先检查朝向。未对准第一段路径方向时，只原地转向，不施加前进力。

8. **修复 force 坐标系错误**

   本周发现并修复了一个根因级问题：

   ```text
   控制器输出 world-space force
   物理层却曾按 local-space force 施加
   ```

   修复为 `apply_force_at_world_point()` 后，控制器的受力方向和 Pymunk 实际施力方向一致。

#### 本周验证

完成了基础编译验证：

```bash
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall robot_path_planning
```

并完成了关键运动 smoke test：

```text
horizontal_straight
vertical_straight
turn_case
one_cell_corridor
```

验证结果说明：

```text
直线路径可以完成
竖直路径可以完成
简单 90 度转弯可以完成
一格直线通道仍然可通过
起步对齐阶段不产生平移漂移
基础场景不会误触发 blocked
```

#### 仍然存在的限制

Week 4 完成的是“物理路径跟踪闭环”的第一版，不代表所有真实地图都已经稳定。

仍需继续改进：

```text
复杂拐点处旧方向速度尚未完全处理
窄通道需要根据 clearance / XErr 降速
blocked 后还没有自动恢复策略
当前 segment、投影点和 lookahead target 尚未可视化
典型 stuck case 还没有保存为回归测试地图
```

#### Week 5 建议方向

下一周建议围绕“拐点与窄通道稳定性”继续推进：

```text
阶段 7-A：拐点接近减速
阶段 7-B：切向速度 / 法向纠偏控制拆分
阶段 7-C：窄通道速度保护
阶段 7-D：当前 segment、投影点、lookahead target 可视化
阶段 7-E：Reset Robot / Pause / Resume / blocked recovery
阶段 7-F：保存 stuck case 并建立回归测试
```

#### 收尾结论

Week 4 的最大收获是：

```text
PID 不是魔法。
```

PID 可以帮助机器人控制朝向，但稳定导航还需要：

```text
正确的坐标系
合理的路径跟踪
速度和力限制
横向误差纠偏
物理碰撞诊断
起步和拐点状态管理
```

这周的迭代让 RobotNav 真正进入了机器人导航仿真的核心问题区：不只是“找到路”，而是让一个有半径、有质量、有速度、有朝向的机器人，在连续物理世界中稳定地沿着路走。
