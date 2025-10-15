from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN", "Az4jyxjh30uxm4r9FbSt4qk5tbVonYe0Pt2HAbKyEkPp8VHpgEkRK/NF4FpRcQJCazAjS8YEYY7TKUoSUmysRNBpe73UApRBl6IDpRb0OTYLbdsgw2CTClpAh90iQLW+YSnKgw89r+WKEOOyV/6AygdB04t89/1O/w1cDnyilFU=")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET", "7fde77933da5605b5dad9d16b254fa45")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --- 基本首頁（測試是否正常部署）---
@app.route("/", methods=["GET"])
def home():
    return "LINE BOT is running ✅"

# --- Webhook 主要路由 ---
@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 的簽章
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    # 驗證簽章正確性
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# --- 處理訊息事件 ---
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text

    if "放鬆" in user_msg:
        reply_text = "推薦你這款療癒香氛蠟燭 🕯️"
    elif "開心" in user_msg:
        reply_text = "太好了～希望你今天都能保持笑容 😊"
    elif "難過" in user_msg:
        reply_text = "想跟我聊聊嗎？我可以推薦療癒小物 💛"
    else:
        reply_text = "可以告訴我你今天的心情嗎？"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# ✅ 不要加 app.run()！！
# Vercel 會自動執行 app 這個物件
