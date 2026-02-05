# Nanobot Enhanced Version (Feishu & Separate Config)

这是一个基于原版 [Nanobot](https://github.com/HKUDS/nanobot) 增强的版本，重点增加了对 **[飞书 (Lark/Feishu)](https://www.feishu.cn/)** 的支持，以及支持**配置文件分离**（将敏感信息分离存储），方便团队协作和代码管理。

This is an enhanced version of [Nanobot](https://github.com/HKUDS/nanobot) with added support for **Feishu/Lark** and **modular configuration** files.

## 📚 文档索引 (Documentation)

### 1. 核心指南 (Key Guides)

*   **[独立配置指南 (Separate Configuration Guide)](SEPARATE_CONFIG_GUIDE_CN.md)**  
    🔴 **(推荐阅读 / Recommended)**  
    详细介绍了如何将飞书凭证和 GLM/Zhipu Key 拆分到 `feishu.json` 和 `glm.json` 中，以及如何启动增强版服务。

*   **[飞书配置指南 (Feishu Setup Guide)](FEISHU_CONFIG_GUIDE.md)**  
    详细介绍了如何在飞书开放平台创建应用、获取 App ID/Secret 以及配置权限。

*   **[飞书 Markdown 富文本支持 (Feishu Markdown Support)](FEISHU_MARKDOWN.md)**  
    介绍如何使用飞书的富文本卡片功能，让 AI 回复的 Markdown 格式自动渲染为精美卡片。

### 2. 原版文档 (Original Documentation)

*   **[原版项目说明 (Original README)](NANOBOT_README.md)**  
    Nanobot 原项目的完整说明文档，包含架构介绍、基础安装、Docker 部署等信息。

## ✨ 主要增强功能 (Key Enhancements)

1.  **飞书 (Feishu/Lark) 集成**: 
    - 支持通过 WebSocket 长连接与飞书机器人通信，无需公网 IP。
    - 支持接收单聊和群聊消息。
    - **🎨 Markdown 富文本支持**：AI 回复的 Markdown 格式会自动渲染为精美的卡片消息。
    - **🖼️ 图片消息处理**：正确解析和传递图片消息中的 `image_key`。
2.  **配置分离 (Secure Config)**:
    - 支持从 `feishu.json` 加载飞书配置。
    - 支持从 `glm.json` 加载智谱 AI (GLM) 配置。
    - 这些敏感文件默认被 git 忽略，防止泄露。
    - 支持自定义 Bridge 端口配置。

## 🚀 快速开始 (Quick Start)

1.  **安装**:
    ```bash
    pip install -e .
    ```

2.  **配置**:
    参考 [独立配置指南](SEPARATE_CONFIG_GUIDE_CN.md) 创建配置文件。

3.  **启动**:
    ```bash
    nanobot gateway
    ```
