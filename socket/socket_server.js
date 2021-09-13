
const fs = require("fs");
const cors = require('cors')
const bodyParser = require('body-parser');
const corsOptions = {
  origin: '*',
  optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
}


var express = require('express');
var app = express();
app.use(bodyParser.json());
var http = require('http').Server(app);
const io = require('socket.io')(http, {
  origins: ['*']
});
const PORT = process.env.PORT || 4000;
app.use(cors())


io.on('connection', function (socket) {
  console.log('connected');
  app.post('/addWord', (req, res) => {
    const words = req.body.words;
    console.log(words)
    for (let i = 0; i < words.length; i++) {
      io.emit('publish', words[i]);
    }
    res.end("OK");
  });
});

app.get('/', (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  var output = fs.readFileSync("./index.html", "utf-8");
  res.end(output);
})


http.listen(PORT, function () {
  console.log('server listening. Port:' + PORT);
});