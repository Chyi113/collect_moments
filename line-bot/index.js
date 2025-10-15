import express from "express";
import { Client, middleware } from "@line/bot-sdk";

const config = {
  channelAccessToken: "Az4jyxjh30uxm4r9FbSt4qk5tbVonYe0Pt2HAbKyEkPp8VHpgEkRK/NF4FpRcQJCazAjS8YEYY7TKUoSUmysRNBpe73UApRBl6IDpRb0OTYLbdsgw2CTClpAh90iQLW+YSnKgw89r+WKEOOyV/6AygdB04t89/1O/w1cDnyilFU=",
  channelSecret: "7fde77933da5605b5dad9d16b254fa45"
};

const client = new Client(config);
const app = express();

app.post("/api/webhook", middleware(config), async (req, res) => {
  try {
    await Promise.all(req.body.events.map(handleEvent));
    res.status(200).end(); // ✅ 回應 200 給 LINE，避免出現 405 錯誤
  } catch (err) {
    console.error(err);
    res.status(500).end();
  }
});

async function handleEvent(event) {
  if (event.type !== "message" || event.message.type !== "text") {
    return;
  }

  // 當使用者傳訊息時，回覆一個 LIFF 連結按鈕
  const replyMessage = {
    type: "template",
    altText: "開啟 Collect Moments",
    template: {
      type: "buttons",
      text: "點擊下方按鈕開啟你的幸福牆 🌈",
      actions: [
        {
          type: "uri",
          label: "開啟 LIFF",
          uri: "https://liff.line.me/2008295999-yQYmRPP6"
        }
      ]
    }
  };

  await client.replyMessage(event.replyToken, replyMessage);
}

export default app;
