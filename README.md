# Nanobot (Feishu Edition)

这是一个轻量级、智能化的个人 AI 助手项目。本项目经过定制，已完美支持 **飞书 (Feishu/Lark)** 作为主要交互渠道，并默认接入 **智谱 GLM-4** 等高性能大模型。

您可以将它部署在本地电脑或服务器上，通过飞书与您的 AI 助手随时随地进行对话。

有关原版项目的详细英文文档，请参考 [NANOBOT_README.md](./NANOBOT_README.md)。

---

## ✨ 核心特性

*   **飞书原生集成**：无需公网 IP，通过 WebSocket 长连接实现极其稳定的消息收发。
*   **多模型支持**：默认配置支持 OpenAI 格式接口（推荐使用智谱 GLM-4），同时也支持 Anthropic, Gemini 等。
*   **隐私安全**：代码与数据完全运行在您的掌控之中。
*   **简单易用**：提供了便捷的 CLI 命令来管理和启动服务。

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装：
*   **Python 3.10+**
*   **Node.js 18+** (用于运行飞书 Bridge)

### 2. 安装项目

```bash
# 克隆项目
git clone <your-repo-url>
cd Nanobot

# 创建并激活 Python 虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e .
```

### 3. 配置模型 (GLM-4)

编辑配置文件 `~/.nanobot/config.json`（如果没有则运行 `nanobot onboard` 生成）。

找到 `providers.openai` 部分（因为智谱兼容 OpenAI 格式），填入您的 Key：

```json
"openai": {
  "apiKey": "您的_智谱_API_KEY",
  "apiBase": "https://open.bigmodel.cn/api/paas/v4"
}
```

同时确保 `agents.defaults.model` 设置正确：
```json
"defaults": {
  "model": "openai/glm-4.7", 
  ...
}
```
*(注：`openai/` 前缀是必须的，代表使用 OpenAI 兼容协议调用)*

### 4. 配置飞书 (Feishu/Lark)

**第一步：创建飞书应用**
1.  前往 [飞书开放平台](https://open.feishu.cn/app)。
2.  创建企业自建应用，获取 **App ID** 和 **App Secret**。
3.  **开启机器人能力**。
4.  **权限配置**：开通 `im:message` (接收消息), `im:resource` (获取资源) 等权限。
5.  **事件订阅**：在“事件与回调”中，配置为 **“使用长连接”**，并添加 `im.message.receive_v1` 事件。
6.  **发布版本**：创建版本并发布，确保应用处于可用状态。
7.  *详细步骤请参考项目内的 [FEISHU_CONFIG_GUIDE.md](./FEISHU_CONFIG_GUIDE.md)*。

**第二步：启动 Bridge**
使用我们为您准备的快捷命令：

```bash
nanobot channels start
```
*首次运行会提示您输入 App ID 和 Secret，输入后会自动保存。*

**第三步：配置白名单**
为了防止他人滥用，您需要在 `~/.nanobot/config.json` 中将您的飞书 OpenID 加入白名单：

```json
"channels": {
  "whatsapp": {  // 注意：这里保留了 whatsapp 字段名以兼容旧配置，实际为通用 Bridge
    "enabled": true,
    "bridgeUrl": "ws://localhost:3001",
    "allowFrom": [
        "ou_xxxxxxxxxxxxxx" // 您的飞书 OpenID (在 Bridge 日志中可以看到)
    ]
  }
}
```

### 5. 启动主服务

在新的终端窗口中运行：

```bash
nanobot gateway
```

现在，您可以在飞书上给您的机器人发消息了！🎉

---

## 🛠️ 常用命令

*   **`nanobot gateway`**: 启动 AI 核心服务。
*   **`nanobot channels start`**: 启动飞书 Bridge (连接器)。
*   **`nanobot agent -m "你好"`**: 在命令行直接测试 AI 回复。
*   **`nanobot status`**: 查看当前配置状态。

## 📂 目录结构

*   `nanobot/`: Python 核心代码
*   `bridge/`: Node.js 桥接服务 (处理飞书/WebSocket 连接)
*   `FEISHU_CONFIG_GUIDE.md`: 详细的飞书后台配置图文指南
