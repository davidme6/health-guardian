---
name: health-guardian
description: Health Guardian Anti-Aging Edition - Multi-user interactive health management with calorie tracking, personalized notifications via Feishu
version: 3.0.0-multiuser
author: davidme6
homepage: https://github.com/davidme6/openclaw/tree/main/skills/health-guardian
---

# 🏥 Health Guardian - 健康管理系统（多用户交互式）

**全方位健康管理 · 科学减肥 · 抗衰老优化 · 多用户支持 · 交互式通知**

[![Version](https://img.shields.io/badge/version-3.0.0--multiuser-blue.svg)](https://github.com/davidme6/openclaw/tree/main/skills/health-guardian)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 功能特性

### 💧 智能喝水提醒
- 根据体重自动计算每日饮水量
- 定时提醒，飞书独立窗口通知
- 交互式记录，实时更新进度

### 🏃 个性化运动计划
- 根据体重、天气推荐运动
- 室内/室外自动切换
- 卡路里消耗追踪
- 运动数据实时记录

### 😴 睡眠优化
- 睡眠呼吸暂停支持
- 呼吸机使用提醒
- 睡前准备清单
- 睡眠质量追踪

### 🍽️ 饮食指导
- **科学热量计算**（新增）
- 三大营养素分配
- 一日三餐建议
- 食物热量查询
- 饮食记录与分析

### ⚖️ 体重管理
- BMI 计算与健康评估
- 减肥计划追踪
- 周报生成
- 减重速度预测

### 🌤️ 天气集成
- 自动获取当地天气
- 根据天气调整建议
- 空气质量提醒

### 📱 飞书独立通知
- 独立会话窗口
- 交互式卡片消息
- 实时数据记录
- 多用户支持（新增）

### ✨ 抗衰老优化
- 日出而作，日入而息（昼夜节律）
- 清茶淡饭（清淡饮食）
- 不劳心力（压力管理）
- 顺应自然（生活方式）
- 柳叶刀研究三大黄金标准

---

## 🆕 v3.0.0 多用户交互式新增功能

### 多用户支持
- ✅ 支持无限个用户
- ✅ 每个用户独立健康档案
- ✅ 专属飞书通知窗口
- ✅ 个性化数据推送

### 交互式通知
- ✅ 询问真实数据
- ✅ 实时记录反馈
- ✅ 按钮交互
- ✅ 消息回复识别

### 科学热量管理
- ✅ Mifflin-St Jeor 公式计算
- ✅ BMR/TDEE精准计算
- ✅ 三大营养素分配
- ✅ 一日三餐建议
- ✅ 食物热量查询
- ✅ 饮食记录分析

### 飞书独立通知
- ✅ 独立会话窗口
- ✅ 不和开发消息混合
- ✅ 美观卡片消息
- ✅ 实时互动反馈

---

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
- 飞书 webhook URL
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

# 计算热量需求
python scripts/calorie_calculator.py

# 发送飞书通知
python scripts/interactive_notify.py now
```

---

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

### 热量计算（Mifflin-St Jeor 公式）
```
男性 BMR = (10 × 体重 kg) + (6.25 × 身高 cm) - (5 × 年龄) + 5
女性 BMR = (10 × 体重 kg) + (6.25 × 身高 cm) - (5 × 年龄) - 161

TDEE = BMR × 活动系数

减肥目标 = TDEE - 500 大卡（安全减重）
```

### 减重速度
```
安全速度：每周 0.5-1kg
热量缺口：500-750 大卡/天
1kg 脂肪 ≈ 7700 大卡
```

---

## ⏰ 完整提醒时间表

| 时间 | 类型 | 内容 |
|------|------|------|
| 07:00 | 🧴 晨间护肤 | 洁面→保湿→防晒 |
| 07:30 | ☀️ 早安 | 今日计划 + 抗衰老重点 |
| 08:00 | 💧 喝水 + 维 C | 250ml + 抗氧化 |
| 10:00 | 💧 喝水 | 250ml |
| 12:00 | 🍽️ 午餐 + 维 E | 豆制品 + 全谷物 |
| 14:00 | 💧 喝水 | 250ml + 绿茶 |
| 16:00 | 💧 喝水 | 250ml + 坚果 |
| 17:00 | 🏃 运动 | 30 分钟有氧/力量 |
| 18:00 | 🍽️ 晚餐 | 清淡 + Omega-3 |
| 20:00 | 🧘 拉伸 | 10 分钟放松 |
| 21:00 | 🌙 晚间护肤 | 清洁→修复→滋养 |
| 21:30 | 😴 睡前准备 | 关闭电子设备 |
| 22:30 | 💤 入睡 | 保证 7-8 小时 |

**检查频率：** 每 10 分钟自动检查  
**通知方式：** 飞书独立会话窗口

---

## 🌟 抗衰老核心建议

### 抖音视频养生智慧
- 日出而作，日入而息
- 清茶淡饭
- 不劳心力
- 顺应自然

### 柳叶刀研究（2026 年 1 月）
- 样本：近 6 万人，随访 8 年
- 三大黄金标准：好好睡觉 + 好好运动 + 好好吃饭
- 效果：延长健康寿命 9.45 年

---

## ⚠️ 医疗免责声明

**重要：** 本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱
- 营养补充剂使用前请咨询医生

---

## 📞 支持

- **GitHub Issues:** https://github.com/davidme6/openclaw/issues
- **ClawHub:** https://clawhub.com/skills/health-guardian

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

**davidme6**

- GitHub: [@davidme6](https://github.com/davidme6)
- ClawHub: [@davidme6](https://clawhub.com/@davidme6)

---

**健康是人生的第一财富！让 Health Guardian 陪你一起变健康、变年轻！** 💪✨

*顺应自然，清茶淡饭，不劳心力，健康长寿！* 🌟
