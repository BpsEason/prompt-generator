# 🎯 行銷內容生成 Prompt 模組化架構

本專案提供一套**生產級的 AI 行銷文案生成系統骨架**，旨在幫助行銷團隊和開發者高效、穩定地產出高品質文案。它巧妙結合 **FastAPI、Docker、YAML 模組庫與 GPT 模型**，實現了從模組化輸入、異步處理到自動化品質驗收的完整工作流程。無論是作為教學範例、團隊內部工具，或是進一步開發 AI 應用，這套架構都能提供堅實的基礎。

---

## ✨ 核心特色與優勢

*   **模組化 Prompt 組合**：以前所未有的靈活性，通過產品、風格、受眾、格式、CTA 等模組，快速定義和生成目標明確的行銷文案。
*   **異步處理 (Async/Await)**：底層 LLM 呼叫全面採用 `async/await` 異步模式，顯著提升 API 吞吐量和響應速度，滿足高併發請求的需求。
*   **集中式環境變數管理**：採用 `pydantic-settings` 庫，通過 `.env` 文件和系統環境變數，安全、靈活地管理敏感配置（如 LLM API 金鑰），易於部署和維護。
*   **YAML 模組庫，高度可擴充**：所有 Prompt 模組以 YAML 格式儲存，結構清晰，便於快速擴充、版本控管，並支援熱插拔更新。
*   **智能 Rubric 驗收標準**：內建基於 LLM 的自動化品質驗收機制，確保生成的文案在目標受眾、品牌風格、CTA 明確性、可讀性及可落地性上達到預期標準。
*   **Docker 化部署，無縫整合 CI/CD**：提供完整的 Dockerfile 和 docker-compose 配置，實現快速容器化部署，輕鬆整合現有 CI/CD 流程，簡化開發與生產環境的一致性。

---

## 🚀 快速啟動

在您的本地環境中，只需簡單幾步即可啟動這套強大的系統。

### 1. 安裝必要工具

請確保您的系統已安裝以下軟體：

