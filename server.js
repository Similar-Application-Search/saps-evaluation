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

app.get('/check_rating', (req, res) => {
  const key = req.query.key;
  const user_email = req.query.user_email;
  const cand_id = req.query.cand;
  const check_rating_query = "SELECT rating FROM ratings WHERE user_id=? AND test_proj_id=? AND candidate_proj_id=?";
  const user_query = "SELECT id FROM users WHERE email=?";

  if (user_email === "null") {
    res.send([{rating:0}]);
  } else {
    util.log(user_email);
    connection.query(user_query, user_email, function(err, response, field){
      let user_id = -1;
      if (err) throw err;
      if (response[0]) {
        let output = '';
        user_id = response[0].id;
        connection.query(check_rating_query, [user_id, key, cand_id], function(err1, response1, field1){
          if (err1) throw err1;
          if (response1 && response1[0]){
            res.send(response1);
          } else {
            res.send([{rating:0}]);
          }
        });
      } else {
        res.send([{rating:0}]);
      }

    });
  }
});

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
    res.send(200);
});

app.post('/rating', function(req, res) {
    const user_email = req.body.user_email;
    const testproject_id = req.body.testproject_id;
    const candidate_id = req.body.candidate_id;
    const rating = req.body.rating;
    const user_query = "SELECT id FROM users WHERE email=?";
    let user_id = -1;
    connection.query(user_query, user_email, function(err, response, field){
      if (err) throw err;
      if (response[0]) {
        user_id = response[0].id;
        const check_query = "SELECT * FROM ratings WHERE user_id=? AND test_proj_id=? AND candidate_proj_id=?";
        const insert_query = "INSERT INTO ratings (user_id, test_proj_id, candidate_proj_id, rating) VALUES (?, ?, ?, ?)";
        //check if this rating entry already exists
        connection.query(check_query, [user_id, testproject_id, candidate_id], function(err2, response2, field2){
          if (err2) throw err2;
          if (response2[0]) {
            // this rating entry exists in db
             const update_query = "UPDATE ratings SET rating=? WHERE user_id=? AND test_proj_id=? AND candidate_proj_id=?";
             connection.query(update_query, [rating, user_id, testproject_id, candidate_id], function(err3, response3, field3){
               if (err3) throw err3;
               if (response3) {
                 res.send(response3);
               }
             });
          } else {
            connection.query(insert_query,[user_id, testproject_id, candidate_id, rating], function(err1, response1, field1){
              if (err1) throw err1;
              if (response1) {
                res.send(response1);
              }
            });
          }
        });
        util.log([user_id, testproject_id, candidate_id, rating]);
      }
    });


});

app.listen(app.get('port'), () => {
  console.log(`Find the server at: http://localhost:${app.get('port')}/`); // eslint-disable-line no-console
});
