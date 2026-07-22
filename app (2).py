# -*- coding: utf-8 -*-
"""
勞資爭議數位證據鏈 Agent
Labor Dispute Digital Evidence Chain Agent

黑客松模擬互動平台 - Streamlit 版本
"""

import streamlit as st
import hashlib
import random
import time
import io
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------
# 基本頁面設定
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="勞資爭議數位證據鏈 Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# 自訂樣式 (現代化 UI・多巴胺色系)
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* 多巴胺色系：明亮飽和但柔和的暖色背景，取代原本暗沉主題 */
    .main {
        background-color: #FFF8F1;
    }
    .stApp {
        background: linear-gradient(160deg, #FFF6EE 0%, #FFF0F5 45%, #F0FBFF 100%);
    }
    h1, h2, h3 {
        color: #2D2A4A;
        font-weight: 800;
    }
    p, li, span, label {
        color: #4A4560;
    }
    .app-logo-bar {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 10px 4px 18px 4px;
        margin-bottom: 6px;
        border-bottom: 2px solid #FFD6E8;
    }
    .app-logo-bar .logo-emoji {
        font-size: 2.1rem;
    }
    .app-logo-bar .logo-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #7B2D6B;
        margin: 0;
    }
    .app-logo-bar .logo-sub {
        font-size: 0.85rem;
        color: #9A6FA0;
        margin: 0;
    }
    .hero-card {
        background: linear-gradient(135deg, #FFD6E8 0%, #FFE9C7 55%, #C8F4E9 100%);
        border-radius: 18px;
        padding: 28px 32px;
        border: 1px solid #FFD1E3;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(255, 141, 161, 0.18);
    }
    .hero-card h1 {
        color: #7B2D6B;
    }
    .pain-card {
        background: #FFFFFF;
        border-left: 5px solid #FF6B6B;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.10);
    }
    .solution-card {
        background: #FFFFFF;
        border-left: 5px solid #06D6A0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(6, 214, 160, 0.12);
    }
    .step-card {
        background: #FFFFFF;
        border-left: 5px solid #7B61FF;
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(123, 97, 255, 0.10);
    }
    .step-card .step-num {
        display: inline-block;
        background: linear-gradient(90deg, #FF6B9D 0%, #FFD23F 100%);
        color: #fff;
        font-weight: 800;
        border-radius: 999px;
        width: 26px;
        height: 26px;
        text-align: center;
        line-height: 26px;
        margin-right: 10px;
        font-size: 0.85rem;
    }
    .evidence-panel {
        background: #FFFFFF;
        border: 1px solid #FFE1EC;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(123, 97, 255, 0.08);
    }
    .law-tag {
        display: inline-block;
        background: #EFEBFF;
        color: #6D4CE0;
        border: 1px solid #D8CCFF;
        border-radius: 999px;
        padding: 4px 12px;
        margin: 4px 6px 4px 0;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-chip-done {
        background: #DEFBEF;
        color: #0B9D6F;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.85rem;
        border: 1px solid #8CE9C9;
        font-weight: 600;
    }
    .status-chip-pending {
        background: #FFF3D6;
        color: #C98A00;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.85rem;
        border: 1px solid #FFD976;
        font-weight: 600;
    }
    .hash-mono {
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 0.8rem;
        color: #4C6FE0;
        word-break: break-all;
    }
    .timeline-item {
        padding: 10px 0 10px 20px;
        border-left: 2px solid #FFD1E3;
        margin-left: 8px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 14px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #06D6A0;
    }
    .timeline-item.pending::before {
        background: #FFC53D;
    }
    .case-id-badge {
        display: inline-block;
        background: linear-gradient(90deg, #7B61FF 0%, #4CC9F0 100%);
        color: #fff;
        font-weight: 700;
        border-radius: 10px;
        padding: 6px 16px;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        border: none;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #FF6B9D 0%, #FF9F45 100%);
        color: #fff;
    }
    /* 側邊欄導覽按鈕 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFEFF6 0%, #F0FBFF 100%);
    }
    section[data-testid="stSidebar"] .stRadio > label {
        font-weight: 700;
        color: #7B2D6B;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 6px;
        border: 1px solid #FFE1EC;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_logo_header():
    st.markdown(
        """
        <div class="app-logo-bar">
            <div class="logo-emoji">⚖️</div>
            <div>
                <p class="logo-title">Labor-Guard Agent</p>
                <p class="logo-sub">勞資爭議數位證據鏈 Agent · 黑客松模擬展示平台</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# 內建測試帳號
# ----------------------------------------------------------------------------
DEMO_ACCOUNTS = {
    "labor01": "test1234",
    "demo": "demo1234",
}

# ----------------------------------------------------------------------------
# Session State 初始化
# ----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "case_id" not in st.session_state:
    st.session_state.case_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "agent",
            "content": "您好，我是 Labor-Guard Agent 👋 我會全程陪伴您完成蒐證與法規比對。"
                       "請簡述您目前遇到的勞資問題（例如：加班費未給付、無預警解雇、特休未給等）。",
        }
    ]

if "evidence_items" not in st.session_state:
    st.session_state.evidence_items = []  # 每筆: dict(name, size, hash, anchored, tx_hash, time)

if "case_facts" not in st.session_state:
    st.session_state.case_facts = None  # 由對話萃取出的結構化資料

if "applicant_info" not in st.session_state:
    st.session_state.applicant_info = {
        "name": "",
        "id_no": "",
        "phone": "",
        "address": "",
        "employer": "",
        "employer_addr": "",
    }

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "submitted_time" not in st.session_state:
    st.session_state.submitted_time = None


# ----------------------------------------------------------------------------
# 工具函式
# ----------------------------------------------------------------------------
def sha256_of_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fake_tx_hash() -> str:
    return "0x" + "".join(random.choices("0123456789abcdef", k=64))


def gen_case_id(username: str) -> str:
    seed = f"{username}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(0, 9999)}"
    digest = hashlib.sha1(seed.encode()).hexdigest()[:6].upper()
    return f"LDC-{datetime.now().year}-{digest}"


def extract_case_facts(user_text: str):
    """
    簡易關鍵字比對，模擬 Agent 從對話中萃取違法事實與法規。
    這裡以規則式模擬取代真正 NLP / LLM 呼叫，方便黑客松展示不需外部 API。
    """
    facts = {
        "violation": [],
        "laws": [],
        "estimated_amount": 0,
        "overtime_hours": 0,
    }

    if any(k in user_text for k in ["加班", "延長工時", "超時"]):
        hours = random.randint(12, 40)
        hourly_wage = 200
        amount = int(hours * hourly_wage * 1.34)  # 概略估算加成
        facts["violation"].append("延長工作時間未依法給付加班費（疑似違反勞基法第 24 條）")
        facts["laws"].append("勞動基準法 第 24 條（延長工時工資加給）")
        facts["laws"].append("勞動事件法 第 34 條（雇主出勤紀錄推定義務）")
        facts["overtime_hours"] = hours
        facts["estimated_amount"] += amount

    if any(k in user_text for k in ["解雇", "資遣", "開除", "fired"]):
        facts["violation"].append("疑似違法終止勞動契約（未依勞基法第 11 / 12 條事由，或未給付資遣費）")
        facts["laws"].append("勞動基準法 第 11 條 / 第 12 條（終止契約事由）")
        facts["laws"].append("勞動基準法 第 17 條（資遣費計算）")

    if any(k in user_text for k in ["特休", "休假"]):
        facts["violation"].append("疑似特別休假未依法給予或未折算工資")
        facts["laws"].append("勞動基準法 第 38 條（特別休假）")

    if any(k in user_text for k in ["踢", "封鎖", "刪除對話", "群組"]):
        facts["violation"].append("證據可能遭湮滅風險，建議立即蒐證並上鏈保存")

    if not facts["violation"]:
        facts["violation"].append("尚待更多資訊，建議上傳相關對話紀錄或出勤資料以利判斷")

    return facts


def render_status_chip(done: bool):
    if done:
        return '<span class="status-chip-done">🟢 已完成</span>'
    return '<span class="status-chip-pending">⏳ 進行中</span>'


def timeline_row(label, done, extra=""):
    cls = "timeline-item" if done else "timeline-item pending"
    icon = "✅" if done else "⏳"
    st.markdown(
        f'<div class="{cls}"><b>{icon} {label}</b><br/><span style="color:#8b8698;">{extra}</span></div>',
        unsafe_allow_html=True,
    )


# ============================================================================
# 登入頁面
# ============================================================================
def render_login_page():
    render_logo_header()

    col_l, col_mid, col_r = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown(
            "<p style='text-align:center; font-size:1.05rem; color:#4A4560; margin:8px 0 22px 0;'>"
            "👋 歡迎使用 Labor-Guard Agent，請先登入勞工帳號，開始您的智慧蒐證與調解申請流程。"
            "</p>",
            unsafe_allow_html=True,
        )

        st.subheader("🔐 勞工帳號登入")
        with st.form("login_form"):
            username = st.text_input("帳號", placeholder="例如：labor01")
            password = st.text_input("密碼", type="password", placeholder="請輸入密碼")
            submitted = st.form_submit_button("登入", type="primary", use_container_width=True)

        if submitted:
            if username in DEMO_ACCOUNTS and DEMO_ACCOUNTS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.case_id = gen_case_id(username)
                st.success("登入成功，正在進入平台...")
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請再試一次。")

        st.info(
            "🧪 **測試用內建帳號**\n\n"
            "帳號：`labor01` ／ 密碼：`test1234`\n\n"
            "帳號：`demo` ／ 密碼：`demo1234`"
        )


# ============================================================================
# 使用說明 / Demo 劇情頁
# ============================================================================
def render_demo_story(compact: bool = False):
    steps = [
        ("勞工登入平台", "使用內建測試帳號（labor01 / test1234）登入 Labor-Guard Agent。"),
        ("與 Agent 對話描述狀況", "在「💬 AI 智慧蒐證對話」分頁輸入：「公司未支付加班費」，Agent 會開始引導蒐證。"),
        ("上傳關鍵證據", "上傳 LINE 對話截圖、薪資單、打卡紀錄等檔案，系統會自動計算每份檔案的 SHA-256 指紋。"),
        ("Agent 自動整理並比對法規", "Agent 解析上傳內容，辨識缺漏資料，並自動比對《勞動基準法》第 24 條等相關條文，估算應補發金額。"),
        ("產生調解申請書草稿", "切換到「📄 調解申請與送件」分頁，系統依蒐證結果自動產出結構化申請書草稿。"),
        ("使用者確認並授權送件", "勞工本人檢視草稿內容無誤後，按下「確認送出」按鈕，完成 Human Approval 人工確認機制。"),
        ("證據與操作紀錄上鏈", "前往「🔗 區塊鏈證據鏈」分頁，一鍵將證據雜湊與送件操作紀錄寫入區塊鏈，系統顯示交易雜湊（TxHash）並驗證成功。"),
        ("查看案件進度", "在「📊 我的案件」分頁，隨時查看目前送件與處理進度，追蹤四大階段是否完成。"),
    ]

    for i, (title, desc) in enumerate(steps, start=1):
        st.markdown(
            f"""
            <div class="step-card">
            <span class="step-num">{i}</span><b>{title}</b>
            <div style="margin-top:6px; margin-left:36px; color:#5c5770;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not compact:
        st.markdown("---")
        st.subheader("🗂️ 分頁功能對照")
        st.markdown(
            """
            | 分頁 | 對應 Demo 步驟 | 功能重點 |
            |---|---|---|
            | 💬 AI 智慧蒐證對話 | 步驟 2 - 3 | 與 Agent 對話描述問題、上傳證據檔案、即時法規比對與金額試算 |
            | 🔗 區塊鏈證據鏈 | 步驟 7 | 證據雜湊上鏈、TxHash 顯示、竄改驗證工具 |
            | 📄 調解申請與送件 | 步驟 5 - 6 | 自動生成申請書草稿、人工確認並授權送出 |
            | 📊 我的案件 | 步驟 8 | 案件編號、四大階段進度追蹤、送件狀態總覽 |
            """
        )

        st.markdown("---")
        st.subheader("💡 操作小提醒")
        st.markdown(
            """
            - 建議依照以下順序操作：**對話 → 上傳證據 → 上鏈存證 → 產出申請書 → 確認送出 → 查看進度**。
            - 「上鏈」與「送出至勞工局」流程皆為**模擬展示**，不會真的寫入公開區塊鏈或送出至政府系統。
            - 若要重新示範，重新整理頁面或登出後再登入，即可清空本次示範資料（僅限單次瀏覽器工作階段）。
            """
        )


def page_instructions():
    render_logo_header()
    st.subheader("📖 平台使用說明")
    st.caption("依照以下步驟操作，5 分鐘體驗完整的智慧蒐證、區塊鏈存證與調解申請流程。")
    render_demo_story(compact=False)


# ============================================================================
# 分頁：AI 智慧蒐證對話
# ============================================================================
def page_chat():
    render_logo_header()
    st.subheader("💬 勞工智慧對話與蒐證")
    col_chat, col_panel = st.columns([1.2, 1], gap="large")

    with col_chat:
        st.markdown("##### 對話機器人 (Chat Interface)")
        chat_container = st.container(height=420, border=True)
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "agent":
                    with st.chat_message("assistant", avatar="⚖️"):
                        st.write(msg["content"])
                else:
                    with st.chat_message("user", avatar="🧑"):
                        st.write(msg["content"])

        user_input = st.chat_input("請描述您遇到的狀況，例如：老闆常叫我加班到晚上10點但沒給加班費...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            facts = extract_case_facts(user_input)
            st.session_state.case_facts = facts

            reply_lines = ["了解，我已初步分析您的狀況："]
            for v in facts["violation"]:
                reply_lines.append(f"• {v}")
            reply_lines.append(
                "請上傳最近三個月的 LINE 對話截圖、上下班打卡記錄（或門禁卡紀錄），"
                "我來幫您計算應得金額並比對法規，並可將證據存證上鏈。"
            )
            st.session_state.chat_history.append(
                {"role": "agent", "content": "\n".join(reply_lines)}
            )
            st.rerun()

        st.markdown("##### 📎 上傳蒐證檔案（對話截圖 / 薪資單 / 打卡紀錄）")
        uploaded_files = st.file_uploader(
            "支援圖片、PDF、文字檔等格式",
            type=["png", "jpg", "jpeg", "pdf", "txt", "csv"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            for f in uploaded_files:
                content = f.read()
                h = sha256_of_bytes(content)
                already = any(item["name"] == f.name and item["hash"] == h for item in st.session_state.evidence_items)
                if not already:
                    st.session_state.evidence_items.append(
                        {
                            "name": f.name,
                            "size": len(content),
                            "hash": h,
                            "anchored": False,
                            "tx_hash": None,
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
            st.success(f"已接收 {len(uploaded_files)} 份檔案，並自動計算 SHA-256 指紋。請至「區塊鏈證據鏈」分頁完成上鏈存證。")

    with col_panel:
        st.markdown("##### ⚡ 即時證據解析面板 (Evidence Extraction Panel)")
        st.markdown('<div class="evidence-panel">', unsafe_allow_html=True)

        facts = st.session_state.case_facts
        if facts:
            st.markdown("**違法事實研判：**")
            for v in facts["violation"]:
                st.markdown(f"- {v}")

            if facts["overtime_hours"]:
                st.markdown("**估算加班時數：**")
                st.metric("加班時數", f"{facts['overtime_hours']} 小時")

            if facts["estimated_amount"]:
                st.markdown("**估算應補發金額：**")
                st.metric("估算金額 (TWD)", f"$ {facts['estimated_amount']:,}")

            if facts["laws"]:
                st.markdown("**法規依據提示：**")
                law_html = "".join(f'<span class="law-tag">{law}</span>' for law in set(facts["laws"]))
                st.markdown(law_html, unsafe_allow_html=True)
        else:
            st.info("尚未偵測到具體案件內容。請在左方輸入您遭遇的狀況，Agent 會自動萃取關鍵事實與法規。")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("##### 📂 已上傳證據數")
        st.metric("證據檔案數量", len(st.session_state.evidence_items))


# ============================================================================
# 分頁：區塊鏈證據鏈
# ============================================================================
def page_blockchain():
    render_logo_header()
    st.subheader("🔗 區塊鏈驗證與證據鏈")
    st.caption("展現 Web3 技術應用，確保數位證據的不可否認性 (Non-repudiation)。以下上鏈流程為模擬展示。")

    col_a, col_b = st.columns([2, 1], gap="large")

    with col_a:
        st.markdown("##### 📋 證據清單表格 (Evidence Ledger)")
        if not st.session_state.evidence_items:
            st.warning("目前尚無證據檔案，請至「AI 智慧蒐證對話」分頁上傳檔案。")
        else:
            for idx, item in enumerate(st.session_state.evidence_items):
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**{item['name']}**  ·  {item['size']:,} bytes  ·  {item['time']}")
                        st.markdown(f'<span class="hash-mono">SHA-256: {item["hash"]}</span>', unsafe_allow_html=True)
                        if item["anchored"]:
                            st.markdown(
                                f'{render_status_chip(True)} &nbsp; TxHash: '
                                f'<span class="hash-mono">{item["tx_hash"]}</span>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(render_status_chip(False), unsafe_allow_html=True)
                    with c2:
                        if not item["anchored"]:
                            if st.button("上鏈存證", key=f"anchor_{idx}"):
                                with st.spinner("正在打包並寫入區塊鏈..."):
                                    time.sleep(1.2)
                                st.session_state.evidence_items[idx]["anchored"] = True
                                st.session_state.evidence_items[idx]["tx_hash"] = fake_tx_hash()
                                st.rerun()
                        else:
                            st.success("已上鏈")

            st.markdown("---")
            if st.button("🔒 一鍵將本次蒐證包打包並上鏈 (Anchor All)", type="primary"):
                with st.spinner("正在打包全部證據並寫入區塊鏈..."):
                    time.sleep(1.5)
                for item in st.session_state.evidence_items:
                    if not item["anchored"]:
                        item["anchored"] = True
                        item["tx_hash"] = fake_tx_hash()
                st.success("全部證據已完成上鏈存證！")
                st.rerun()

    with col_b:
        st.markdown("##### 🔍 驗證工具")
        st.caption("上傳原始檔案，系統會計算 Hash 並與已存證紀錄比對，證明檔案自蒐集以來未被修改過。")
        verify_file = st.file_uploader("上傳要驗證的檔案", type=None, key="verify_uploader")
        if verify_file:
            content = verify_file.read()
            h = sha256_of_bytes(content)
            match = next((item for item in st.session_state.evidence_items if item["hash"] == h), None)
            st.markdown(f'<span class="hash-mono">計算出的 Hash：{h}</span>', unsafe_allow_html=True)
            if match:
                st.success(f"✅ 驗證成功！此檔案與存證紀錄「{match['name']}」完全一致，未遭竄改。")
                if match["anchored"]:
                    st.markdown(
                        f'鏈上交易：<span class="hash-mono">{match["tx_hash"]}</span>',
                        unsafe_allow_html=True,
                    )
            else:
                st.error("⚠️ 查無相符的存證紀錄，此檔案內容與已上傳證據不一致，或尚未上傳存證。")

        st.markdown("---")
        st.markdown("##### 🌐 模擬鏈上瀏覽器")
        st.caption("（模擬 Polygon / Ethereum 測試網畫面）")
        anchored_count = sum(1 for i in st.session_state.evidence_items if i["anchored"])
        st.metric("已上鏈證據數", anchored_count)
        st.metric("待處理證據數", len(st.session_state.evidence_items) - anchored_count)


# ============================================================================
# 分頁：調解申請與送件
# ============================================================================
def page_application():
    render_logo_header()
    st.subheader("📄 勞資調解申請書生成與送件")

    st.markdown("##### 📝 申請人 / 相對人基本資料")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.applicant_info["name"] = st.text_input(
            "申請人姓名", st.session_state.applicant_info["name"]
        )
        st.session_state.applicant_info["id_no"] = st.text_input(
            "身分證字號（後三碼將於預覽中遮蔽）", st.session_state.applicant_info["id_no"]
        )
        st.session_state.applicant_info["phone"] = st.text_input(
            "聯絡電話", st.session_state.applicant_info["phone"]
        )
        st.session_state.applicant_info["address"] = st.text_input(
            "通訊地址", st.session_state.applicant_info["address"]
        )
    with c2:
        st.session_state.applicant_info["employer"] = st.text_input(
            "相對人（公司）名稱", st.session_state.applicant_info["employer"]
        )
        st.session_state.applicant_info["employer_addr"] = st.text_input(
            "公司地址", st.session_state.applicant_info["employer_addr"]
        )

    st.markdown("---")

    facts = st.session_state.case_facts
    evidence_items = st.session_state.evidence_items
    anchored_items = [i for i in evidence_items if i["anchored"]]

    if not facts:
        st.info("請先至「AI 智慧蒐證對話」分頁與 Agent 對話，讓系統萃取案件事實。")
    else:
        st.markdown("##### 📄 表單預覽區 (Document Preview)")

        applicant = st.session_state.applicant_info
        masked_id = (applicant["id_no"][:-3] + "***") if len(applicant["id_no"]) > 3 else applicant["id_no"]

        request_item = "請求給付加班費新台幣 {:,} 元".format(facts["estimated_amount"]) if facts["estimated_amount"] else "請求資方依法改善並補償相關損失"

        law_refs = "、".join(sorted(set(facts["laws"]))) if facts["laws"] else "（尚待補充相關法條）"
        evidence_refs = "、".join(f"證據編號 #{idx+1}（{item['name']}）" for idx, item in enumerate(anchored_items)) or "（尚無已上鏈證據）"

        with st.container(border=True):
            st.markdown(f"""
### 勞資爭議調解申請書（模擬預覽）

**申請人資訊**
- 姓名：{applicant['name'] or '（未填寫）'}
- 身分證字號：{masked_id or '（未填寫）'}
- 聯絡電話：{applicant['phone'] or '（未填寫）'}
- 通訊地址：{applicant['address'] or '（未填寫）'}

**相對人資訊**
- 公司名稱：{applicant['employer'] or '（未填寫）'}
- 公司地址：{applicant['employer_addr'] or '（未填寫）'}

**請求事項**

{request_item}

**事實及理由**

依申請人陳述及上傳之數位證據顯示：{"；".join(facts['violation'])}。

上開事實有經 SHA-256 雜湊處理並上鏈存證之數位證據可資佐證，該等證據具備不可竄改性
（Non-repudiation），相關證據編號如下：{evidence_refs}。

依法應適用之相關法條包含：{law_refs}。

爰依《勞資爭議處理法》規定，向　貴機關申請調解，敬請惠予受理，並促使相對人依法給付/改善，
以維護申請人合法權益。

此致

貴地方政府勞工局（處）

申請人：{applicant['name'] or '＿＿＿＿＿＿'}　　中華民國 {datetime.now().year - 1911} 年 {datetime.now().month} 月 {datetime.now().day} 日
            """)

        st.warning("⚠️ 本文件為黑客松模擬展示之申請書範本，非正式法律文件，實際申請請以當地勞工局規定格式為準，建議諮詢專業法律意見。")

        doc_text = f"""
勞資爭議調解申請書（模擬）

申請人：{applicant['name']}
身分證字號：{masked_id}
聯絡電話：{applicant['phone']}
通訊地址：{applicant['address']}

相對人（公司）：{applicant['employer']}
公司地址：{applicant['employer_addr']}

請求事項：
{request_item}

事實及理由：
依申請人陳述及上傳之數位證據顯示：{"；".join(facts['violation'])}。
上開事實有經 SHA-256 雜湊處理並上鏈存證之數位證據可資佐證，相關證據編號如下：
{evidence_refs}

適用法條：
{law_refs}

爰依《勞資爭議處理法》規定，向 貴機關申請調解，敬請惠予受理。

此致
貴地方政府勞工局（處）

申請人：{applicant['name']}
中華民國 {datetime.now().year - 1911} 年 {datetime.now().month} 月 {datetime.now().day} 日
"""

        col_dl, col_submit = st.columns(2)
        with col_dl:
            st.download_button(
                "⬇️ 下載申請書 (TXT)",
                data=doc_text.encode("utf-8"),
                file_name="勞資爭議調解申請書.txt",
                mime="text/plain",
            )
        with col_submit:
            st.caption("按下送出前請確認以上內容無誤（Human Approval 人工確認機制）")
            if st.button("✅ 確認內容並授權送出至地方勞工局線上申訴系統（模擬）", type="primary"):
                with st.spinner("正在模擬送出申請..."):
                    time.sleep(1.5)
                st.session_state.submitted = True
                st.session_state.submitted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("✅ 已模擬送出！請至「📊 我的案件」分頁查看最新進度。")


# ============================================================================
# 分頁：我的案件（進度追蹤）
# ============================================================================
def page_my_cases():
    render_logo_header()
    st.subheader("📊 我的案件")

    facts = st.session_state.case_facts
    evidence_items = st.session_state.evidence_items
    anchored_items = [i for i in evidence_items if i["anchored"]]
    applicant = st.session_state.applicant_info

    col_id, col_status = st.columns([1, 1.4])
    with col_id:
        st.markdown(f'<span class="case-id-badge">案件編號：{st.session_state.case_id}</span>', unsafe_allow_html=True)
        st.caption(f"登入帳號：{st.session_state.username}")
    with col_status:
        if st.session_state.submitted:
            st.success(f"目前狀態：已送出，等待勞工局受理中（送出時間：{st.session_state.submitted_time}）")
        elif facts:
            st.info("目前狀態：蒐證與草擬進行中，尚未送出申請")
        else:
            st.warning("目前狀態：尚未開始，請至「AI 智慧蒐證對話」分頁與 Agent 對話")

    st.markdown("---")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("已上傳證據", len(evidence_items))
    col_m2.metric("已上鏈證據", len(anchored_items))
    col_m3.metric(
        "估算應補發金額 (TWD)",
        f"$ {facts['estimated_amount']:,}" if facts and facts.get("estimated_amount") else "—",
    )
    col_m4.metric("送件狀態", "已送出" if st.session_state.submitted else "未送出")

    st.markdown("---")
    st.markdown("##### 📊 案件進度追蹤 (Timeline Tracker)")

    step1_done = facts is not None
    step2_done = len(anchored_items) > 0
    step3_done = bool(applicant["name"]) and step1_done
    step4_done = st.session_state.submitted

    timeline_row(
        "Step 1：智慧蒐證與法規對齊",
        step1_done,
        "已與 Agent 完成對話並萃取法規依據" if step1_done else "請至「AI 智慧蒐證對話」分頁開始",
    )
    timeline_row(
        "Step 2：數位證據區塊鏈存證",
        step2_done,
        f"已上鏈 {len(anchored_items)} / {len(evidence_items)} 份證據"
        + (f"，最新 TxHash: {anchored_items[-1]['tx_hash']}" if anchored_items else ""),
    )
    timeline_row(
        "Step 3：調解申請書產出",
        step3_done,
        "已填寫申請人資料並產出草稿" if step3_done else "請至「調解申請與送件」分頁填寫資料",
    )
    timeline_row(
        "Step 4：已送交主管機關 / 等待勞工局受理",
        step4_done,
        f"已於 {st.session_state.submitted_time} 模擬送出，等待受理中" if step4_done else "尚未送出",
    )

    st.markdown("---")
    if evidence_items:
        st.markdown("##### 📂 證據總覽")
        for idx, item in enumerate(evidence_items):
            status = "🟢 已上鏈" if item["anchored"] else "⏳ 尚未上鏈"
            st.markdown(f"- **{item['name']}** · {item['size']:,} bytes · {status}")
    else:
        st.caption("尚無已上傳的證據檔案。")


# ============================================================================
# 主程式路由
# ============================================================================
if not st.session_state.authenticated:
    render_login_page()
else:
    with st.sidebar:
        st.markdown("## ⚖️ Labor-Guard Agent")
        st.caption("勞資爭議數位證據鏈 Agent · 黑客松模擬展示")
        st.markdown(f"👤 歡迎，**{st.session_state.username}**")
        st.markdown(f'<span class="case-id-badge">{st.session_state.case_id}</span>', unsafe_allow_html=True)
        st.markdown("---")

        page = st.radio(
            "平台導覽",
            [
                "📖 使用說明",
                "💬 AI 智慧蒐證對話",
                "🔗 區塊鏈證據鏈",
                "📄 調解申請與送件",
                "📊 我的案件",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.info("本平台為概念驗證 (PoC) / 黑客松模擬展示，登入、區塊鏈上鏈與送件流程皆為模擬，非正式法律文件或真實鏈上交易。")

        st.markdown("---")
        if st.button("🚪 登出", use_container_width=True):
            for key in ["authenticated", "username", "case_id"]:
                st.session_state[key] = False if key == "authenticated" else None
            st.rerun()

    if page == "📖 使用說明":
        page_instructions()
    elif page == "💬 AI 智慧蒐證對話":
        page_chat()
    elif page == "🔗 區塊鏈證據鏈":
        page_blockchain()
    elif page == "📄 調解申請與送件":
        page_application()
    elif page == "📊 我的案件":
        page_my_cases()

    st.markdown("---")
    st.caption("⚖️ Labor-Guard Agent · 勞資爭議數位證據鏈 Agent · 黑客松模擬展示專案（Proof of Concept）")
