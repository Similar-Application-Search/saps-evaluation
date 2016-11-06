#npm install -g forever
forever start server.js
cd ./search_interface
forever start -c "npm start" ./
