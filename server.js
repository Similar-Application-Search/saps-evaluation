const express = require('express');
const bodyParser = require("body-parser");

const fs = require('fs');
var util = require("util");
var mysql = require('mysql');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const spawn = require("child_process").spawn;

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'passw0rd',
  database: "saps"
});
connection.connect();

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

app.get('/login', (req, res) => {

  const email = req.query.email;
  const query = 'SELECT username FROM users WHERE email=?';
  connection.query(query, email,function(err, rows, fields){
    if (err) throw err;
    if (rows.length > 0) {
      const userValue = {email:email, username:rows[0]};

      res.cookie('user', userValue, { expires: new Date(Date.now() + 3600000), httpOnly: true });
      res.setHeader('Content-Type', 'application/json');
      res.send(rows[0]);
    } else {
      res.setHeader('Content-Type', 'application/json');
      res.send({email:email, username:null});
    }

  });

});

app.post('/register', function(req, res) {
    const email = req.body.email;
    const username = req.body.username;
    const userValue = {email:email, username:username};
    const query = 'INSERT INTO users (email, username) VALUES (?, ?)';
    connection.query(query, [email, username], function(err, response, fields){
      if (err) throw err;
      if (response) {
        res.cookie('user', userValue, { expires: new Date(Date.now() + 3600000), httpOnly: true });
      }
      res.send(response);
    })
});

app.post('/logout', function(req, res) {
    res.clearCookie('user');
});


app.listen(app.get('port'), () => {
  console.log(`Find the server at: http://localhost:${app.get('port')}/`); // eslint-disable-line no-console
});
