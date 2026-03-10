# 🏥 Health Guardian - 个人健康管家

**全方位健康管理 · 科学减肥 · 智能提醒 · 个性化建议**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/davidme6/openclaw/tree/main/skills/health-guardian)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 功能特性

### 💧 智能喝水提醒
- 根据体重自动计算每日饮水量
- 定时提醒，支持企业微信通知
- 根据天气温度自动调整建议

### 🏃 个性化运动计划
- 根据体重、天气推荐运动
- 室内/室外自动切换
- 卡路里消耗追踪

### 😴 睡眠优化
- 睡眠呼吸暂停支持
- 呼吸机使用提醒
- 睡前准备清单

### 🍽️ 饮食指导
- 卡路里计算
- 营养建议
- 用餐提醒

### ⚖️ 体重管理
- BMI 计算与健康评估
- 减肥计划追踪
- 周报生成

### 🌤️ 天气集成
- 自动获取当地天气
- 根据天气调整建议
- 空气质量提醒

### 📱 多渠道通知
- OpenClaw Web 通知
- 企业微信机器人
- 定时/手动触发

## 🚀 快速开始

### 安装

```bash
# 使用 ClawHub
npx skills add davidme6/openclaw@health-guardian

# 或手动安装
git clone https://github.com/davidme6/openclaw.git
cp -r openclaw/skills/health-guardian ~/.openclaw/workspace/skills/
```

### 初始化

```bash
cd health-guardian
python scripts/health_guardian.py init
```

按照向导输入：
- 身高、体重、年龄
- 健康状况（如睡眠呼吸暂停）
- 使用设备（如呼吸机）
- 企业微信 webhook（可选）
- 所在城市

### 基本使用

```bash
# 查看今日计划
python scripts/health_guardian.py today

# 记录喝水 250ml
python scripts/health_guardian.py log-water 250

# 记录体重
python scripts/health_guardian.py log-weight 102.5

# 查看健康状态
python scripts/health_guardian.py status

# 手动触发喝水提醒
python scripts/health_guardian.py remind water

# 生成周报
python scripts/health_guardian.py weekly-report
```

## 📊 科学计算

### 每日饮水量
```
基础量 (ml) = 体重 (kg) × 35
运动追加 = 运动时长 (分钟) × 12
高温追加 = 温度>30°C ? 500ml : 0
```

### BMI 分类
```
< 18.5  偏瘦
18.5-24 正常
24-28   偏胖
> 28    肥胖
```

### 减肥计划
- 安全减重速度：每周 0.5-1kg
- 每日热量缺口：500-750 大卡
- 1kg 脂肪 ≈ 7700 大卡

## ⚙️ 配置

### 配置文件位置
```
~/.health_guardian_config.json
```

### 示例配置
```json
{
  "user": {
    "height_cm": 178,
    "weight_kg": 103,
    "age": 30,
    "gender": "male",
    "goal": "lose_weight",
    "target_weight_kg": 75
  },
  "health": {
    "conditions": ["sleep_apnea"],
    "devices": ["cpap"]
  },
  "notifications": {
    "wechat_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "enabled": true
  },
  "location": {
    "city": "北京"
  }
}
```

## 📱 企业微信通知配置

### 1. 创建机器人
1. 企业微信 → 工作台 → 群机器人
2. 添加机器人
3. 复制 webhook URL

### 2. 配置到 Health Guardian
```json
{
  "notifications": {
    "wechat_webhook": "你的 webhook URL",
    "enabled": true
  }
}
```

### 3. 测试通知
```bash
python scripts/health_guardian.py remind water
```

## 📋 提醒时间表

| 类型 | 默认时间 | 说明 |
|------|---------|------|
| 💧 喝水 | 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00 | 每次 250ml |
| 🍽️ 用餐 | 07:30, 12:00, 18:00 | 三餐提醒 |
| 🏃 运动 | 17:00 | 根据天气调整 |
| 😴 睡前 | 21:30 | 睡前准备 |

## 🌤️ 天气集成

使用 [wttr.in](https://wttr.in) 获取天气：

```bash
# 测试天气 API
curl wttr.in/北京?format=j1
```

根据天气自动调整：
- 温度>30°C → 增加饮水 500ml，建议室内运动
- 温度<10°C → 建议保暖，室内运动
- 雨天 → 室内运动替代方案
- 空气质量差 → 避免户外运动

## ⚠️ 医疗免责声明

**重要：** 本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱
- 本技能不诊断、治疗任何疾病

## 📁 项目结构

```
health-guardian/
├── SKILL.md                  # 技能定义
├── README.md                 # 本文件
├── LICENSE                   # MIT 许可证
├── _meta.json                # ClawHub 元数据
├── scripts/
│   ├── health_guardian.py    # 主脚本
│   ├── notifications.py      # 通知模块
│   ├── weather.py            # 天气集成
│   └── calculations.py       # 健康计算
└── references/
    ├── health-guidelines.md  # 健康指南
    └── notification-templates.md  # 通知模板
```

## 🆘 故障排除

### Q: 微信通知不工作？
A: 检查 webhook URL 是否正确，确保企业微信机器人已启用

### Q: 天气数据获取失败？
A: 检查网络连接，wttr.in 可能暂时不可用

### Q: 提醒时间不准确？
A: 检查系统时区设置，确认配置文件中的时间格式

### Q: Python 依赖缺失？
A: 安装依赖：`pip install requests`

## 📊 使用示例

### 完整使用流程

```bash
# 1. 初始化
python scripts/health_guardian.py init

# 2. 查看今日计划
python scripts/health_guardian.py today

# 3. 早上喝水
python scripts/health_guardian.py log-water 250

# 4. 午餐前
python scripts/health_guardian.py remind meal

# 5. 运动后
python scripts/health_guardian.py log-weight 102.3

# 6. 周末生成周报
python scripts/health_guardian.py weekly-report
```

### 输出示例

```
📊 健康状态
============================================================

⚖️  体重指数
   BMI: 32.5 (肥胖)
   当前：103.0kg
   目标：75.0kg
   还需：28.0kg

💧 今日饮水
   1500ml / 3600ml (42%)

📈 体重趋势
   2026-03-06: 103.5kg
   2026-03-07: 103.2kg
   2026-03-08: 103.0kg
   2026-03-09: 102.8kg
   2026-03-10: 102.5kg

============================================================
```

## 📞 支持

- **GitHub Issues:** https://github.com/davidme6/openclaw/issues
- **ClawHub:** https://clawhub.com/skills/health-guardian

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**davidme6**

- GitHub: [@davidme6](https://github.com/davidme6)
- ClawHub: [@davidme6](https://clawhub.com/@davidme6)

---

**健康是人生的第一财富！让 Health Guardian 陪你一起变健康！** 💪✨
