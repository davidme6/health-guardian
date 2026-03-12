---
name: health-guardian
description: Health Guardian Anti-Aging Edition - Multi-user interactive health management with Feishu two-way communication, calorie tracking, and automated notifications
version: 3.1.0-feishu-interactive
author: davidme6
homepage: https://github.com/davidme6/openclaw/tree/main/skills/health-guardian
---

# 🏥 Health Guardian - 健康管理系统（飞书双向互动版）

**全方位健康管理 · 科学减肥 · 抗衰老优化 · 多用户支持 · 飞书双向互动**

[![Version](https://img.shields.io/badge/version-3.1.0--feishu--interactive-blue.svg)](https://github.com/davidme6/openclaw/tree/main/skills/health-guardian)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 功能特性

### 💬 飞书双向互动（新增）⭐⭐⭐⭐⭐
- ✅ 在群里@健康管家，自动回复
- ✅ 智能识别饮水、运动、饮食、体重等记录
- ✅ 实时数据分析和建议
- ✅ 24 小时自动响应

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
- **科学热量计算**（Mifflin-St Jeor 公式）
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
- 多用户支持

### ✨ 抗衰老优化
- 日出而作，日入而息
- 清茶淡饭
- 不劳心力
- 顺应自然
- 柳叶刀研究三大黄金标准

---

## 🆕 v3.1.0 飞书双向互动新增功能

### 飞书机器人互动
- ✅ 创建飞书企业自建应用
- ✅ 添加机器人到群
- ✅ 配置事件订阅
- ✅ 自动接收群消息
- ✅ 智能识别用户意图
- ✅ 实时回复和建议

### 智能消息识别
- ✅ 饮水记录："喝了 250ml"
- ✅ 运动记录："运动了 30 分钟"、"走了 5000 步"
- ✅ 饮食记录："吃了汉堡和薯条"
- ✅ 体重记录："体重 102.5kg"
- ✅ 睡眠记录："昨晚睡得不错"
- ✅ 状态查询："查看健康状态"

### 自动回复系统
- ✅ 记录数据并确认
- ✅ 计算进度和百分比
- ✅ 提供科学建议
- ✅ 鼓励和激励

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

### 配置飞书双向互动

#### 第 1 步：创建飞书应用

1. 访问：https://open.feishu.cn/app
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

#### 第 2 步：添加机器人

1. 应用 → 添加机器人
2. 创建机器人"健康管家"
3. 获取 Verification Token

#### 第 3 步：配置权限

```
✅ 获取用户信息
✅ 发送消息
✅ 读取消息
✅ 加入群聊
```

#### 第 4 步：配置事件订阅

```
订阅地址：http://你的服务器 IP:8080/feishu/event
订阅事件：
- 接收消息
- 群聊消息
- @机器人消息
```

#### 第 5 步：配置本地文件

```bash
cd github/davidme6/health-guardian
copy feishu_config.template.json feishu_config.json
```

编辑 `feishu_config.json`：
```json
{
  "app_id": "你的 App ID",
  "app_secret": "你的 App Secret",
  "verification_token": "你的 Verification Token",
  "server_port": 8080
}
```

#### 第 6 步：启动监听服务

```bash
python scripts/feishu_listener.py
```

#### 第 7 步：添加到群

1. 应用 → 机器人 → 添加到群聊
2. 选择"健康管理通知"群
3. 确认添加

---

### 基本使用

#### 在飞书群里@健康管家：

**记录饮水：**
```
@健康管家 喝了 250ml 水
```

**记录运动：**
```
@健康管家 运动了 30 分钟
@健康管家 走了 5000 步
```

**记录饮食：**
```
@健康管家 吃了汉堡和薯条
@健康管家 早餐吃了鸡蛋牛奶
```

**记录体重：**
```
@健康管家 体重 102.5kg
```

**查询状态：**
```
@健康管家 查看健康状态
@健康管家 今天喝了多少水
```

**获取帮助：**
```
@健康管家 帮助
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

---

## ⏰ 定时提醒时间表

| 时间 | 类型 | 内容 |
|------|------|------|
| 07:00 | 🧴 晨间护肤 | 洁面→保湿→防晒 |
| 07:30 | ☀️ 早安 | 今日计划 |
| 08:00 | 💧 喝水 + 维 C | 250ml |
| 10:00 | 💧 喝水 | 250ml |
| 12:00 | 🍽️ 午餐 + 维 E | 豆制品 + 全谷物 |
| 14:00 | 💧 喝水 | 250ml |
| 16:00 | 💧 喝水 | 250ml |
| 17:00 | 🏃 运动 | 30 分钟 |
| 18:00 | 🍽️ 晚餐 | 清淡 + Omega-3 |
| 20:00 | 🧘 拉伸 | 10 分钟 |
| 21:00 | 🌙 晚间护肤 | 清洁→修复→滋养 |
| 21:30 | 😴 睡前准备 | 关闭电子设备 |
| 22:30 | 💤 入睡 | 7-8 小时 |

**检查频率：** 每 10 分钟自动检查

---

## 💬 飞书互动示例

### 用户：
```
@健康管家 喝了 250ml 水
```

### 系统回复：
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

## ⚠️ 医疗免责声明

**重要：** 本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱

---

## 📞 支持

- **GitHub Issues:** https://github.com/davidme6/openclaw/issues
- **配置文档:** FEISHU_APP_SETUP.md

---

## 📄 许可证

MIT License

---

## 👨‍💻 作者

**davidme6**

---

**健康是人生的第一财富！让 Health Guardian 陪你一起变健康、变年轻！** 💪✨
