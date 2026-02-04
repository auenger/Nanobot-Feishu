# Nanobot 飞书 (Feishu) 配置指南

本指南将帮助您配置 Nanobot 以支持飞书消息收发。

## 1. 准备工作

在配置之前，您需要登录 [飞书开放平台](https://open.feishu.cn/app) 并创建一个自建应用。

### 1.1 创建自建应用
1.  登录 [飞书开放平台](https://open.feishu.cn/app)。
2.  点击 **创建自建应用**。
3.  填写应用名称（例如 "Nanobot"）和描述。
4.  创建完成后，您会自动进入应用详情页。

### 1.2 获取 App ID 和 App Secret
*   在应用详情页左侧菜单，点击 **凭证与基础信息**。
*   复制 **App ID**。
    *   变量名：`FEISHU_APP_ID`
*   复制 **App Secret**。
    *   变量名：`FEISHU_APP_SECRET`

### 1.3 启用机器人能力
1.  在左侧菜单，点击 **添加应用能力**。
2.  选择 **机器人**，并点击添加。

### 1.4 配置权限
1.  在左侧菜单，点击 **权限管理**。
2.  搜索并开通以下权限（非常重要）：
    *   `im:message` (获取与发送单聊、群组消息)
    *   `im:message:send_as_bot` (以应用身份发送消息)
    *   `im:message.group_at_msg` (获取群组中@机器人的消息)
    *   `im:message.p2p_msg` (获取用户发给机器人的单聊消息)
    *   `im:resource` (获取与上传图片或文件资源)
3.  点击 **批量开通**（如果是企业内部开发，可能需要版本发布后由管理员审核通过）。

### 1.5 配置事件订阅 (长连接模式)
这是飞书最棒的功能，不需要公网 IP！

1.  在左侧菜单，点击 **事件与回调**。
2.  点击 **事件配置**。
3.  **订阅方式**：选择 **使用长连接接收事件** (WebSocket)。
    *   (如果不选这个，你就需要配公网 URL，很麻烦)
4.  **添加事件**：
    *   点击“添加事件”。
    *   搜索 `接收消息` (`im.message.receive_v1`)。
    *   点击确认添加。

### 1.6 版本发布与审核
1.  在左侧菜单，点击 **版本管理与发布**。
2.  点击 **创建版本**。
3.  填写版本详情（应用功能截图可以随便截一张）。
4.  点击 **申请发布**。
    *   如果是你是企业管理员，可以自己审核通过。
    *   如果不是，需要联系管理员审核。
    *   *提示：只有发布后的应用，权限才会生效。*

## 2. 配置 Nanobot

您可以通过设置环境变量来启动飞书模式。

### 环境变量列表

| 变量名 | 描述 | 示例 |
|--------|------|------|
| `FEISHU_APP_ID` | 应用 App ID | `cli_a1b2c3d4e5` |
| `FEISHU_APP_SECRET` | 应用 App Secret | `abc123xyz...` |
| `FEISHU_BRIDGE_PORT` | Nanobot Bridge 端口 | `18789` (默认) |

### 启动方式

```bash
cd /Users/ryan/mycode/Nanobot/feishu-openclaw

# 安装依赖 (如果还没装)
npm install

# 启动桥接
export FEISHU_APP_ID="cli_xxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxx"
node bridge.mjs
```

## 3. 下一步

配置完成后，Nanobot 就能通过飞书接收消息了。
飞书的长连接模式 (WebSocket) 不需要您配置任何公网 IP 或回调 URL，启动即可连接。
