# 📱 飞书双向互动配置指南

**让健康管家能够接收并回复你的消息！**

---

## 🎯 配置步骤（10-15 分钟）

### 第 1 步：创建飞书应用（5 分钟）

1. **访问飞书开放平台**
   ```
   https://open.feishu.cn/app
   ```

2. **登录飞书账号**
   - 用你的飞书账号登录

3. **创建企业自建应用**
   - 点击"创建应用"
   - 选择"企业自建"
   - 填写应用信息：
     - 应用名称：`健康管家`
     - 应用图标：随便选一个
   - 点击"确定"

4. **复制 App ID 和 App Secret**
   - 进入应用管理页面
   - 找到"凭证"部分
   - 复制：
     - **App ID**（格式：`cli_xxxxxxxxxxxxx`）
     - **App Secret**（一串字符）

---

### 第 2 步：添加机器人（3 分钟）

1. **进入应用 → 添加机器人**
   - 在应用管理页面
   - 点击左侧"添加机器人"
   - 点击"创建机器人"

2. **填写机器人信息**
   - 名称：`健康管家`
   - 描述：`你的专属健康管理助手`
   - 头像：随便选

3. **复制机器人信息**
   - 复制 **Verification Token**
   - 保存好

---

### 第 3 步：配置权限（2 分钟）

1. **进入应用 → 权限管理**
   - 点击"权限管理"

2. **添加以下权限**
   ```
   ✅ 获取用户信息
   ✅ 发送消息
   ✅ 读取消息
   ✅ 加入群聊
   ```

3. **发布应用**
   - 点击"发布"
   - 等待审核（通常很快）

---

### 第 4 步：配置事件订阅（3 分钟）

1. **进入应用 → 事件订阅**
   - 点击"事件订阅"

2. **开启事件订阅**
   - 打开开关

3. **配置订阅地址**
   ```
   http://你的服务器 IP:8080/feishu/event
   ```
   
   **注意：** 需要公网 IP
   
   **临时方案（本地测试）：**
   - 使用 ngrok 或 natapp 内网穿透
   - 或使用云服务器

4. **订阅事件**
   ```
   ✅ 接收消息
   ✅ 群聊消息
   ✅ @机器人消息
   ```

5. **保存配置**
   - 点击"保存"
   - 飞书会发送验证请求

---

### 第 5 步：添加到群（1 分钟）

1. **进入应用 → 机器人**
   - 点击"添加到群聊"

2. **选择"健康管理通知"群**
   - 找到你的群
   - 点击"添加"

3. **确认添加**
   - 机器人已加入群

---

### 第 6 步：配置本地文件

1. **复制配置模板**
   ```bash
   cd github/davidme6/health-guardian
   copy feishu_config.template.json feishu_config.json
   ```

2. **编辑配置文件**
   ```json
   {
     "app_id": "你的 App ID",
     "app_secret": "你的 App Secret",
     "verification_token": "你的 Verification Token",
     "server_port": 8080,
     "public_url": "http://你的服务器 IP:8080/feishu/event"
   }
   ```

3. **保存配置**

---

### 第 7 步：启动监听服务

1. **启动服务**
   ```bash
   python scripts/feishu_listener.py
   ```

2. **验证运行**
   ```
   🚀 飞书事件监听服务已启动
   📍 监听端口：8080
   ⏰ 等待飞书事件...
   ```

---

### 第 8 步：测试互动

1. **在群里@健康管家**
   ```
   @健康管家 喝了 250ml 水
   ```

2. **等待回复**
   - 系统会自动回复
   - 记录你的数据

3. **确认成功**
   - 收到回复 = 成功！

---

## 🔧 技术配置

### 服务器要求

**最低配置：**
- CPU: 1 核
- 内存：512MB
- 带宽：1Mbps
- 系统：Windows/Linux

**推荐配置：**
- CPU: 2 核
- 内存：1GB
- 带宽：2Mbps
- 系统：Linux（更稳定）

---

### 内网穿透（本地开发用）

**使用 ngrok：**

1. **下载 ngrok**
   ```
   https://ngrok.com/
   ```

2. **启动 ngrok**
   ```bash
   ngrok http 8080
   ```

3. **获取公网地址**
   ```
   Forwarding: https://xxxx.ngrok.io -> localhost:8080
   ```

4. **配置到飞书**
   ```
   订阅地址：https://xxxx.ngrok.io/feishu/event
   ```

---

### 云服务器部署（推荐）

**使用腾讯云/阿里云：**

1. **购买云服务器**
   - 1 核 1GB 即可
   - 约 50-100 元/月

2. **安装 Python**
   ```bash
   sudo apt-get update
   sudo apt-get install python3
   ```

3. **上传代码**
   ```bash
   git clone https://github.com/davidme6/health-guardian.git
   cd health-guardian
   ```

4. **配置防火墙**
   ```bash
   sudo ufw allow 8080
   ```

5. **启动服务**
   ```bash
   python3 scripts/feishu_listener.py
   ```

6. **配置飞书**
   ```
   订阅地址：http://你的服务器 IP:8080/feishu/event
   ```

---

## 📝 配置文件说明

### feishu_config.json

```json
{
  "app_id": "cli_xxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxx",
  "app_access_token": "",
  "verification_token": "xxxxxxxxxxxxxxxxx",
  "bot_name": "健康管家",
  "server_port": 8080,
  "public_url": "http://你的服务器 IP:8080/feishu/event"
}
```

**字段说明：**
- `app_id`: 飞书应用 ID
- `app_secret`: 应用密钥
- `app_access_token`: 自动获取（不用填）
- `verification_token`: 事件验证 Token
- `server_port`: 监听端口
- `public_url`: 公网访问地址

---

## ✅ 配置完成后的效果

### 你在群里发消息：
```
@健康管家 喝了 250ml 水
```

### 系统自动回复：
```
✅ 已记录饮水 250ml！

💧 当前进度
• 已喝：1250ml / 3605ml
• 进度：35%
• 还需喝：2355ml

💡 建议
• 每小时喝 250ml
• 小口慢饮

继续加油！💪
```

---

## 🎯 快速配置清单

- [ ] 创建飞书应用
- [ ] 获取 App ID 和 Secret
- [ ] 添加机器人
- [ ] 配置权限
- [ ] 配置事件订阅
- [ ] 添加到群
- [ ] 复制配置文件
- [ ] 填写配置信息
- [ ] 启动监听服务
- [ ] 测试互动

---

## 💬 配置完成后

**在群里直接@我：**

- "喝了 250ml 水"
- "运动了 30 分钟"
- "吃了汉堡"
- "查看健康状态"

**我会自动回复并记录！** 🤖

---

*最后更新：2026-03-12*
