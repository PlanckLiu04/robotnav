# RobotNav：可交互的 2D 机器人路径规划与仿真控制平台

## 项目简介

RobotNav 是一个使用 Python + Pygame 开发的二维机器人路径规划与仿真控制项目。

当前项目已经完成第一阶段原型：用户可以在 2D 网格地图中绘制障碍物、设置起点和终点，并使用 BFS 广度优先搜索算法规划路径。

项目最终目标是做成一个适合初学者学习和展示的机器人导航仿真平台，逐步包含地图编辑、路径规划、搜索过程可视化、机器人运动仿真、PID 控制和算法效果对比。

## 当前已实现功能

- 创建 Pygame 2D 窗口。
- 绘制规则网格地图。
- 鼠标点击交互。
- 按 `1` 切换障碍物模式：
  - 点击空白格子添加黑色障碍物。
  - 再次点击黑色格子取消障碍物。
- 按 `2` 切换起点模式：
  - 点击格子设置绿色起点。
  - 起点只有一个，以最后一次设置为准。
- 按 `3` 切换终点模式：
  - 点击格子设置红色终点。
  - 终点只有一个，以最后一次设置为准。
- 按 `Space` 执行 BFS 路径规划：
  - 如果存在可通行路线，会显示蓝色路径。

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
按 Space：执行 BFS 路径规划
关闭窗口：退出程序
```

颜色含义：

```text
浅色格子：可通行区域
黑色格子：障碍物
绿色格子：起点
红色格子：终点
蓝色格子：规划得到的路径
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
└── robot_path_planning/
    ├── main.py
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
robot_path_planning/main.py：当前 Pygame 原型主程序。
robot_path_planning/README.md：早期阶段说明文档，后续可合并到根目录 README。
```

## 当前代码结构

当前阶段为了方便初学者理解，核心代码集中在 `robot_path_planning/main.py`。

主要变量：

```text
WIDTH, HEIGHT：窗口宽度和高度
CELL_SIZE：每个网格单元的像素大小
ROWS, COLS：地图行数和列数
screen：Pygame 绘图窗口
clock：控制刷新率的时钟对象
obstacles：保存障碍物格子的集合
start：保存起点格子
goal：保存终点格子
path：保存 BFS 找到的路径
mode：当前鼠标点击模式
```

主要函数：

```text
draw_grid()：绘制网格线
draw_cell(cell, color)：绘制某一个格子
draw_obstacles()：绘制所有障碍物
get_neighbors(cell)：获取当前格子上下左右的可通行邻居
bfs(start, goal)：使用广度优先搜索寻找路径
```

主循环负责：

```text
读取键盘事件
读取鼠标点击事件
更新当前模式
添加或删除障碍物
设置起点和终点
按空格时执行路径搜索
重新绘制整个窗口
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
Week 2: add interactive map editor
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

## 第一阶段完成情况

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
路径显示
基础项目文档
Git 友好的仓库文件
```

## 后续改进方向

建议按下面顺序继续开发：

1. 增加重置功能：按 `C` 清空障碍物、起点、终点和路径。
2. 增加找不到路径的提示：当 BFS 返回空路径时提示 `No path found`。
3. 可视化 BFS 搜索过程：显示搜索扩散访问过的格子。
4. 实现 A* 算法：加入更有方向感的路径规划方法。
5. 增加路径统计：显示路径长度、访问节点数和搜索耗时。
6. 拆分代码结构：把地图、规划算法、渲染逻辑拆成独立模块。
7. 增加机器人运动仿真：让机器人沿蓝色路径移动。
8. 加入 PID 控制：控制机器人朝向和运动稳定性。
9. 补充截图、演示视频和项目展示材料。

## 给后续 AI 协作的说明

如果后续使用 AI 继续开发，请先阅读本文档，理解当前状态：

```text
技术路线：Python + Pygame
当前阶段：单文件 Pygame 原型
当前核心功能：网格编辑 + 起点终点设置 + BFS 路径规划
当前代码入口：robot_path_planning/main.py
下一步优先级：重置功能、搜索过程可视化、A* 算法、代码模块化
项目最终方向：2D 机器人路径规划与 PID 导航控制仿真平台
```

开发时建议保持小步迭代：每次只新增一个清晰功能，运行成功后再继续下一步。
