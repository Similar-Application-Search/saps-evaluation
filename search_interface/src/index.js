import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import queryoptions from '../../data/testProjectName.json'

ReactDOM.render(
  <App queryoptions={ queryoptions }/>,
  document.getElementById('root')
);
