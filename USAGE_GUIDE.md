# Nanobot 操作指南

本指南将帮助您快速上手 Nanobot 个人 AI 助手。

## 🚀 启动服务

### 1. 激活环境
请确保您已进入项目目录并激活虚拟环境：

```bash
cd Nanobot
source .venv/bin/activate
```

### 2. 启动飞书桥接器 (Feishu Bridge)
如果您配置了飞书集成，请开启 Bridge 服务以接收消息：

```bash
nanobot channels start
```
*首次运行会提示配置飞书 App ID 和 Secret。*

### 3. 启动核心网关 (Gateway)
启动主服务，处理消息调度和 AI 逻辑：

```bash
nanobot gateway
```

---

## 💬 命令行聊天
除了使用飞书，您也可以直接在命令行与 Agent 交互：

**交互模式:**
```bash
nanobot agent
```

**单指令模式:**
```bash
nanobot agent -m "你好，请介绍一下你自己"
```

## ⚙️ 配置说明

配置文件位于 `~/.nanobot/config.json`。

**智谱 GLM-4 配置示例:**
```json
"providers": {
  "openai": {
    "apiKey": "YOUR_ZHIPU_KEY",
    "apiBase": "https://open.bigmodel.cn/api/paas/v4"
  }
},
"agents": {
  "defaults": {
    "model": "openai/glm-4-flash"
  }
}
```

## 📂 目录说明
- **项目根目录**: 您 clone 下来的 `Nanobot` 文件夹
- **配置与工作区**: `~/.nanobot/` (包含 config.json、Bridge 配置及 AI 生成的文件)
