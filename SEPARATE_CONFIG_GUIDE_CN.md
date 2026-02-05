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

### 如何获取智谱 AI API Key

1. **注册账号**  
   访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)，注册并登录账号。

2. **创建 API Key**  
   - 登录后进入控制台
   - 点击"API Keys"或"密钥管理"
   - 点击"创建新的 API Key"
   - 复制生成的 API Key（格式类似：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxx`）

3. **充值余额**  
   - 智谱 AI 采用按量计费模式
   - 需要在账户中充值才能使用 API
   - 建议先充值小额测试（如 10 元）

### 支持的 GLM 模型

智谱 AI 提供多个模型，以下是常用模型列表：

| 模型名称 | 说明 | 推荐用途 |
|---------|------|---------|
| `glm-4` | GLM-4 标准版 | 通用对话和任务 |
| `glm-4-flash` | GLM-4 快速版 | 快速响应场景 |
| `glm-4.7` | GLM-4.7 版本 | 高性能对话 |
| `glm-4-air` | GLM-4 轻量版 | 成本敏感场景 |
| `glm-4-airx` | GLM-4 Air 增强版 | 平衡性能和成本 |

### 完整配置示例

#### 方式一：使用 OpenAI 兼容接口（推荐）

在 `~/.nanobot/config.json` 中配置：

```json
{
  "agents": {
    "defaults": {
      "model": "openai/glm-4.7",
      "workspace": "~/.nanobot/workspace",
      "max_tokens": 8192,
      "temperature": 0.7
    }
  }
}
```

在 `~/.nanobot/glm.json` 中配置：

```json
{
  "api_key": "your_zhipu_api_key_here.xxxxxxxx",
  "api_base": "https://open.bigmodel.cn/api/paas/v4/"
}
```

#### 方式二：使用 LiteLLM 原生支持

在 `~/.nanobot/config.json` 中配置：

```json
{
  "agents": {
    "defaults": {
      "model": "zhipu/glm-4",
      "workspace": "~/.nanobot/workspace"
    }
  }
}
```

在 `~/.nanobot/glm.json` 中配置：

```json
{
  "api_key": "your_zhipu_api_key_here.xxxxxxxx"
}
```

#### 方式三：使用 GLM 的 Anthropic 兼容接口（推荐，无需 glm.json）

智谱 AI 提供了 Anthropic 兼容接口，可以直接在 `config.json` 中配置，**无需创建 `glm.json` 文件**。

在 `~/.nanobot/config.json` 中配置：

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot/workspace",
      "model": "anthropic/glm-4.7",
      "maxTokens": 8192,
      "temperature": 0.7,
      "maxToolIterations": 20
    }
  },
  "channels": {
    "whatsapp": {
      "enabled": true,
      "bridgeUrl": "ws://localhost:3001",
      "allowFrom": []
    },
    "telegram": {
      "enabled": false,
      "token": "",
      "allowFrom": []
    }
  },
  "providers": {
    "anthropic": {
      "apiKey": "your_zhipu_api_key_here.xxxxxxxx",
      "apiBase": "https://open.bigmodel.cn/api/anthropic"
    },
    "openai": {
      "apiKey": ""
    }
  }
}
```

**优点：**
- ✅ 配置更简洁，所有配置在一个文件中
- ✅ 使用 Anthropic 兼容接口，兼容性好
- ✅ 支持所有 GLM 模型（glm-4、glm-4-flash、glm-4.7 等）
- ✅ 无需额外的 `glm.json` 文件

**注意事项：**
- 模型名称使用 `anthropic/` 前缀（如 `anthropic/glm-4.7`）
- `apiBase` 设置为 `https://open.bigmodel.cn/api/anthropic`
- API Key 直接配置在 `providers.anthropic.apiKey` 中

### 常见问题

**Q: 三种配置方式应该选择哪一种？**  
A: 推荐选择：
1. **方式三（Anthropic 兼容接口）** - 最推荐，配置简单，无需额外文件，兼容性好
2. **方式一（OpenAI 兼容接口）** - 适合需要分离敏感配置的场景
3. **方式二（LiteLLM 原生）** - 适合对 LiteLLM 熟悉的用户

**Q: 使用 Anthropic 兼容接口时，是否需要创建 glm.json？**  
A: **不需要**。如果使用方式三（`anthropic/glm-4.7` + `apiBase: https://open.bigmodel.cn/api/anthropic`），直接在 `config.json` 中配置即可，不要创建 `glm.json` 文件。

**Q: 为什么会出现 401 认证错误？**  
A: 请检查：
1. API Key 是否正确复制（注意不要有多余空格）
2. 账户余额是否充足
3. API Key 是否已激活
4. 如果使用 Anthropic 兼容接口，确认 `apiBase` 是否正确设置为 `https://open.bigmodel.cn/api/anthropic`

**Q: 如何切换不同的 GLM 模型？**  
A: 修改 `config.json` 中的 `agents.defaults.model` 字段，例如：
- 使用 Anthropic 兼容接口：
  - `"anthropic/glm-4"` - 使用 GLM-4 标准版
  - `"anthropic/glm-4-flash"` - 使用 GLM-4 快速版
  - `"anthropic/glm-4.7"` - 使用 GLM-4.7 版本
- 使用 OpenAI 兼容接口：
  - `"openai/glm-4"` - 使用 GLM-4 标准版
  - `"openai/glm-4-flash"` - 使用 GLM-4 快速版
  - `"openai/glm-4.7"` - 使用 GLM-4.7 版本

**Q: glm.json 和 config.json 中的配置有什么区别？**  
A: 
- `glm.json` - 存储敏感的 API 凭证（API Key、API Base），不会提交到 git（仅在使用方式一或方式二时需要）
- `config.json` - 存储非敏感的配置（模型名称、温度参数等），可以提交到 git
- 如果使用方式三（Anthropic 兼容接口），则只需要 `config.json`，不需要 `glm.json`

**Q: 是否必须使用 `openai/` 或 `anthropic/` 前缀？**  
A: 
- 使用 **Anthropic 兼容接口**时，必须使用 `anthropic/` 前缀（如 `anthropic/glm-4.7`）
- 使用 **OpenAI 兼容接口**时，推荐使用 `openai/` 前缀（如 `openai/glm-4.7`）
- 使用 **LiteLLM 原生支持**时，可以使用 `zhipu/` 前缀或直接使用模型名称


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
