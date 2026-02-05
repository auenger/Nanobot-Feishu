# Nanobot-Feishu

这是一个基于原版 [Nanobot](https://github.com/HKUDS/nanobot) 增强的版本，重点增加了对 **飞书 (Lark/Feishu)** 的支持，以及支持**智谱 AI (GLM)** 模型的集成。

## 🌟 主要特性

### 1. 飞书 (Feishu/Lark) 集成
- ✅ 通过 WebSocket 长连接与飞书机器人通信，无需公网 IP
- ✅ 支持接收单聊和群聊消息
- ✅ 自动管理飞书 Bridge 进程
- ✅ 支持 NVM 环境自动检测和切换

### 2. 智谱 AI (GLM) 支持
- ✅ 完整支持智谱 AI 的 GLM 系列模型（glm-4、glm-4-flash、glm-4.7 等）
- ✅ 通过 LiteLLM 统一接口调用
- ✅ 支持 OpenAI 兼容接口
- ✅ 独立配置文件管理 API 密钥

### 3. 配置分离 (Secure Config)
- ✅ 支持从 `feishu.json` 加载飞书配置
- ✅ 支持从 `glm.json` 加载智谱 AI 配置
- ✅ 敏感文件默认被 git 忽略，防止泄露
- ✅ 灵活的配置合并机制

## 📚 文档导航

- **[独立配置指南 (Separate Configuration Guide)](SEPARATE_CONFIG_GUIDE_CN.md)** 🔴 **(推荐阅读)**  
  详细介绍如何配置飞书和 GLM，包括配置文件格式、字段说明和启动方式

- **[原版项目说明 (Original README)](NANOBOT_README.md)**  
  Nanobot 原项目的完整说明文档

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -e .

# 安装 Bridge 依赖（需要 Node.js 20+）
cd bridge
npm install
npm run build
cd ..
```

### 2. 配置文件

在 `~/.nanobot/` 目录下创建配置文件：

#### 主配置文件 `config.json`

**方式一：使用 GLM 的 Anthropic 兼容接口（推荐，无需额外文件）**

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/glm-4.7",
      "workspace": "~/.nanobot/workspace"
    }
  },
  "providers": {
    "anthropic": {
      "apiKey": "your_zhipu_api_key.xxxxxxxx",
      "apiBase": "https://open.bigmodel.cn/api/anthropic"
    }
  }
}
```

**方式二：使用分离配置文件（适合需要隔离敏感信息的场景）**

`config.json`:
```json
{
  "agents": {
    "defaults": {
      "model": "openai/glm-4.7",
      "workspace": "~/.nanobot/workspace"
    }
  }
}
```

`glm.json`（单独创建，git 会自动忽略）:
```json
{
  "api_key": "your_zhipu_api_key.xxxxxxxx",
  "api_base": "https://open.bigmodel.cn/api/paas/v4/"
}
```

#### 飞书配置 `feishu.json`（可选）

如果需要使用飞书集成：

```json
{
  "app_id": "cli_xxxxxxxxxx",
  "app_secret": "your_app_secret",
  "verification_token": "your_verification_token",
  "encrypt_key": "your_encrypt_key",
  "enabled": true
}
```

> **提示**：详细的配置说明请参考 [独立配置指南](SEPARATE_CONFIG_GUIDE_CN.md)

### 3. 启动服务

```bash
nanobot gateway
```

## 🔧 技术改进

### Python 核心修改

1. **`nanobot/config/schema.py`**
   - 新增 `FeishuConfig` 类
   - 新增 `zhipu` provider 配置

2. **`nanobot/providers/litellm_provider.py`**
   - 修复智谱 AI 模型识别逻辑
   - 支持 `zhipu`、`glm`、`zai` 等模型前缀
   - 正确设置 `ZHIPUAI_API_KEY` 环境变量

3. **`nanobot/channels/feishu.py`** (新增)
   - 实现飞书通道逻辑
   - 支持 NVM 环境检测
   - 连接重试机制

### Bridge 修改

1. **`bridge/src/feishu.ts`** (新增)
   - 飞书 WebSocket 客户端实现
   - 消息接收和转发

2. **`bridge/src/server.ts`**
   - 集成 FeishuManager

## 📝 更新日志

### 2026-02-05
- ✅ 修复智谱 AI 模型识别问题
- ✅ 优化 LiteLLM provider 配置逻辑
- ✅ 完善配置文档

### 2026-02-04
- ✅ 添加飞书集成支持
- ✅ 实现配置文件分离
- ✅ 添加智谱 AI 支持

## 📄 许可证

本项目基于原版 Nanobot 项目，遵循相同的开源许可证。

## 🙏 致谢

感谢 [Nanobot](https://github.com/HKUDS/nanobot) 原项目团队的优秀工作。
