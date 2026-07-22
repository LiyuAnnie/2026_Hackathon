# ⚖️ 勞資爭議數位證據鏈 Agent（Labor-Guard Agent）

黑客松模擬互動平台 — 使用 **Python + Streamlit** 打造，展示 AI Agent 蒐證解析 + Web3 區塊鏈存證 + 自動化調解申請書生成的完整概念驗證 (PoC)。

> ⚠️ 本專案為黑客松展示用途，區塊鏈上鏈與勞工局送件流程皆為**模擬**，非真實鏈上交易，生成之申請書亦非正式法律文件。

## 📌 專案簡介

勞資爭議中，勞工常面臨「口說無憑」、法規資訊不對等、申請流程繁瑣等困境。
本平台打造全天候陪伴勞工的 **Labor-Guard Agent**：

- 🤖 自動解析勞工上傳的對話紀錄、出勤資料，萃取違法事實與估算金額
- 📚 自動比對《勞動基準法》《勞動事件法》相關條文
- 🔗 將關鍵證據 SHA-256 雜湊上鏈，確保不可竄改、不可否認
- 📄 自動生成具參考效力的勞資爭議調解申請書，並模擬送件流程

## 🗂️ 四大分頁

| 分頁 | 說明 |
|---|---|
| 📌 專案緣起與痛點 | 說明痛點、解決方案與系統架構 |
| 💬 AI 智慧蒐證對話 | 模擬勞工與 Agent 對話，上傳證據、即時法規比對與金額試算 |
| 🔗 區塊鏈證據鏈 | 顯示證據 Hash、模擬上鏈狀態 / TxHash，並提供竄改驗證工具 |
| 📄 調解申請與送件 | 自動生成調解申請書預覽、下載，並模擬送件與進度追蹤 |

## 🚀 本機執行方式

```bash
# 1. 建立虛擬環境（可選）
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. 安裝套件
pip install -r requirements.txt

# 3. 啟動 Streamlit
streamlit run app.py
```

啟動後瀏覽器會自動開啟 `http://localhost:8501`。

## ☁️ 部署到 Streamlit Community Cloud

1. 將本專案上傳至 GitHub repository（含 `app.py`、`requirements.txt`）。
2. 前往 [share.streamlit.io](https://share.streamlit.io)，使用 GitHub 帳號登入。
3. 點選 **New app**，選擇你的 repository、分支，Main file path 填 `app.py`。
4. 點選 **Deploy**，即可取得公開網址分享給評審。

## 📁 專案結構

```
labor-dispute-agent/
├── app.py              # 主程式（Streamlit 應用）
├── requirements.txt     # Python 套件需求
└── README.md            # 專案說明文件
```

## 🛠️ 技術重點

- **前端 / 互動**：Streamlit（多分頁、chat_input、file_uploader、session_state）
- **證據雜湊**：Python 內建 `hashlib.sha256`
- **區塊鏈上鏈**：以模擬 TxHash（可替換為實際串接 Polygon / Ethereum 測試網 SDK，如 web3.py）
- **法規比對**：規則式關鍵字比對（Demo 用，正式版可替換為 LLM / RAG 引擎串接勞基法資料庫）

## 📄 授權

本專案僅供黑客松展示與教育用途使用。
