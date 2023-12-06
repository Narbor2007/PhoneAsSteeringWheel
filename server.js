
const express = require('express');
const app = express();
const https = require('https');
const fs = require('fs');

const host = 'HOST IP';
const port = 3003;

https
  .createServer(
    {
      key: fs.readFileSync('C:/key.pem'),
      cert: fs.readFileSync('C:/cert.pem'),
    },
    app.get('/style.css', function(req, res){
      res.sendFile(process.cwd() + '/style.css');
    }),
    app.get('/script.js', function(req, res){
      res.sendFile(process.cwd() + '/script.js');
    }),
    app.get('/', function(req, res){
      res.sendFile(process.cwd() + '/file.html');
    })
  )
  .listen(port, host, function () {
    console.log(`Server listens https://${host}:${port}`);
  });