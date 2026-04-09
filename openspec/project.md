# Project Context: Fitness Assistant

## Purpose
开发一个基于 AI 的极简一对一健身助手，能够根据用户输入实时生成并更新客户评估报告与定制化健身计划。

## Tech Stack
- **Backend/Frontend**: Python + Streamlit (Full-stack)
- **AI Model**: qwen3.5-27b (via OpenAI compatible API)
- **Configuration**: python-dotenv
- **Storage**: Local Markdown files (user_profile.md, fitness_plan.md)

## Project Conventions

### Code Style
- 遵循 KISS 原则，保持逻辑简单、不冗余。
- 使用 Streamlit 组件快速构建 UI，通过 CSS 注入实现视觉优化。

### Architecture Patterns
- **智能合并更新**: 在写入 Markdown 文件前，将新旧数据同时发送给 AI，指令其输出合并后的单一精简文档，实现覆盖更新而非追加。

## Important Constraints
- API 密钥和本地模型地址必须存储在 `.env` 中，严禁推送到 Git。
- Markdown 文件应只保留最新、最核心的信息。
