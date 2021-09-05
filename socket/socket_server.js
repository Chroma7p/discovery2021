const WebSocket = require('ws');
const express = require('express');
const bodyParser = require('body-parser')
const app = express();
const port = 4000;
const cors = require('cors')
app.listen(port, () => console.log(`Listening on port ${port}...`));
app.use(bodyParser.json());

const wss = new WebSocket.Server({ port: 8080 });

const corsOptions = {
  origin: '*',
  optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
}


wss.on('connection', (ws) => {

  app.post('/addWord', cors(corsOptions), (req, res) => {
    const words = req.body.words;
    console.log(words)
    ws.clients.forEach((client) => {
      if (client.readyState == WebSocket.OPEN && data != undefined) {
        words.forEach((word) => {
          client.send(word)
        })
      }
    })
    res.send("Received Data");
  });


  console.log('クライアントとの接続を確立しました');
  ws.on('message', (message) => {
    console.log(`クライアントよりメッセージを受信しました: ${message}`);
  });
});