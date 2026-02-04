# Nanobot 独立配置指南

为了方便管理敏感信息，避免频繁修改主项目代码，我们对 `Nanobot` 进行了增强，支持将 **飞书 (Feishu)** 和 **智谱 GLM (ZhipuAI)** 的配置拆分到单独的 JSON 文件中。

## 1. 配置文件存放位置

默认情况下，Nanobot 的配置文件位于用户主目录下的 `.nanobot` 文件夹中。
请确保以下新增的配置文件与您的主配置文件 `config.json` 位于同一目录。

**通常路径:**
- macOS/Linux: `~/.nanobot/`
- Windows: `C:\Users\YourUsername\.nanobot\`

## 2. 飞书 (Feishu) 独立配置

在配置目录下创建一个名为 `feishu.json` 的文件。

**文件内容示例 (`feishu.json`):**

```json
{
  "app_id": "cli_a1b2c3d4e5",
  "app_secret": "your_app_secret_here",
  "verification_token": "your_verification_token_here",
  "encrypt_key": "your_encrypt_key_here",
  "enabled": true
}
```

或者，如果你喜欢嵌套的结构（与主 config 保持一致），也可以这样写：

```json
{
  "feishu": {
    "app_id": "cli_a1b2c3d4e5",
    "app_secret": "your_app_secret_here",
    "verification_token": "your_verification_token_here",
    "encrypt_key": "your_encrypt_key_here",
    "enabled": true
  }
}
```

> **注意**: 如果 `feishu.json` 存在，它将自动覆盖 `config.json` 中 `config.channels.feishu` 的相关设置。

## 3. 智谱 GLM (ZhipuAI) 独立配置

在配置目录下创建一个名为 `glm.json` 的文件。

**文件内容示例 (`glm.json`):**

```json
{
  "api_key": "your_zhipu_api_key_here",
  "api_base": "https://open.bigmodel.cn/api/paas/v4/"
}
```

同样支持嵌套结构：

```json
{
  "zhipu": {
    "api_key": "your_zhipu_api_key_here",
    "api_base": "https://open.bigmodel.cn/api/paas/v4/"
  }
}
```

> **注意**: 加载程序会将 `glm.json` 的内容映射到 `config.providers.zhipu`。

### 关于模型名称 (Model Name)
`glm.json` 仅用于配置 **API 连接凭证** (API Key / Base URL)，它**不**决定 Nanobot 当前使用的模型。

如果您希望 Nanobot 默认使用特定模型（例如 `glm-4-flash` 或 `glm-4.7`），您需要修改主配置文件 `config.json`（**注意：不是在 `glm.json` 中修改**）。

**在 `config.json` 中修改默认模型的示例：**

```json
{
  "agents": {
    "defaults": {
      "model": "openai/glm-4.7" 
    }
  }
}
```

> **说明**: 
> 1. 上述配置位于 `config.json` 的根对象下。
> 2. `"model"` 的值可以是任何支持的模型名称。如果您使用的是 GLM 的 OpenAI 兼容接口，建议使用 `openai/模型名称` 的格式（如 `openai/glm-4.7`, `openai/glm-4`）。
> 3. 修改后重启 Nanobot 生效。

## 4. 字段说明

### 飞书配置字段
- **verification_token**: 用于飞书开放平台验证请求来源的合法性（在“事件订阅”中查看）。
- **encrypt_key**: 如果您在飞书后台开启了“加密策略”，则必须填写此 Key 用于解密消息；如未开启，可设为空字符串。

### 智谱 GLM 配置字段
- **api_key**: 您的智谱 AI API Key。
- **api_base**: API 基础路径，通常为 `https://open.bigmodel.cn/api/paas/v4/`。
- **(不需要在此处配置模型名称)**: 模型选择由 Agent 配置决定。

## 5. 安全说明

我们已经更新了项目的 `.gitignore` 文件，默认忽略了以下文件，防止您不小心将包含敏感密钥的配置提交到 git 仓库：

