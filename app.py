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
# 自訂樣式 (現代化 UI)
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    .main {
        background-color: #0f1117;
    }
    .stApp {
        background: linear-gradient(180deg, #0b0e14 0%, #12151f 100%);
    }
    h1, h2, h3 {
        color: #f5f7fa;
        font-weight: 700;
    }
    p, li, span, label {
        color: #cbd3e1;
    }
    .hero-card {
        background: linear-gradient(135deg, #1b2130 0%, #232b3d 100%);
        border-radius: 16px;
        padding: 28px 32px;
        border: 1px solid #2c3346;
        margin-bottom: 18px;
    }
    .pain-card {
        background: #171b26;
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .solution-card {
        background: #171b26;
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .evidence-panel {
        background: #171b26;
        border: 1px solid #2c3346;
        border-radius: 14px;
        padding: 20px;
    }
    .law-tag {
        display: inline-block;
        background: #1e293b;
        color: #7dd3fc;
        border: 1px solid #334155;
        border-radius: 999px;
        padding: 4px 12px;
        margin: 4px 6px 4px 0;
        font-size: 0.85rem;
    }
    .status-chip-done {
        background: #052e16;
        color: #4ade80;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.85rem;
        border: 1px solid #166534;
    }
    .status-chip-pending {
        background: #1e293b;
        color: #facc15;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.85rem;
        border: 1px solid #78716c;
    }
    .hash-mono {
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 0.8rem;
        color: #93c5fd;
        word-break: break-all;
    }
    .timeline-item {
        padding: 10px 0 10px 20px;
        border-left: 2px solid #334155;
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
        background: #22c55e;
    }
    .timeline-item.pending::before {
        background: #facc15;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Session State 初始化
# ----------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------
# 工具函式
# ----------------------------------------------------------------------------
def sha256_of_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fake_tx_hash() -> str:
    return "0x" + "".join(random.choices("0123456789abcdef", k=64))


def extract_case_facts(user_text: str):
    """
    簡易關鍵字比對，模擬 Agent 從對話中萃取違法事實與法規。
    這裡以規則式模擬取代真正 NLP / LLM 呼叫，方便黑客松展示不需外部 API。
    """
    text = user_text.lower()
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

    if any(k in user_text for k in ["解雇", "資遣", "開除", "фired", "fired"]):
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


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚖️ Labor-Guard Agent")
    st.caption("勞資爭議數位證據鏈 Agent · 黑客松模擬展示")
    st.markdown("---")
    st.markdown(
        """
        **平台流程**
        1. 📌 專案緣起與痛點
        2. 💬 AI 智慧蒐證對話
        3. 🔗 區塊鏈證據鏈
        4. 📄 調解申請與送件
        """
    )
    st.markdown("---")
    st.info("本平台為概念驗證 (PoC) / 黑客松模擬展示，區塊鏈上鏈與送件流程皆為模擬，非正式法律文件或真實鏈上交易。")

# ----------------------------------------------------------------------------
# 分頁
# ----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📌 專案緣起與痛點",
        "💬 AI 智慧蒐證對話",
        "🔗 區塊鏈證據鏈",
        "📄 調解申請與送件",
    ]
)

# ============================================================================
# 分頁一：專案緣起與痛點
# ============================================================================
with tab1:
    st.markdown(
        """
        <div class="hero-card">
        <h1>⚖️ 勞資爭議數位證據鏈 Agent</h1>
        <p style="font-size:1.05rem;">
        打造全天候陪伴勞工的 <b>Labor-Guard Agent</b>，結合 AI 蒐證解析與 Web3 不可竄改證明，
        讓「口說無憑」的勞資爭議，變成「有憑有據」的正式申訴。
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("🩹 核心痛點與現行狀況")
        st.markdown(
            """
            <div class="pain-card">
            <b>舉證門檻高</b><br/>
            勞資爭議（如加班費未給付、違法解雇）時，勞工常面臨「口說無憑」的困境，
            且 LINE 對話紀錄、出勤截圖容易被資方質疑遭變造或刪除。
            </div>
            <div class="pain-card">
            <b>法規資訊不對等</b><br/>
            勞工往往不熟悉《勞動基準法》第 24 條（加班費）、第 38 條（特休）或
            《勞動事件法》相關舉證規定，導致協商時居於劣勢。
            </div>
            <div class="pain-card">
            <b>流程繁瑣</b><br/>
            撰寫勞資爭議調解申請書對一般勞工門檻極高，不知如何精準對應法條。
            </div>
            <div class="pain-card">
            <b>影響對象</b><br/>
            廣大受薪階級、中小企業勞工、非典型勞動者。
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.subheader("💡 AI Agent 解決方案")
        st.markdown(
            """
            <div class="solution-card">
            <b>自動化蒐證與解析</b><br/>
            智慧解析勞工上傳的對話檔、班表，自動萃取關鍵時間、未給付薪資金額。
            </div>
            <div class="solution-card">
            <b>法規對齊</b><br/>
            自動匹配勞基法條，生成具有說服力的「事實與理由」。
            </div>
            <div class="solution-card">
            <b>Web3 信任根基</b><br/>
            將關鍵證據（檔案 SHA-256 雜湊）上鏈，確保資方無法否定其真實性，
            提供法庭或勞工局調解時的強力數位證據。
            </div>
            <div class="solution-card">
            <b>閉環服務</b><br/>
            從對話蒐證 → 區塊鏈存證 → 自動生成調解申請書 → 模擬送件，一站式完成。
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("🧭 系統架構總覽")
    st.markdown(
        """
        ```
        勞工輸入 (對話 / 截圖 / 班表)
                │
                ▼
        💬 AI Agent：法規比對 + 事實萃取 + 金額試算
                │
                ▼
        🔗 區塊鏈存證：SHA-256 雜湊 + 模擬上鏈 (TxHash)
                │
                ▼
        📄 自動生成勞資爭議調解申請書 (含鏈上證據編號)
                │
                ▼
        🏛️ 模擬送交地方勞工局線上申訴系統
        ```
        """
    )

# ============================================================================
# 分頁二：AI 智慧蒐證對話
# ============================================================================
with tab2:
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

        st.markdown("##### 📎 上傳蒐證檔案（對話截圖 / 出勤紀錄）")
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
# 分頁三：區塊鏈證據鏈
# ============================================================================
with tab3:
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
# 分頁四：調解申請與送件
# ============================================================================
with tab4:
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
            if st.button("📮 一鍵送出至地方勞工局線上申訴系統（模擬）", type="primary"):
                with st.spinner("正在模擬送出申請..."):
                    time.sleep(1.5)
                st.session_state.submitted = True
                st.success("✅ 已模擬送出！申請書已進入下方進度追蹤。")

        st.markdown("---")
        st.markdown("##### 📊 進度追蹤 (Timeline Tracker)")

        step1_done = facts is not None
        step2_done = len(anchored_items) > 0
        step3_done = bool(applicant["name"]) and step1_done
        step4_done = st.session_state.submitted

        def timeline_row(label, done, extra=""):
            cls = "timeline-item" if done else "timeline-item pending"
            icon = "✅" if done else "⏳"
            st.markdown(
                f'<div class="{cls}"><b>{icon} {label}</b><br/><span style="color:#94a3b8;">{extra}</span></div>',
                unsafe_allow_html=True,
            )

        timeline_row("Step 1：智慧蒐證與法規對齊", step1_done)
        timeline_row(
            "Step 2：數位證據區塊鏈存證",
            step2_done,
            f"已上鏈 {len(anchored_items)} / {len(evidence_items)} 份證據"
            + (f"，最新 TxHash: {anchored_items[-1]['tx_hash']}" if anchored_items else ""),
        )
        timeline_row("Step 3：調解申請書產出", step3_done)
        timeline_row(
            "Step 4：已送交主管機關 / 等待勞工局受理",
            step4_done,
            "已模擬送出，等待受理中" if step4_done else "尚未送出",
        )

st.markdown("---")
st.caption("⚖️ Labor-Guard Agent · 勞資爭議數位證據鏈 Agent · 黑客松模擬展示專案（Proof of Concept）")
