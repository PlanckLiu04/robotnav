# RobotNav：可交互的 2D 机器人路径规划与仿真控制平台

## 项目简介

RobotNav 是一个使用 Python + Pygame 开发的二维机器人路径规划与仿真控制项目。

当前项目已经进入 Week 2：在第一阶段单文件原型的基础上，代码已经按功能拆分为地图、规划、渲染、UI 和应用状态模块，并新增了启动主界面、运行界面、算法选择、运行统计和基础机器人路径跟随模拟。

项目最终目标是做成一个适合初学者学习和展示的机器人导航仿真平台，逐步包含地图编辑、路径规划、搜索过程可视化、机器人运动仿真、PID 控制和算法效果对比。

## 当前已实现功能

- 创建 Pygame 2D 窗口。
- 启动时进入主界面：
  - 显示简短过渡引导。
  - 按 `Enter` 或点击 `Start Lab` 进入运行界面。
- 绘制规则网格地图。
- 鼠标点击交互。
- 按 `1` 切换障碍物模式：
  - 点击空白格子添加黑色障碍物。
  - 再次点击黑色格子取消障碍物。
  - 按住鼠标左键拖动可以连续添加或擦除障碍物。
- 按 `2` 切换起点模式：
  - 点击格子设置绿色起点。
  - 起点只有一个，以最后一次设置为准。
- 按 `3` 切换终点模式：
  - 点击格子设置红色终点。
  - 终点只有一个，以最后一次设置为准。
- 按 `Tab` 或点击算法按钮切换 `BFS` / `A*`。
- 按 `Space` 执行当前选择的路径规划算法：
  - 如果存在可通行路线，会显示蓝色路径。
- 运行界面显示算法统计：
  - 当前算法。
  - 运行时间。
  - 访问节点数。
  - 路径长度。
- UI 清晰度优化：
  - 右侧面板加宽。
  - 窗口调整为 `1160 x 780`，减少桌面遮挡，同时给信息区留出空间。
  - 地图区为 `840 x 780`，对应 `28 x 26` 个完整 `30px` 网格。
  - 使用跨平台系统字体候选列表。
  - 运行界面使用更紧凑但清晰的字号。
  - 编辑模式和寻路算法改为浮层下拉选择。
  - 状态消息最多显示两行，避免挤压底部信息栏。
- 按 `S` 或点击 `Start Robot` 启动基础机器人路径跟随动画。
- 右侧 UI 面板：
  - 通过 `Edit Mode` 下拉选择 `Obstacle`、`Start`、`Goal`。
  - 通过 `Path Planner` 下拉选择 `BFS`、`A*`。
  - 点击 `Run Planner` 执行路径规划。
  - 点击 `Start Robot` 播放机器人沿路径运动。
  - 点击 `Random Map` 随机生成障碍物、起点和终点。
  - 点击 `Clear` 清空地图。
  - 点击 `Home` 返回主界面。
  - 显示当前模式、障碍物数量、访问节点数、路径长度和状态信息。
- 按 `R` 随机生成障碍物、起点和终点。
- 按 `C` 清空障碍物、起点、终点和搜索结果。
- 找不到路径时显示 `No path found` 状态。
- BFS 搜索后显示访问过的节点，为后续搜索过程动画做准备。

## 运行方式

推荐先创建并激活 Python 环境，然后安装依赖：

```bash
pip install -r requirements.txt
```

从仓库根目录运行：

```bash
python3 robot_path_planning/main.py
```

也可以进入代码目录后运行：

```bash
cd robot_path_planning
python3 main.py
```

如果你的系统中 `python3` 不可用，可以尝试使用 `python`。

## 操作说明

```text
按 1：障碍物编辑模式
按 2：设置起点模式
按 3：设置终点模式
按 Tab：切换 BFS / A*
按 Space：执行当前算法
按 S：启动机器人路径跟随模拟
按 R：随机生成障碍物、起点和终点
按 C：清空地图和搜索结果
按 H：返回主界面
关闭窗口：退出程序
```

也可以使用右侧 UI 面板中的下拉框和按钮完成同样操作。

在障碍物模式下，可以按住鼠标左键拖动：

```text
从空白格开始拖动：连续添加障碍物
从障碍物开始拖动：连续擦除障碍物
```

颜色含义：

```text
浅色格子：可通行区域
黑色格子：障碍物
绿色格子：起点
红色格子：终点
蓝色格子：规划得到的路径
浅蓝格子：当前算法访问过的节点
黄色圆点：机器人
黄色线条：机器人运动轨迹
```

## 当前目录结构

```text
.
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── project.md
├── docs/
│   └── dev_log.md
└── robot_path_planning/
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
    ├── ui/
    │   ├── __init__.py
    │   ├── fonts.py
    │   └── panel.py
    └── README.md
```

说明：

