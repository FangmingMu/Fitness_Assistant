# Design: enhance-ux

## Architecture: Streamlit State Machine
使用 `st.session_state` 控制应用的渲染逻辑。
- `st.session_state.page`: 控制显示的视图 (`"form"`, `"loading"`, `"result"`)。
- `st.session_state.results`: 暂存 AI 生成的 Markdown 结果 (`{"profile": "...", "plan": "..."}`)。

## Async Execution (Threading)
- **Problem**: Streamlit 的主线程是阻塞的。
- **Solution**: 
  - 使用 `threading.Thread` 进行 `get_ai_response`。
  - 主线程通过 `while` 循环配合 `time.sleep` 进行 UI 的状态刷新（进度条、知识点轮播）。
  - 使用 `st.empty` 容器动态替换展示的内容。

## Progress Bar Logic
- 设定 180 秒（3 分钟）为进度上限。
- 每秒钟进度条平滑增长（例如：每秒增约 0.5%），在达到 90% 后停止增长，直到线程返回。
- 线程返回后，进度条直接跳至 100%。

## Enhanced Prompts
- **评估 Prompt**: 强制要求对性别、年龄、身高、体重指数、伤病风险等级等 10 个以上维度进行深度分析。
- **计划 Prompt**: 训练方案必须包含“准备活动、正式训练、拉伸放松”三大版块，动作需标明“RPE 强度、组数、次数、间歇”。饮食建议需计算具体的全天能量目标及蛋白质/碳水/脂肪比例。
