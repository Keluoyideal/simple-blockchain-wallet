#  簡易區塊鏈錢包系統

本專案為一個以 Python Flask 開發的簡易區塊鏈錢包系統，結合前端網頁 UI 提供：
- 私鑰/公鑰錢包生成
- 基於 ECDSA 的交易簽章
- 區塊鏈共識機制與節點同步
- 區塊鏈挖礦與交易紀錄查詢

## 功能特色

-  錢包私鑰、公鑰生成
-  使用 ECDSA 進行交易簽章與驗證
-  區塊資料儲存與鏈接
-  一鍵挖礦、共識機制、自動同步
-  分散式節點互聯
-  可查詢特定地址的交易紀錄
-  直覺式前端 UI，支援 Bootstrap 響應式

##  使用技術

- Python 3.x
- Flask
- Bootstrap 5
- ECDSA（數位簽章）
- Axios (前端與後端互動)
- JSON 傳輸協定

##  安裝與執行

```bash
# 建立虛擬環境
python -m venv .venv
source .venv/bin/activate  # Windows 用者改為 .venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 啟動伺服器（可開多個 port 作為節點）
python app.py
