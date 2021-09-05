const WebSocket = require('ws');
const express = require('express');
const bodyParser = require('body-parser')
const app = express();
const port = 4000;
app.listen(port, () => console.log(`Listening on port ${port}...`));
app.use(bodyParser.json());

const wss = new WebSocket.Server({ port: 8080 });



wss.on('connection', (ws) => {

  app.post('/addWord', (req, res) => {
    const words = req.body.words;
    ws.send(words);
    res.send("Received Data!");
  });


  console.log('クライアントとの接続を確立しました');
  ws.on('message', (message) => {
    console.log(`クライアントよりメッセージを受信しました: ${message}`);
  });
});