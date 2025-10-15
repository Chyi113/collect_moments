import express from "express";
import { Client, middleware } from "@line/bot-sdk";

const config = {
  channelAccessToken: "你的 Channel Access Token",
  channelSecret: "你的 Channel Secret"
};

const app = express();
const client = new Client(config);

app.post("/webhook", middleware(config), (req, res) => {
  Promise.all(req.body.events.map(handleEvent))
    .then((result) => res.json(result));
});

async function handleEvent(event) {
  if (event.type !== "message" || event.message.type !== "text") {
    return Promise.resolve(null);
  }

  // 當使用者傳訊息時，回覆開啟 LIFF 的按鈕
  const message = {
    type: "template",
    altText: "開啟 Collect Moments",
    template: {
      type: "buttons",
      text: "點擊下方按鈕開啟你的幸福牆 🌈",
      actions: [
        {
          type: "uri",
          label: "開啟 LIFF",
          uri: "https://liff.line.me/你的LIFF_ID" // ← 換成剛才複製的 LIFF ID
        }
      ]
    }
  };

  return client.replyMessage(event.replyToken, message);
}

app.listen(3000, () => console.log("✅ Bot running on port 3000"));
