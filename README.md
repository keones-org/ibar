# ibar

LLM Playground — 一个交互式大语言模型实验平台，可通过 Web 界面与 DeepSeek AI 模型进行交互。

## 项目概述

ibar 提供了一个简洁的 Web 界面，让用户无需处理复杂的 API 集成即可体验 LLM 的能力。支持两种模式：

- **Completion 模式**: 提供 prompt，模型生成续写内容
- **Fill-in-Middle (FIM) 模式**: 提供前缀和后缀，模型生成中间填充内容

用户可通过界面调节 `temperature`（随机性）和 `max_tokens`（最大长度）等参数。

## 技术栈

### 前端 (`frontend/llm-playground-ui`)

- **框架**: React 18 + TypeScript
- **UI 组件**: shadcn/ui（基于 Radix UI）
- **构建工具**: Vite
- **样式**: Tailwind CSS

### 后端 (`backend/llm-playground-api`)

- **框架**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **HTTP 客户端**: httpx（异步请求）
- **数据校验**: Pydantic v2
- **配置管理**: pydantic-settings
- **依赖管理**: Poetry

## 项目结构

```
ibar/
├── frontend/
│   └── llm-playground-ui/
│       ├── src/
│       │   ├── App.tsx              # 主应用组件（状态管理、API 调用、UI）
│       │   ├── components/ui/       # shadcn/ui 组件
│       │   └── assets/              # 静态资源
│       └── .env.example             # 前端环境变量模板
│
├── backend/
│   └── llm-playground-api/
│       ├── app/
│       │   ├── main.py              # FastAPI 应用、路由端点
│       │   ├── models.py            # Pydantic 请求/响应模型
│       │   ├── config.py            # 环境变量配置
│       │   └── __init__.py
│       ├── .env.example             # 后端环境变量模板
│       └── README.md                # 后端 API 详细文档
│
└── README.md                        # 本文件
```

## 快速开始

### 环境要求

- Node.js >= 18
- Python >= 3.9
- Poetry（Python 依赖管理）

### 后端启动

```bash
cd backend/llm-playground-api

# 安装依赖
poetry install

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DeepSeek API Key

# 启动开发服务器
poetry run uvicorn app.main:app --reload
```

后端默认运行在 http://localhost:8000

### 前端启动

```bash
cd frontend/llm-playground-ui

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.local
# 设置 VITE_API_URL=http://localhost:8000

# 启动开发服务器
npm run dev
```

前端默认运行在 http://localhost:5173

## API 接口

| 方法   | 路径               | 说明               |
| ------ | ------------------ | ------------------ |
| `GET`  | `/healthz`         | 健康检查           |
| `GET`  | `/api/models`      | 获取可用模型列表   |
| `POST` | `/api/completions` | 生成文本补全       |

### 生成补全请求示例

**Completion 模式：**
```bash
curl -X POST http://localhost:8000/api/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "prompt": "Hello!",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

**FIM 模式：**
```bash
curl -X POST http://localhost:8000/api/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "prefix": "def greet():",
    "suffix": "# End of function",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

### 响应格式

```json
{
  "text": "生成的文本内容",
  "model": "deepseek-chat"
}
```

## 环境变量

### 后端

| 变量                     | 说明                      | 默认值                      |
| ------------------------ | ------------------------- | --------------------------- |
| `DEEPSEEK_API_KEY`       | DeepSeek API 密钥         | （必填）                    |
| `DEEPSEEK_API_BASE_URL`  | DeepSeek API 基础 URL     | `https://api.deepseek.com`  |

### 前端

| 变量            | 说明              | 默认值                    |
| --------------- | ----------------- | ------------------------- |
| `VITE_API_URL`  | 后端 API 地址     | `http://localhost:8000`   |

> **注意**: 未配置 API Key 时，后端会返回 mock 响应，方便开发调试。

## 更多文档

- 后端 API 详细文档：[backend/llm-playground-api/README.md](backend/llm-playground-api/README.md)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs)
