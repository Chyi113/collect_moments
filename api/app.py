from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# --- 直接使用真實 Token / Secret ---
CHANNEL_ACCESS_TOKEN = "Az4jyxjh30uxm4r9FbSt4qk5tbVonYe0Pt2HAbKyEkPp8VHpgEkRK/NF4FpRcQJCazAjS8YEYY7TKUoSUmysRNBpe73UApRBl6IDpRb0OTYLbdsgw2CTClpAh90iQLW+YSnKgw89r+WKEOOyV/6AygdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "7fde77933da5605b5dad9d16b254fa45"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "✅ LINE BOT Flask app is running on Vercel"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if "放鬆" in msg:
        reply = "推薦你這款療癒香氛蠟燭 🕯️"
    elif "開心" in msg:
        reply = "太好了～希望你今天都能保持笑容 😊"
    elif "難過" in msg:
        reply = "想跟我聊聊嗎？我可以推薦療癒小物 💛"
    else:
        reply = "可以告訴我你今天的心情嗎？"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
