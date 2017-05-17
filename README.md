# saps-evaluation
This project is about generating SApS results.

ProjSrch is a single-page web application developed mainly in Javascript and Python. The front-end interface is built in React framework, with the server-side support of Node.js. On the other hand, the computation of document similarity and search result is performed in a python file, which is invoked every time an user provides an search query and click "Search".

To get the application up running, first Node.js and the newest version of NPM should be installed in the system. Since the back-end calculation for similarities is performed by a Python file, Python 2 should also be installed on the machine, along with a dependency called "pynum". All required dependencies are defined in the package.json file, located in the root folder. By simply running the terminal command "npm install", developers can easily set up the environment for the application with the help of NPM. Besides that, an installation of MySQL database is also necessary to set up the environment. The document information and user registration information would be stored on and retrieved from the database. The default database setting is: 
	
  <pre><code> 
    host: 'localhost',
  	user: 'root',
  	password: 'passw0rd',
  	database: "saps"
  </code></pre>

  
Developers are able to change the settings to be consistent to their own database by modifying the "connection" variable on the top of "server.js" file and the "db" variable in "load_test_data_into_database.py" file to connect to the database properly.


Once the environment is well set up, developers could simply call "npm start" from the root folder to start running the application. As default, the front-end side is running on "localhost:3000", but developers are able to change the port number as desired by modifying the "start" script in "package.json" file. The server side, on the contrary, is running on port 3001, which could be changed in "server.js" file:
<pre><code>
  app.set('port', (process.env.API_PORT || 3001));
</code></pre>



