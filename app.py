import streamlit as st
import os
import time
import random
import threading
from openai import OpenAI
from dotenv import load_dotenv

# ==========================================
# 1. 绝对第一位的 Streamlit 命令
# ==========================================
st.set_page_config(
    page_title="AI 健身助手", 
    page_icon="💪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 状态初始化 (必须在顶层，确保上下文)
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "form"
if "results" not in st.session_state:
    st.session_state.results = {}
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ==========================================
# 3. 环境与配置加载
# ==========================================
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")

DATA_DIR = "data/users"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 初始化 AI 客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 健身知识库
FITNESS_TIPS = [
    "💡 深蹲时，保持背部挺直，感受臀部发力，膝盖不要超过脚尖过多。",
    "💡 减脂的本质是热量缺口，但不要盲目节食，保证蛋白质摄入能防止肌肉流失。",
    "💡 力量训练后的拉伸可以有效缓解延迟性肌肉酸痛 (DOMS)。",
    "💡 水分摄入对代谢至关重要，建议每天摄入体重(kg) x 35ml 的水。",
    "💡 睡眠是肌肉生长的核心时间，每天保证 7-8 小时高质量睡眠。",
    "💡 动作的质量永远优先于重量，错误的动作只会增加受伤风险。",
    "💡 复合动作 (如硬拉、卧推) 能一次性动员更多肌肉群，效率更高。",
    "💡 蛋白质是肌肉修复的砖块，减脂期建议每公斤体重摄入 1.6-2.0g 蛋白质。",
    "💡 平台期很正常，可以尝试改变训练顺序或增加训练强度 (RPE)。",
    "💡 健身是一场马拉松，坚持比爆发更重要，保持心态平衡。"
]

# ==========================================
# 4. 样式注入
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main .block-container {
        border-radius: 24px;
        background: white;
        padding: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-top: 2rem;
    }
    div.stButton > button {
        border-radius: 30px;
        padding: 0.6rem 2.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4CAF50, #8BC34A); }
    .tip-card {
        padding: 20px;
        border-radius: 15px;
        background: #e8f5e9;
        border-left: 5px solid #4CAF50;
        font-size: 1.2rem;
        color: #2e7d32;
        margin: 20px 0;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 10px 15px !important;
        color: #1e293b !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4CAF50 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.1) !important;
        outline: none !important;
    }
    .stWidgetLabel p {
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: #334155 !important;
        margin-bottom: 6px !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 0.4rem 1rem;
        text-transform: none;
        letter-spacing: 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 5. 业务逻辑函数
# ==========================================
def get_user_file_path(username, filename):
    user_dir = os.path.join(DATA_DIR, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return os.path.join(user_dir, filename)

def read_md_file(username, filename):
    path = get_user_file_path(username, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_md_file(username, filename, content):
    path = get_user_file_path(username, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_existing_users():
    if not os.path.exists(DATA_DIR):
        return []
    return sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])

def get_ai_response(system_prompt, user_content):
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def send_pushplus_notification(title, content):
    """通过 PushPlus 发送微信通知"""
    if not PUSHPLUS_TOKEN:
        return
    
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "markdown"
    }
    try:
        requests.post(url, json=data, timeout=10)
    except Exception:
        pass  # 推送失败不影响主业务

def run_ai_processing(username, new_info, results_dict):
    """异步任务"""
    old_profile = read_md_file(username, "user_profile.md")
    eval_prompt = "你是一个专业的健身教练。请根据用户新旧信息生成一份深度评估报告 Markdown。要求：格式清晰，使用表格。"
    
    profile_result = get_ai_response(eval_prompt, f"客户:{username}\n新信息:{new_info}\n旧报告:{old_profile}")
    if "Error" in profile_result:
        results_dict["error"] = profile_result
        return

    old_plan = read_md_file(username, "fitness_plan.md")
    plan_prompt = """你是一个金牌教练。请生成详细的健身与饮食方案。
    要求：表格必须包含 7 列，且表头与分隔线严格对齐（8个竖线 | 分隔 7 列）。
    示例：| 训练阶段 | 动作名称 | 组数 | 次数 | RPE | 组间休息 | 优化点 |"""
    
    plan_result = get_ai_response(plan_prompt, f"评估:{profile_result}\n旧计划:{old_plan}")
    if "Error" in plan_result:
        results_dict["error"] = plan_result
    else:
        write_md_file(username, "user_profile.md", profile_result)
        write_md_file(username, "fitness_plan.md", plan_result)
        results_dict["profile"] = profile_result
        results_dict["plan"] = plan_result
        results_dict["done"] = True
        
        # 发送微信推送
        push_content = f"""# 👤 客户档案：{username}
{new_info}

---

# 📊 AI 深度评估报告
{profile_result}

---

# 📋 私人定制健身方案
{plan_result}
"""
        send_pushplus_notification(f"[健身助手] 新客户方案：{username}", push_content)

# ==========================================
# 6. 渲染逻辑 (按顺序直接在顶层运行)
# ==========================================

# --- 侧边栏 ---
with st.sidebar:
    st.header("👤 客户中心")
    users = get_existing_users()
    if users:
        curr_idx = users.index(st.session_state.current_user) if st.session_state.current_user in users else 0
        selected_user = st.selectbox("选择已有客户", users, index=curr_idx)
        st.session_state.current_user = selected_user
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📖 查看方案"):
                p = read_md_file(selected_user, "user_profile.md")
                pl = read_md_file(selected_user, "fitness_plan.md")
                if p and pl:
                    st.session_state.results = {"profile": p, "plan": pl, "done": True}
                    st.session_state.page = "result"
                    st.rerun()
                else:
                    st.warning("暂无方案")
        with c2:
            if st.button("📝 修改信息"):
                st.session_state.page = "form"
                st.rerun()
    else:
        st.info("暂无记录")
    
    st.divider()
    if st.button("➕ 新建客户"):
        st.session_state.current_user = None
        st.session_state.page = "form"
        st.session_state.results = {}
        st.rerun()

# --- 主页面路由 ---
if st.session_state.page == "form":
    st.title("💪 AI 一对一健身助手")
    st.markdown("### 📝 录入/更新客户档案")
    
    with st.form("fitness_form"):
        username = st.text_input("0. 客户姓名/昵称 (必填)", value=st.session_state.current_user if st.session_state.current_user else "")
        c1, c2 = st.columns(2)
        with c1:
            gender_age = st.text_input("1. 性别 / 年龄")
            height_weight = st.text_input("2. 身高 / 体重")
            target_weight = st.text_input("3. 目标 / 预期")
        with c2:
            exercise_days = st.slider("8. 每周天数", 1, 7, 3)
            duration = st.text_input("9. 每次时长")
            equipment = st.selectbox("7. 环境", ["商业健身房", "宿舍/徒手", "有小器械", "户外"])
        core_goal = st.text_area("4. 核心诉求")
        injuries = st.text_area("6. 伤病情况")
        submitted = st.form_submit_button("🔥 开始定制")

    if submitted:
        if not username: st.error("姓名必填")
        else:
            st.session_state.current_user = username
            st.session_state.user_data = {"info": f"{gender_age}, {height_weight}, {target_weight}, {core_goal}, {injuries}, {equipment}, {exercise_days}天"}
            st.session_state.page = "loading"
            st.rerun()

elif st.session_state.page == "loading":
    st.title(f"🏃 正在为 {st.session_state.current_user} 制定方案...")
    bar = st.progress(0)
    tip_area = st.empty()
    
    if "ai_thread" not in st.session_state or not st.session_state.ai_thread.is_alive():
        st.session_state.results = {"done": False}
        thread = threading.Thread(target=run_ai_processing, args=(st.session_state.current_user, st.session_state.user_data["info"], st.session_state.results))
        st.session_state.ai_thread = thread
        thread.start()

    start = time.time()
    while not st.session_state.results.get("done"):
        elapsed = time.time() - start
        bar.progress(min(95, int((elapsed / 180) * 95)))
        tip_area.markdown(f'<div class="tip-card">{random.choice(FITNESS_TIPS)}</div>', unsafe_allow_html=True)
        if "error" in st.session_state.results:
            st.error(st.session_state.results["error"])
            break
        time.sleep(2)
        if st.session_state.results.get("done"): break

    if st.session_state.results.get("done"):
        bar.progress(100)
        time.sleep(0.5)
        st.session_state.page = "result"
        st.rerun()

elif st.session_state.page == "result":
    st.title(f"🎯 {st.session_state.current_user} 的定制方案")
    t1, t2 = st.tabs(["📊 评估报告", "📋 训练计划"])
    with t1: st.markdown(st.session_state.results.get("profile", ""))
    with t2: st.markdown(st.session_state.results.get("plan", ""))
    if st.button("⬅️ 返回修改"):
        st.session_state.page = "form"
        st.rerun()
