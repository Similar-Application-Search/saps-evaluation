const express = require('express');
const fs = require('fs');
var util = require("util");

const app = express();
const spawn = require("child_process").spawn;

app.set('port', (process.env.API_PORT || 3001));

app.get('/search', (req, res) => {
  const key = req.query.key;
  const process = spawn('python',["./search.py", key]);
  util.log('readingin')

  let output = '';
  process.stdout.on('data',function(chunk){

      output = chunk.toString('utf8');// buffer to string
      util.log(output);

      res.setHeader('Content-Type', 'application/json');
      res.send(output);


  });

});

app.listen(app.get('port'), () => {
  console.log(`Find the server at: http://localhost:${app.get('port')}/`); // eslint-disable-line no-console
});