```text
README.md：仓库首页说明，给使用者和后续 AI 快速了解项目。
CHANGELOG.md：开发日志，记录每周完成的功能。
requirements.txt：pip 依赖文件。
environment.yml：Conda 环境文件。
.gitignore：Git 忽略规则。
project.md：完整项目规划文档。
docs/dev_log.md：开发过程、设计决策和下一步计划。
robot_path_planning/config.py：窗口尺寸、网格尺寸、颜色和 FPS 等配置。
robot_path_planning/main.py：当前 Pygame 程序入口，负责主循环和事件分发。
robot_path_planning/core/：地图数据结构和应用状态。
robot_path_planning/planning/：路径规划算法，目前包含 BFS 和 A*。
robot_path_planning/rendering/：Pygame 绘制逻辑。
robot_path_planning/ui/：右侧控制面板和按钮。
robot_path_planning/ui/fonts.py：跨平台字体选择工具，用于提升文字清晰度。
robot_path_planning/README.md：早期阶段说明文档，后续可合并到根目录 README。
```

## 当前代码结构

Week 2 后，项目开始采用模块化结构。`robot_path_planning/main.py` 只保留程序入口、主循环和事件分发，不再直接写地图逻辑、规划算法和绘图细节。

核心模块：

```text
config.py：统一管理窗口、网格、颜色等常量。
core/grid_map.py：GridMap 保存障碍物、起点、终点，并提供邻居查询。
core/app_state.py：AppState 保存当前模式、路径、访问节点和状态文字。
planning/bfs.py：BFS 算法，输入 GridMap、起点和终点，输出 SearchResult。
planning/astar.py：A* 算法，用曼哈顿距离作为启发函数。
rendering/renderer.py：Renderer 负责绘制地图、路径、访问节点和起终点。
ui/panel.py：SidePanel 负责绘制启动主界面、右侧 UI、算法选择和统计信息。
ui/fonts.py：按 macOS、Windows、Linux 常见字体自动匹配清晰字体，找不到时回退到 Pygame 默认字体。
main.py：连接所有模块，处理键盘、鼠标、按钮、算法运行、统计和机器人模拟。
```

当前主循环流程：

```text
读取 Pygame 事件
→ 处理键盘或鼠标输入
→ 更新 GridMap 和 AppState
→ 需要时调用当前选择的路径规划算法
→ Renderer 重绘地图和 UI
→ 刷新窗口
```

## BFS 算法说明

BFS 是 Breadth-First Search，也就是广度优先搜索。

在当前网格地图中，BFS 从起点开始，一层一层向外扩散搜索：

```text
第 0 层：起点
第 1 层：起点上下左右相邻的格子
第 2 层：再往外一圈的格子
...
直到找到终点
```

因为当前地图中每移动一格的代价相同，所以 BFS 找到的路径是最短路径之一。

关键数据结构：

```text
queue：队列，保存接下来要访问的格子
visited：集合，记录已经访问过的格子
parent：字典，记录每个格子从哪个上一个格子走来，用于还原路径
```

## Git 工作流

建议从项目一开始就使用 Git 记录开发历史：

```text
main 分支：始终保持可运行版本
feature 分支：开发某个较大功能时使用，可选
每周六结束：至少提交一次 commit
每个阶段完成：打一个 tag
```

推荐提交节奏：

```text
Week 1: init project structure and pygame grid
Week 2: modularize project and add UI panel
Week 3: implement BFS planner
Week 4: implement A* planner and metrics
Week 5: add robot model
Week 6: add PID heading controller
Week 7: connect path tracking simulation
Week 8+: polish docs and demo
```

常用命令：

```bash
git status
git add .
git commit -m "Week 1: initialize project structure and BFS grid planner"
git push
```

## 阶段完成情况

第一阶段目标：

```text
搭建项目基础结构，创建 Pygame 窗口和 2D 网格画布，实现基础交互。
```

当前已经完成：

```text
Pygame 窗口
网格地图
障碍物添加和删除
起点设置
终点设置
BFS 路径搜索
A* 路径搜索
路径显示
基础项目文档
Git 友好的仓库文件
模块化项目结构
右侧交互 UI 面板
清空地图功能
随机生成障碍物、起点和终点
拖动连续添加或擦除障碍物
无路径状态提示
访问节点显示
路径统计信息
基础机器人路径跟随模拟
```

## 后续改进方向

Week 3 建议按下面顺序继续开发：

1. 把 BFS 访问节点做成逐帧动画，而不是一次性显示。
2. 增加更完整的算法对比视图：连续记录 BFS / A* 多次运行结果。
3. 可选：增加“生成可通行随机地图”，确保随机地图至少存在一条路径。
4. 改进机器人模型：从圆点升级为有朝向的三角形机器人。
5. 加入 PID 控制：控制机器人朝向和运动稳定性。
6. 增加暂停、继续、重置模拟功能。
7. 补充截图、演示视频和项目展示材料。

## 给后续 AI 协作的说明

如果后续使用 AI 继续开发，请先阅读本文档，理解当前状态：

```text
技术路线：Python + Pygame
当前阶段：Week 2 模块化 Pygame 原型
当前核心功能：网格编辑 + 起点终点设置 + BFS/A* 路径规划 + 运行统计 + 基础机器人路径跟随 + 主界面/运行界面
当前代码入口：robot_path_planning/main.py
下一步优先级：BFS/A* 动画、算法对比记录、PID 控制、机器人模型增强
项目最终方向：2D 机器人路径规划与 PID 导航控制仿真平台
```

开发时建议保持小步迭代：每次只新增一个清晰功能，运行成功后再继续下一步。
