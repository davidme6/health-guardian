# 🚀 Health Guardian 发布指南

## 📦 已完成的部署

### ✅ 本地 OpenClaw
- **位置**: `C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\health-guardian`
- **状态**: ✅ 已安装
- **测试**: 待测试

### ✅ GitHub 仓库
- **位置**: `C:\Windows\System32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian`
- **状态**: ✅ 已提交
- **推送**: 待推送到远程

---

## 🌐 发布到各平台

### 1. GitHub 发布

```bash
# 进入仓库目录
cd C:\Windows\System32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian

# 添加远程仓库（如果还没有）
git remote add origin https://github.com/davidme6/health-guardian.git

# 推送到 GitHub
git push -u origin master

# 创建 Release
# 访问：https://github.com/davidme6/health-guardian/releases/new
# Tag: v1.0.0
# Title: Health Guardian v1.0.0 - 个人健康管家
```

**发布内容：**
- ✅ 完整源代码
- ✅ README.md 使用文档
- ✅ 配置文件示例
- ✅ 健康指南参考文档

---

### 2. ClawHub 发布

#### 方式 1: 使用 CLI
```bash
# 登录 ClawHub
npx clawhub login

# 发布技能
npx clawhub publish "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\health-guardian"
```

#### 方式 2: 手动上传
1. 访问：https://clawhub.com/upload
2. 选择文件夹：`C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\health-guardian`
3. 填写信息：
   - **Slug**: health-guardian
   - **Display Name**: Health Guardian - 个人健康管家
   - **Version**: 1.0.0
   - **Tags**: health, fitness, weight-loss, reminders, wechat, imessage, notifications
   - **License**: MIT
4. 上传发布

---

### 3. 腾讯 SkillHub 发布

访问：https://skillhub.tencent.com/

#### 发布步骤：
1. **注册/登录** 腾讯 SkillHub
2. **创建技能**
   - 技能名称：Health Guardian - 个人健康管家
   - 技能描述：全方位健康管理，支持企业微信/iMessage/钉钉等多渠道通知
   - 技能分类：健康医疗 / 效率工具
3. **上传代码**
   - 上传 `health-guardian` 文件夹全部内容
   - 或关联 GitHub 仓库：https://github.com/davidme6/health-guardian
4. **填写配置**
   ```json
   {
     "name": "health-guardian",
     "version": "1.0.0",
     "description": "个人健康管家 - 全方位健康管理 · 科学减肥 · 智能提醒",
     "author": "davidme6",
     "license": "MIT",
     "keywords": ["健康", "减肥", "提醒", "企业微信", "iMessage", "通知"],
     "entry": "scripts/health_guardian.py",
     "requirements": ["requests"]
   }
   ```
5. **提交审核**
   - 通常 1-3 个工作日审核完成
   - 审核通过后自动上架

---

## 📱 通知渠道配置示例

### 企业微信
```json
{
  "notifications": {
    "channels": {
      "wechat_work": {
        "enabled": true,
        "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```

### iMessage (BlueBubbles)
```json
{
  "notifications": {
    "channels": {
      "imessage": {
        "enabled": true,
        "bluebubbles_url": "http://your-server:12345",
        "bluebubbles_token": "your-token",
        "recipient": "+8613800138000"
      }
    }
  }
}
```

### iMessage (macOS 本地)
```json
{
  "notifications": {
    "channels": {
      "imessage": {
        "enabled": true,
        "use_local_imessage": true,
        "recipient": "iMessage 联系人"
      }
    }
  }
}
```

### 钉钉
```json
{
  "notifications": {
    "channels": {
      "dingtalk": {
        "enabled": true,
        "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
        "secret": "YOUR_SECRET"
      }
    }
  }
}
```

### 飞书
```json
{
  "notifications": {
    "channels": {
      "feishu": {
        "enabled": true,
        "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK"
      }
    }
  }
}
```

### Slack
```json
{
  "notifications": {
    "channels": {
      "slack": {
        "enabled": true,
        "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
      }
    }
  }
}
```

### Telegram
```json
{
  "notifications": {
    "channels": {
      "telegram": {
        "enabled": true,
        "bot_token": "YOUR_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
      }
    }
  }
}
```

### 邮件
```json
{
  "notifications": {
    "channels": {
      "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "your@gmail.com",
        "password": "your-password",
        "to_email": "recipient@example.com"
      }
    }
  }
}
```

---

## 🧪 测试流程

### 1. 本地测试
```bash
# 初始化配置
cd C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\health-guardian
python scripts/health_guardian.py init

# 测试通知
python scripts/notifications.py test

# 发送测试消息
python scripts/health_guardian.py remind water
```

### 2. 功能测试清单

- [ ] 初始化配置正常
- [ ] 喝水记录正常
- [ ] 体重记录正常
- [ ] 今日计划显示正常
- [ ] 健康状态显示正常
- [ ] 企业微信通知正常
- [ ] iMessage 通知正常（如配置）
- [ ] 其他通知渠道正常（如配置）
- [ ] 周报生成正常
- [ ] 天气集成正常

---

## 📊 推广建议

### 1. 社交媒体
- **微博**: 发布使用截图 + 功能介绍
- **小红书**: 健康管理心得 + 工具推荐
- **知乎**: 回答减肥/健康管理相关问题，推荐工具
- **抖音**: 制作使用演示视频

### 2. 技术社区
- **GitHub Trending**: 优化 README，增加 star
- **V2EX**: 分享帖子介绍项目
- **掘金**: 写技术文章介绍实现
- **少数派**: 投稿效率工具推荐

### 3. 健康社区
- **Keep**: 分享减肥经验 + 工具
- **薄荷健康**: 饮食管理心得
- **知乎健康**: 专业回答 + 工具推荐

---

## 📈 后续迭代计划

### v1.1.0 (计划中)
- [ ] 增加食物卡路里数据库
- [ ] 增加运动视频指导
- [ ] 增加数据导出功能
- [ ] 增加多用户支持

### v1.2.0 (计划中)
- [ ] 接入智能手环/手表
- [ ] 自动同步运动数据
- [ ] 自动同步睡眠数据
- [ ] 心率监测集成

### v2.0.0 (计划中)
- [ ] AI 健康顾问
- [ ] 个性化饮食计划生成
- [ ] 个性化运动计划生成
- [ ] 健康风险评估

---

## 📞 用户支持

### 问题反馈
- GitHub Issues: https://github.com/davidme6/health-guardian/issues
- 邮箱：your-email@example.com

### 文档
- 使用文档：README.md
- 健康指南：references/health-guidelines.md
- API 文档：scripts/notifications.py 注释

---

## ⚠️ 注意事项

### 医疗免责声明
**重要：** 本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱
- 本技能不诊断、治疗任何疾病

### 隐私保护
- 所有健康数据存储在本地
- 不上传任何个人数据到云端（除非用户主动配置）
- 通知渠道使用 HTTPS 加密传输

### 合规性
- 遵守各平台开发者协议
- 遵守医疗健康相关法规
- 遵守数据保护法规（如 GDPR、个人信息保护法）

---

**祝发布顺利！帮助更多人实现健康目标！** 💪✨
