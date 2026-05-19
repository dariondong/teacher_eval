# 教师教学评价系统

基于 Flask 的教师教学评价系统，支持学生在线评价、管理员后台管理、数据统计与导出。

## 技术栈

- **后端**: Python 3.12 + Flask + SQLAlchemy
- **前端**: 原生 HTML/CSS/JavaScript（无前端框架依赖）
- **数据库**: SQLite
- **导出**: openpyxl (Excel)
- **部署**: Docker

## 功能

### 学生端

- **评价问卷**: 20 道选择题（A-E 五档评分），逐题作答，支持上下题导航、键盘方向键、选中自动跳下一题
- **基本信息**: 选择年级 → 班级 → 学科，级联下拉框
- **预览提交**: 提交前可预览所有答案与总分
- **设备标识**: 通过 localStorage 生成 UUID，同一设备可重复评价不同学科教师，重新提交覆盖原记录

### 管理端 (`/admin/login`)

| 功能 | 路径 |
|------|------|
| 仪表盘 | `/admin` |
| 评价记录 | `/admin/results` |
| 统计分析 | `/admin/stats` |
| 题目管理 | `/admin/questions` |
| 班级配置 | `/admin/classes` |
| 管理员管理 | `/admin/admins` |
| 数据导出 | `/admin/export` |
| 修改密码 | `/admin/password` |

### 数据导出

- **全部导出**: `/admin/export` — Excel 含评价明细、统计汇总、题目配置、班级配置 4 个 Sheet
- **筛选导出**: `/admin/export/filtered?grade=高一&cls=1&subject=数学` — 按条件筛选导出

### 压力测试

- `stress_test.py` 支持并发压测

## 快速开始

### 方式一：直接运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（首次自动初始化数据库）
python app.py

# 访问 http://localhost:5000
# 管理端 http://localhost:5000/admin/login  账号 admin / 密码 admin123
```

### 方式二：Docker

```bash
docker build -t teacher-eval .
docker run -d -p 5000:5000 --name teacher-eval teacher-eval
```

### 方式三：Docker Compose（推荐）

创建 `docker-compose.yml`：

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./instance:/app/instance
    environment:
      - SECRET_KEY=your-secret-key
    restart: always
```

```bash
docker-compose up -d
```

## 默认管理员

| 用户名 | 密码 |
|--------|------|
| admin  | admin123 |

请在首次登录后修改密码。

## API 接口

| 接口 | 说明 |
|------|------|
| `GET /api/grades` | 获取年级列表 |
| `GET /api/classes/<grade>` | 获取某年级班级列表 |
| `GET /api/questions` | 获取问卷题目 |
| `GET /api/my-evaluation?uuid=<uuid>` | 查询某设备的评价记录 |

## 配置项

- **环境变量 `SCHOOL_NAME`**: 学校名称（默认 `实验中学`）
- **环境变量 `SECRET_KEY`**: 会话密钥（默认 `gaozhou-erzhong-eval-secret-2026`）
- **数据库**: 默认使用 `instance/evaluation.db`（SQLite）
- **题目评分**: A-5分, B-4分, C-3分, D-2分, E-1分，满分100分（20题×5分）

## 压力测试

```bash
python stress_test.py --url http://localhost:5000 --count 200 --concurrent 20
```

参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--url` | `https://wed.theez.top/` | 目标地址 |
| `--count` | 100 | 总请求数 |
| `--concurrent` | 10 | 并发线程数 |

## 项目结构

```
teacher_eval/
├── app.py                     # Flask 应用主入口
├── models.py                  # 数据模型 (Admin, Evaluation, ClassConfig, QuestionConfig)
├── requirements.txt           # Python 依赖
├── Dockerfile                 # Docker 构建文件
├── stress_test.py             # 压力测试工具
├── templates/                 # 前端模板
│   ├── survey_original.html   # 学生评价问卷
│   ├── success.html           # 提交成功页面
│   ├── base.html              # 管理端基础布局
│   └── admin/                 # 管理端页面
├── static/                    # 静态资源
└── instance/                  # 数据库文件（自动生成）
```