*   **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**：用於容器化應用程式。
*   **[Docker Compose](https://docs.docker.com/compose/install/)**：用於多容器應用程式的定義和運行。

### 2. 設定環境變數

首先，複製專案根目錄下的 `.env.example` 檔案，並將其重新命名為 `.env`：

```bash
cp .env.example .env
```

然後，編輯 `.env` 檔案，填入您的 OpenAI 或兼容 GPT 模型的 API 金鑰。您也可以在此覆寫預設的模型名稱：

```env
# .env - 環境變數配置文件 (搭配 pydantic-settings)

# LLM 服務金鑰 (請替換為您的實際金鑰，建議從環境變數注入)
LLM_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # 範例金鑰，請替換為您的真實金鑰

# 範例：可以覆蓋 app/config.py 中的預設模型
GENERATION_MODEL="gpt-4o-mini" # 推薦使用最新的高效能模型
RUBRIC_CHECKER_MODEL="gpt-3.5-turbo" # Rubric 檢查器建議使用成本較低的模型
```

### 3. 啟動服務

進入專案根目錄，執行以下命令即可一鍵構建 Docker 映像並啟動所有服務：

```bash
docker-compose up --build -d
```
（` -d ` 參數表示在後台運行服務）

服務啟動後，您即可透過瀏覽器訪問 **`http://localhost:8000/docs`**，體驗由 FastAPI 自動生成的 Swagger UI 介面，直接測試 API 功能！

---

## 📂 專案結構概覽

清晰的模組化結構是本專案的基石，以下是核心目錄和檔案的功能說明：

```
prompt-generator/
├── app/                            # 應用程式核心邏輯
│   ├── main.py                   # FastAPI 主程式：定義 API 路由，整合 Prompt 生成與 Rubric 驗收流程。
│   ├── config.py                 # 環境變數與應用配置：使用 pydantic-settings 集中管理所有運行配置。
│   ├── prompt_engine.py          # Prompt 組合邏輯 (P1)：負責載入 YAML 模組，並根據用戶輸入拼接完整 Prompt。
│   ├── rubric_checker.py         # Rubric 驗收邏輯 (P3/P5)：定義評分標準，通過 LLM 自動評估生成內容品質。
│   ├── router.py                 # API 路由（可選）：用於模組化管理多個 API 路由，保持 main.py 簡潔。
│   └── utils/                    # 工具模組
│       └── llm_connector.py      # GPT 模型串接層 (P4)：抽象化 LLM API 呼叫，支援異步，方便替換不同模型或服務商。
├── app/templates/                  # YAML 模組庫 (P2)：存放產品、風格、受眾等可擴充的 Prompt 碎片定義。
├── tests/                          # 測試文件
│   └── test_rubric.py            # pytest 測試 (P5)：包含單元測試，驗證核心功能與邊界條件。
├── .env.example                    # 環境變數範例檔：引導使用者配置運行參數。
├── requirements.txt                # Python 套件清單：列出所有專案依賴。
├── Dockerfile                      # Docker 容器建置腳本：定義如何建立應用程式的 Docker 映像。
├── docker-compose.yml              # Docker Compose 配置：定義和運行多容器 Docker 應用程式。
└── README.md                       # 教學導覽文件：您正在閱讀的這份文件。
```

---

## 🧩 模組化輸入範例

本系統的核心亮點是其模組化的 Prompt 設計。使用者可以透過簡單的 JSON 請求，組合不同的模組參數來精確控制文案生成。

以下是可用的模組類型及其範例值：

| 模組類型 | 說明 | 範例值 |
| :------- | :--- | :--- |
| **style** | 文案的語氣風格，決定品牌形象傳達。 | `熱血`、`專業`、`幽默`、`溫馨` |
| **audience** | 目標閱讀客群，確保語氣和內容貼合受眾需求。 | `剛畢業的大學生`、`中小企業主`、`家庭主婦`、`科技愛好者` |
| **format** | 最終文案的輸出格式，適應不同行銷渠道。 | `社群貼文`、`EDM 標題`、`短影音腳本`、`產品介紹文` |
| **product** | 產品或服務的核心描述和賣點。 | `AI 簡報生成工具`、`會員訂閱服務`、`智能家居設備` |
| **cta** | 呼籲用戶採取行動的內容，引導轉化。 | `立即免費試用`、`限時搶購`、`瞭解更多`、`立即註冊` |

**範例 JSON 請求 (發送到 `http://localhost:8000/generate_marketing_content`)：**

```json
{
  "prompt": {
    "style": "熱血",
    "audience": "剛畢業的大學生",
    "format": "社群貼文",
    "product": "AI 簡報生成工具",
    "cta": "立即免費試用"
  }
}
```
發送此請求後，系統將自動拼接 Prompt，呼叫 LLM 生成文案，並進行品質驗收。

---

## ✅ Rubric 驗收標準：智能品質把關

為了確保生成內容的質量與一致性，系統內建了一套基於 LLM 的 Rubric 驗收標準。它會自動評估生成的文案，並給出結構化的分數報告。

**評估項目 (每項 0-5 分，滿分 20 分)：**

1.  **🎯 目標受眾吻合**：內容的語氣、詞彙及切入點是否精準貼合 Prompt 指定的客群需求。
2.  **🎨 品牌風格一致**：是否嚴格遵循 Prompt 指定的風格模組（如：熱血、專業），保持品牌語調的統一性。
3.  **📣 CTA 明確**：行動呼籲 (Call to Action) 是否清晰、具說服力，並且按照要求出現在文案的恰當位置（通常是結尾）。
4.  **📖 可讀性高**：文案是否段落清晰、語句流暢、無語法錯誤，易於目標受眾理解和消化。
5.  **🚀 可落地性**：內容是否能直接用於廣告、社群貼文、EDM 等行銷場景，無需額外修改即可發布。

**總分判斷標準**：

*   **總分 ≥ 12 分**：視為 **通過 (PASS)**。
*   **總分 < 12 分**：視為 **不通過 (FAIL)**。

---

## 🧪 測試與驗收

專案配備 `pytest` 測試框架，確保核心功能的正確性和穩定性。您可以在容器內部執行測試：

```bash
# 首先進入正在運行的容器 (如果容器名稱為 prompt_generator_app)
docker exec -it prompt_generator_app bash

# 在容器內部執行 pytest
pytest

# 退出容器
exit
```

**測試項目包含：**

*   **YAML 模組載入錯誤處理**：驗證 `PromptEngine` 在遇到格式錯誤的 YAML 文件時，能穩健處理而不會崩潰。
*   **Prompt 組合完整性**：確保 `PromptEngine` 能正確拼接 Prompt，包含所有必要的模組片段和關鍵詞。
*   **Rubric 評分 JSON 解析錯誤**：測試 `RubricChecker` 在 LLM 輸出非標準 JSON 格式時，能正確捕獲並處理錯誤。

---

## 🔧 延伸應用與未來展望

本專案不僅是一個現成的解決方案，更是一個極具潛力的開發基礎。您可以基於此架構進行以下擴展：

*   **串接真實 GPT API**：將 `llm_connector.py` 中的模擬呼叫替換為 [OpenAI Python SDK](https://github.com/openai/openai-python) 或 [Azure OpenAI Service](https://azure.microsoft.com/zh-tw/products/cognitive-services/openai-service) 的真實異步 API 呼叫。
*   **建立前端選單式 UI**：開發一個直觀的網頁前端介面（例如使用 **Vue 3** 或 React），讓行銷人員能夠通過選單點選組合 Prompt 模組，無需撰寫程式碼。
*   **擴充模組庫**：根據具體業務需求，新增更多模組類型（如 `語言`、`平台`、`季節情境`、`節慶活動` 等），無限豐富文案生成的多樣性。
*   **導入 CI/CD 測試流程**：將 `pytest` 測試整合到 GitHub Actions、GitLab CI/CD 或 Jenkins 等持續整合/持續部署流程中，自動化程式碼提交後的品質驗證。
*   **發佈為教學模板或 SaaS 工具**：將其打造成一個公開的教學模板，或進一步開發成一個商業化的 AI 文案生成 SaaS (Software as a Service) 平台。
