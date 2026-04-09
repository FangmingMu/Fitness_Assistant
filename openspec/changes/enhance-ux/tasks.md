# Tasks: enhance-ux

1. **状态机基础设施建设**:
   - 在 `app.py` 中初始化 `st.session_state.page = "form"` 和 `st.session_state.results = {}`。
   - 创建视图切换逻辑（`if-elif-else` 分发器）。

2. **多线程调用与加载页开发**:
   - 编写 `run_ai_async` 函数，将原来的 AI 调用逻辑封装并能在子线程中执行。
   - 实现 `render_loading_page()` 视图：包含进度条渲染和 10 条基础健身知识的轮播逻辑（每 10 秒切换一次）。

3. **结果页渲染逻辑**:
   - 实现 `render_result_page()`：提取 `st.session_state.results` 中的内容并使用 `st.tabs` 渲染。
   - 提供“返回修改”按钮，点击后重置 `st.session_state.page = "form"`。

4. **Prompt 强化**:
   - 深入重写 `eval_system_prompt` 和 `plan_system_prompt`。
   - 测试新的 Prompt 效果是否能产生比原来长 2 倍以上的有效内容。

5. **验证与部署**:
   - 本地模拟 3 分钟等待，检查进度条的平滑度和知识轮播的正确性。
   - 检查文件覆盖写入逻辑在跳转后是否依然正确。
