#npm install -g forever
forever start -w server.js
cd ./search_interface
forever start -c "npm start" ./
