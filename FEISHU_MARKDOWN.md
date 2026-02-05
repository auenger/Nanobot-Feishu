# 飞书 Markdown 富文本支持

## 功能说明

Nanobot 现在支持在飞书中自动渲染 Markdown 格式的消息！当 AI 回复包含 Markdown 格式时，会自动以富文本卡片的形式展示，提供更好的阅读体验。

## 支持的 Markdown 语法

系统会自动检测以下 Markdown 格式，并将其渲染为飞书卡片：

### 1. 标题
```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 2. 文本样式
```markdown
**粗体文本**
*斜体文本*
`行内代码`
```

### 3. 代码块
````markdown
```python
def hello():
    print("Hello, World!")
```
````

### 4. 列表
```markdown
- 无序列表项 1
- 无序列表项 2

1. 有序列表项 1
2. 有序列表项 2
```

### 5. 链接
```markdown
[链接文本](https://example.com)
```

### 6. 引用
```markdown
> 这是一段引用文本
```

## 工作原理

1. **自动检测**：系统会检查 AI 回复的内容是否包含 Markdown 格式
2. **智能发送**：
   - 如果包含 Markdown → 发送为 `interactive` 卡片消息（支持富文本渲染）
   - 如果是纯文本 → 发送为普通 `text` 消息
3. **容错处理**：如果卡片发送失败，会自动降级为普通文本消息

## 实现细节

### 消息类型

- **普通文本消息**：`msg_type: 'text'`
- **富文本卡片**：`msg_type: 'interactive'`

### 卡片结构

```json
{
  "config": {
    "wide_screen_mode": true
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "你的 Markdown 内容"
    }
  ]
}
```

## 使用示例

### 示例 1：代码解释

**用户问**：如何用 Python 读取文件？

**AI 回复**（自动渲染为卡片）：
```markdown
# Python 文件读取

你可以使用以下方法：

## 方法 1：使用 open()
```python
with open('file.txt', 'r') as f:
    content = f.read()
    print(content)
```

## 方法 2：逐行读取
```python
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())
```

**注意**：记得使用 `with` 语句来自动关闭文件！
```

### 示例 2：列表说明

**用户问**：Python 的优点有哪些？

**AI 回复**（自动渲染为卡片）：
```markdown
## Python 的主要优点

1. **简洁易读**：语法简单，接近自然语言
2. **丰富的库**：拥有大量第三方库
3. **跨平台**：可在多个操作系统上运行
4. **社区活跃**：有庞大的开发者社区

适用场景：
- Web 开发
- 数据分析
- 机器学习
- 自动化脚本
```

## 重启服务

修改代码后，需要重启 bridge 服务才能生效：

```bash
# 如果 bridge 是独立运行的
cd ~/.nanobot/bridge
npm start

# 如果是通过 nanobot 自动启动的
# 重启 nanobot 服务即可
```

## 注意事项

1. **权限要求**：确保飞书应用有发送消息卡片的权限
2. **内容限制**：消息内容不能超过 30KB
3. **兼容性**：飞书 Markdown 支持的语法可能与标准 Markdown 略有差异

## 调试

查看日志中的标识：
- `[Feishu] ✅ Sent Markdown card` - 成功发送卡片
- `[Feishu] Send Markdown card error` - 卡片发送失败，尝试降级

## 参考文档

- [飞书富文本组件文档](https://open.feishu.cn/document/feishu-cards/card-json-v2-components/content-components/rich-text)
- [飞书消息发送 API](https://open.feishu.cn/document/server-docs/im-v1/message/create)
