---
name: health-guardian
description: Health Guardian Anti-Aging Edition - Comprehensive health management with weight loss, hydration tracking, anti-aging care, exercise reminders, sleep optimization, and personalized recommendations. Integrates weather data and Feishu notifications.
version: 2.0.0-antiaging
author: davidme6
homepage: https://github.com/davidme6/openclaw/tree/main/skills/health-guardian
---

# 🏥 Health Guardian - 健康管理系统（新增抗衰老）

**全方位健康管理 · 科学减肥 · 抗衰老优化 · 智能提醒**

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **💧 喝水提醒** | 定时提醒，根据体重计算饮水量 |
| **🏃 运动计划** | 个性化运动建议，结合天气 |
| **😴 睡眠优化** | 睡眠呼吸暂停支持，呼吸机提醒 |
| **🍽️ 饮食指导** | 卡路里计算，营养建议 |
| **⚖️ 体重管理** | BMI 计算，减肥计划追踪 |
| **🌤️ 天气集成** | 根据当地天气调整建议 |
| **📱 飞书通知** | OpenClaw 飞书通道定时推送 |
| **✨ 抗衰老** | 护肤提醒、营养补充、拉伸运动 |

## 🆕 v2.0.0 抗衰老新增功能

### 护肤提醒
- 🧴 晨间护肤（07:00）
- 🌙 晚间护肤（21:00）
- ☀️ 防晒提醒

### 营养补充
- 🍊 维生素 C（08:00）- 抗氧化
- 🥜 维生素 E（12:00）- 保护细胞
- 🐟 Omega-3（18:00）- 抗炎

### 运动优化
- 🧘 拉伸放松（20:00）
- 💪 力量训练建议
- 🏃 有氧运动计划

### 睡眠强化
- 😴 黄金睡眠时间（22:30）
- 🌙 睡前准备清单
- 📱 蓝光管理

## 📋 用户配置

### 基本信息

```json
{
  "height": 178,
  "weight": 103,
  "age": 33,
  "gender": "male",
  "goal": "lose_weight",
  "target_weight": 90,
  "activity_level": "low"
}
```

### 健康状况

```json
{
  "conditions": ["sleep_apnea"],
  "devices": ["cpap"],
  "anti_aging_focus": ["skin_care", "nutrition", "sleep"]
}
```

### 通知配置

```json
{
  "channel": "feishu",
  "enabled": true,
  "quiet_hours": ["22:00", "07:00"]
}
```

## 🚀 快速开始

### 1. 初始化配置

```bash
cd github/davidme6/health-guardian
python scripts/health_guardian.py init
```

### 2. 查看今日计划

```bash
python scripts/health_guardian.py today
```

### 3. 记录数据

```bash
# 记录喝水
python scripts/health_guardian.py log-water 250

# 记录体重
python scripts/health_guardian.py log-weight 102.5
```

### 4. 查看状态

```bash
python scripts/health_guardian.py status
```

## ⏰ 完整提醒时间表

| 时间 | 类型 | 内容 |
|------|------|------|
| 07:00 | 🧴 护肤 | 晨间护肤 + 防晒 |
| 07:30 | ☀️ 早安 | 今日计划 |
| 08:00 | 💧 喝水 | + 维生素 C |
| 10:00 | 💧 喝水 | 保持水分 |
| 12:00 | 🍽️ 午餐 | + 维生素 E |
| 14:00 | 💧 喝水 | + 绿茶建议 |
| 16:00 | 💧 喝水 | 保持水分 |
| 17:00 | 🏃 运动 | 有氧/力量 |
| 18:00 | 🍽️ 晚餐 | + Omega-3 |
| 20:00 | 🧘 拉伸 | 放松助眠 |
| 21:00 | 🌙 护肤 | 晚间护肤 |
| 21:30 | 😴 睡前 | 准备睡觉 |

## 💬 OpenClaw 自然语言命令

直接对我说：
- "记录喝水 250ml"
- "记录体重 102.5"
- "查看健康状态"
- "今天喝了多少水？"
- "我的减肥进度如何？"

## 📊 健康计算

### 每日饮水
```
基础量 = 体重 (kg) × 35
运动追加 = 运动时长 × 12
高温追加 = 温度>30°C ? 500ml : 0
```

### BMI 分类
```
<18.5  偏瘦
18.5-24  正常
24-28  偏胖
>28  肥胖
```

### 减肥速度
```
安全速度：每周 0.5-1kg
热量缺口：500-750 大卡/天
1kg 脂肪 ≈ 7700 大卡
```

## 🌟 抗衰老核心建议

### 营养
- 维生素 C：抗氧化、促胶原
- 维生素 E：保护细胞膜
- Omega-3：抗炎、护心脑
- 多酚类：绿茶、蓝莓

### 护肤
- 晨间：清洁→保湿→防晒
- 晚间：清洁→修复→滋养
- 每天防晒！

### 运动
- 有氧：心肺功能
- 力量：增肌抗衰
- 拉伸：柔韧减压

### 睡眠
- 22:30 入睡
- 7-8 小时
- 黑暗安静

## ⚠️ 医疗免责声明

本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱
- 营养补充剂使用前请咨询医生

## 📁 项目结构

```
health-guardian/
├── SKILL.md
├── README.md
├── _meta.json
├── scripts/
│   ├── health_guardian.py
│   ├── notify.py
│   └── ...
└── references/
    ├── anti-aging-guide.md
    └── health-guidelines.md
```

## 🔧 故障排除

**Q: 收不到提醒？**
A: 检查 Windows 任务计划程序是否运行，OpenClaw 是否在线

**Q: 想修改提醒时间？**
A: 编辑 `~/.health_guardian_config.json` 中的 reminders 配置

**Q: 想关闭某些提醒？**
A: 在配置文件中将对应提醒的 enabled 设为 false

## 📞 支持

- GitHub: https://github.com/davidme6/openclaw/issues
- ClawHub: https://clawhub.com/skills/health-guardian

---

**健康是人生的第一财富！让 Health Guardian 陪你一起变健康、变年轻！** 💪✨
