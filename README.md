# 🏥 Health Guardian - 健康管理系统（新增抗衰老）

**全方位健康管理 · 科学减肥 · 智能提醒 · 抗衰老优化**

[![Version](https://img.shields.io/badge/version-2.0.0--antiaging-blue.svg)](https://github.com/davidme6/openclaw/tree/main/skills/health-guardian)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 功能特性

### 💧 智能喝水提醒
- 根据体重自动计算每日饮水量
- 定时提醒，支持飞书通知
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
- OpenClaw 飞书通知
- 企业微信机器人（可选）
- 定时/手动触发

### ✨ 抗衰老优化（新增）
- 🧴 晨间/晚间护肤提醒
- 🧬 抗氧化营养补充建议
- ☀️ 防晒提醒
- 🧘 拉伸放松指导
- 🍊 维生素 C/E/Omega-3 补充提醒
- 🌙 睡眠优化（黄金修复时间）

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
- 飞书/企业微信 webhook（可选）
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

# 手动触发提醒
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
    "age": 33,
    "gender": "male",
    "goal": "lose_weight",
    "target_weight_kg": 90
  },
  "health": {
    "conditions": ["sleep_apnea"],
    "devices": ["cpap"],
    "anti_aging_focus": ["skin_care", "nutrition", "sleep_optimization"]
  },
  "notifications": {
    "channel": "feishu",
    "enabled": true
  },
  "anti_aging": {
    "enabled": true,
    "goals": [
      "保持皮肤健康",
      "延缓衰老进程",
      "提高生活质量"
    ]
  }
}
```

## ⏰ 完整提醒时间表

| 时间 | 类型 | 说明 |
|------|------|------|
| 07:00 | 🧴 晨间护肤 | 洁面、保湿、防晒 |
| 07:30 | ☀️ 早安 | 今日计划 + 抗衰老重点 |
| 08:00 | 💧 喝水 + 维 C | 抗氧化补充 |
| 10:00 | 💧 喝水 | 保持水分 |
| 12:00 | 🍽️ 午餐 + 维 E | 营养补充 |
| 14:00 | 💧 喝水 + 绿茶 | 抗氧化 |
| 16:00 | 💧 喝水 | 保持水分 |
| 17:00 | 🏃 运动 | 有氧 + 力量训练 |
| 18:00 | 🍽️ 晚餐 + Omega-3 | 抗炎抗衰老 |
| 20:00 | 🧘 拉伸 | 放松助眠 |
| 21:00 | 🌙 晚间护肤 | 夜间修复 |
| 21:30 | 😴 睡前准备 | 黄金睡眠时间 |

## 🌟 抗衰老核心建议

### 1. 营养补充
- **维生素 C**：抗氧化、促进胶原蛋白
- **维生素 E**：保护细胞膜、延缓衰老
- **Omega-3**：抗炎、保护心血管
- **多酚类**：绿茶、蓝莓、番茄

### 2. 皮肤护理
- **晨间**：清洁→保湿→防晒
- **晚间**：清洁→修复→滋养
- **防晒**：每天使用，防止光老化

### 3. 运动健身
- **有氧运动**：促进新陈代谢
- **力量训练**：增加肌肉量、延缓衰老
- **拉伸**：保持柔韧性、减少皱纹

### 4. 睡眠优化
- **时间**：22:30 入睡，保证 7-8 小时
- **环境**：黑暗、安静、适宜温度
- **设备**：睡眠呼吸暂停患者使用呼吸机

## ⚠️ 医疗免责声明

**重要：** 本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱
- 营养补充剂使用前请咨询医生

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

**健康是人生的第一财富！让 Health Guardian 陪你一起变健康、变年轻！** 💪✨
