import React from 'react';
import './bootstrap/css/bootstrap.min.css';
import './css/sidebar.css';


const Sidebar = (props) => {
  return (
    <div id="sidebar-wrapper">
        <ul className="sidebar-nav">
            <li className="sidebar-brand">
                <a href="#">
                    Start Bootstrap
                </a>
            </li>
            <li>
                <a href="#">Dashboard</a>
            </li>
            <li>
                <a href="#">Shortcuts</a>
            </li>
            <li>
                <a href="#">Overview</a>
            </li>
            <li>
                <a href="#">Events</a>
            </li>
            <li>
                <a href="#">About</a>
            </li>
            <li>
                <a href="#">Services</a>
            </li>
            <li>
                <a href="#">Contact</a>
            </li>
        </ul>
    </div>
    );
};

Sidebar.displayName = 'Sidebar';

export default Sidebar;
