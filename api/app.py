from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('Az4jyxjh30uxm4r9FbSt4qk5tbVonYe0Pt2HAbKyEkPp8VHpgEkRK/NF4FpRcQJCazAjS8YEYY7TKUoSUmysRNBpe73UApRBl6IDpRb0OTYLbdsgw2CTClpAh90iQLW+YSnKgw89r+WKEOOyV/6AygdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7fde77933da5605b5dad9d16b254fa45')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    if "放鬆" in user_msg:
        reply = "推薦你這款療癒香氛蠟燭 🕯️"
    else:
        reply = "可以告訴我你今天的心情嗎？"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# 關鍵：新增這個 handler 讓 Vercel 認得
def handler(event, context):
    return app(event, context)
