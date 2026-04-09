# 💪 AI 一对一健身助手 (Fitness Assistant)

基于大语言模型的私人定制健身方案生成系统。通过 Streamlit 构建的现代化 Web 界面，为用户提供从身体素质评估到深度健身/饮食计划的一站式 AI 指导。

## 🌟 核心特性

-   **🎯 深度私人定制**：基于 13 项核心维度（身体数据、伤病史、训练环境、饮食作息等）生成极具针对性的健身方案。
-   **👤 多用户管理系统**：
    -   **侧边栏中心**：支持快速切换历史客户、一键新增客户。
    -   **数据隔离**：每个客户的数据独立存储在 `data/users/<姓名>/` 文件夹下。
    -   **秒速回看**：已有方案的用户可直接点击“查看方案”，无需重新调用 AI。
-   **🧠 智能合并更新**：为老客户更新方案时，AI 会自动融合旧报告与新变动，输出精简后的全套方案，避免文件冗余。
-   **🏃 沉浸式加载体验**：
    -   **异步生成**：采用多线程处理，AI 计算时不阻塞前端。
    -   **进度模拟**：内置 3 分钟平滑进度条（0-95%）及健身知识轮播科普。
-   **📈 商业化预览模式**：
    -   **1/3 预览机制**：网页端仅展示报告的前 1/3 内容，并配合渐变模糊效果。
    -   **解锁引导**：自动展示二维码，引导用户添加教练微信以获取 100% 完整版详尽文档。
-   **📧 管理员邮件触达**：
    -   **PushPlus 集成**：新方案生成后，系统会自动将全套方案（100% 完整版）通过 **邮件通道** 推送到管理员绑定的邮箱。
-   **🎨 现代圆润 UI**：极简、美观的圆角视觉风格，优化了输入框聚焦效果与交互反馈。

## 🛠️ 技术栈

-   **Frontend/Backend**: [Streamlit](https://streamlit.io/) (Python 全栈)
-   **AI Engine**: Qwen 3.5 27B (OpenAI 兼容接口)
-   **Notification**: PushPlus (邮件实时推送)
-   **Data Storage**: 本地隔离 Markdown 文件
-   **Concurrency**: Python `threading`

## 🚀 快速开始

### 1. 环境准备
```powershell
pip install -r requirements.txt
```

### 2. 配置文件
创建 `.env` 文件并填入凭证：
```ini
API_KEY=您的API密钥
BASE_URL=您的模型接口地址
MODEL_ID=qwen3.5-27b
PUSHPLUS_TOKEN=您的PushPlus密钥
```

### 3. 连通性测试 (可选)
验证邮件推送功能：
```powershell
python test_push.py
```

### 4. 运行应用
```powershell
streamlit run app.py
```

## 📂 项目结构

```text
Fitness Assistant/
├── app.py              # 主程序逻辑
├── test_push.py        # 微信/邮件推送连通性测试脚本
├── question.md         # 整理后的信息采集模板
├── requirements.txt    # 项目依赖
├── README.md           # 本文件
├── .env                # 配置文件 (已忽略)
├── ba609a72a4...jpg    # 引导用微信二维码
└── data/
    └── users/          # 客户数据物理隔离存储
        └── <客户姓名>/
            ├── user_profile.md  # 深度评估
            └── fitness_plan.md  # 健身计划
```

## 🔒 安全与隐私

-   **隐私保护**：用户数据存储在本地 `data/` 目录，通过 `.gitignore` 排除，严禁同步至公共仓库。
-   **凭证安全**：所有 API Key 均通过环境变量管理。

---

*由 AI 健身助手团队精心打造 - 专业，源于对细节的极致追求。*
