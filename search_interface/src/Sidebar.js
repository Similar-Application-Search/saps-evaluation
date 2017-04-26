import React, { Component } from 'react';

import './bootstrap/css/bootstrap.min.css';
import './css/sidebar.css';
import $ from 'jquery';


class Sidebar extends Component {
  constructor(props) {
    super(props);
    this.onToggleLang = this.onToggleLang.bind(this);

    this.state ={
      langExpanded : false,
    };
  }
  onToggleLang(e) {
    e.preventDefault();
    this.setState({
      langExpanded:!this.state.langExpanded,
    });
  }


  render() {
    return (
      <div id="sidebar-wrapper">
          <div className="sidebar-nav">
              <form action="">
                <section>
                  <label>Filter</label>
                  <div className="option">
                    <label onClick={this.onToggleLang}>Languages</label>
                    <div className="toggle" hidden={this.state.langExpanded}>
                      <span/><span/>
                    </div>
                    <div className="toggled" hidden={!this.state.langExpanded}>
                      <span/><span/>
                    </div>
                    <div className="expand" hidden={this.state.langExpanded}/>
                    <div className="open" hidden={!this.state.langExpanded}>
                      <input type="checkbox" name="Python" value="Python" onClick={this.props.onCheckboxClicked} checked/> Python <br/>
                      <input type="checkbox" name="Java" value="Java" onClick={this.props.onCheckboxClicked} checked/> Java
                      <input type="checkbox" name="C++" value="C++" onClick={this.props.onCheckboxClicked} checked/> C++
                      <input type="checkbox" name="Objective-C" value="Objective-C" onClick={this.props.onCheckboxClicked} checked/> Objective-C
                      <input type="checkbox" name="Javascript" value="Javascript" onClick={this.props.onCheckboxClicked} checked/> Javascript

                    </div>
                  </div>
                </section>
                <input type="submit" value="filter" onClick={this.props.onFilterSubmitClick}/>
              </form>
          </div>
      </div>
    );
  }

};

Sidebar.displayName = 'Sidebar';

export default Sidebar;