- `feishu.json`
- `glm.json`

## 6. 启动说明

### 如何启动飞书连接
配置完成后，您只需要正常启动 Nanobot 的 Gateway 服务即可：

```bash
nanobot gateway
```

系统会自动读取 `feishu.json`，如果 `enabled` 为 `true`，则会尝试加载并启动飞书通道。

> **关于 `nanobot channels login`**: 
> - 该命令 **仅用于 WhatsApp** (需要扫描二维码登录)。
> - 飞书使用的是 **App ID / Secret** 认证，不需要扫码登录，因此**不需要**运行此命令。
> - 只要配置正确并启动 `gateway`，飞书机器人就会上线。


## 5. 项目修改清单 (File Changes)

为了实现上述功能，我们对原项目进行了以下最小化修改。如果您需要合并代码，请关注以下文件：

### Python (Nanobot Core)
1.  **`nanobot/config/schema.py`**:
    *   新增 `FeishuConfig` 类。
    *   在 `ChannelsConfig` 中注册 `feishu` 字段。
2.  **`nanobot/config/loader.py`**:
    *   修改 `load_config` 函数，增加从 `feishu.json` 和 `glm.json` 合并配置的逻辑。
3.  **`nanobot/channels/feishu.py`** (新增):
    *   实现了 Python 端的飞书通道逻辑。
    *   **关键逻辑说明 (NVM Support)**:
        *   在自动拉起 Bridge 进程时，会自动检测用户是否安装了 `nvm` (检查 `~/.nvm/nvm.sh`)。
        *   如果存在 `nvm`，会通过 `bash -c "source ~/.nvm/nvm.sh && nvm use 20 && npm start"` 启动。
        *   这确保了即使系统 `node` 版本较旧，只要安装了 `nvm`，程序也能切换到 Node 20 环境运行。如果您使用其他版本管理工具（如 `fnm` 或 `n`），可能需要在此处修改代码。
    *   **修复**: 增加了连接重试逻辑（Retries），解决启动时的竞态问题。
4.  **`nanobot/channels/manager.py`**:
    *   在 `_init_channels` 中增加了飞书通道的初始化代码。
    *   **优化**: 增加了互斥逻辑，当飞书启用时强制禁用 WhatsApp 通道，防止端口冲突。
5.  **`nanobot/providers/litellm_provider.py`**:
    *   **修复**: 修正了智谱 AI (GLM) 的识别逻辑，防止因误判为 vLLM 而导致 API 调用失败 (401 Auth Error)。
    *   优化了模型名称前缀处理（自动通过 `openai/` 协议调用智谱 V4 接口）。

### TypeScript / Node.js (Bridge)
1.  **`bridge/package.json`**:
    *   增加了依赖 `"@larksuiteoapi/node-sdk": "^1.24.0"`。
2.  **`bridge/src/feishu.ts`** (新增):
    *   实现了飞书 WebSocket 客户端逻辑。
3.  **`bridge/src/server.ts`**:
    *   集成了 `FeishuManager`，在 Bridge 启动时同时连接飞书。

---

## 6. 快速开始 (Quick Start)

1.  **停止旧服务**:
    如果您正在运行旧的 nanobot 进程，请先将其停止（Ctrl+C 或 kill）。

2.  **准备配置文件**:
    在 `~/.nanobot/` 目录下创建 `feishu.json` 和 `glm.json`，填入您的 Key。
    *(参考本文第 2、3 节的格式)*

3.  **重新编译 Bridge**:
    由于修改了 Bridge 代码，需要重新安装依赖并编译：
    ```bash
    cd nanobot/bridge
    # 确保使用 Node 20+
    nvm use 20 
    npm install
    npm run build
    ```

4.  **启动主程序**:
    回到项目根目录，启动 Gateway：
    ```bash
    nanobot gateway
    ```
    观察日志，如果看到 `Feishu channel enabled` 和 `Initializing Feishu Bridge`，即表示成功。
