import React, { Component } from 'react';

import './bootstrap/css/bootstrap.min.css';
import './css/sidebar.css';
import $ from 'jquery';


class Sidebar extends Component {
  constructor(props) {
    super(props);
    this.onToggleLang = this.onToggleLang.bind(this);
    this.onCheckboxClicked = this.onCheckboxClicked.bind(this);


    this.state ={
      langExpanded : false,
      langSelected : []
    };
  }
  onToggleLang(e) {
    e.preventDefault();
    this.setState({
      langExpanded:!this.state.langExpanded,
    });
  }

  onCheckboxClicked(e) {
    e.preventDefault();
    if (e.checked) {
      this.setState({
        langSelected: this.state.langSelected.concat([e.value]),
      });
    } else {
      const removedIndex = this.state.indexOf(e.value);
      const left = this.state.langSelected.slice(0,removedIndex);
      const right = this.state.langSelected.slice(removedIndex+1);
      const newList = left.concat(right);
      this.setState({
        langSelected: newList,
      });
    }
    this.setState({

    });
  }

  onFilterSubmitClick(e) {
    e.preventDefault();
    const userData = {
      'langSelected':this.state.langSelected};
    $.ajax({
      type: 'POST',
      url: "/filter",
      dataType: 'json',
      cache: false,
      data: userData,
      success: function(data) {
        console.log(data);

        if (data) {
          this.setState({
            user: [this.state.registerEmail, this.state.registerUsername],
            showLoginWindow: false,
            registerEmail: '',
            registerUsername: '',
            registerFailed: false});
        } else {
          this.setState({
            registerFailed: true
          });
        }
      }.bind(this),
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
                      <input type="checkbox" name="Python" value="Python" onClick={this.onCheckboxClicked}/> Python <br/>
                      <input type="checkbox" name="Java" value="Java" onClick={this.onCheckboxClicked}/> Java
                      <input type="checkbox" name="C++" value="C++" onClick={this.onCheckboxClicked}/> C++
                      <input type="checkbox" name="Objective-C" value="Objective-C" onClick={this.onCheckboxClicked}/> Objective-C
                      <input type="checkbox" name="Javascript" value="Javascript" onClick={this.onCheckboxClicked}/> Javascript

                    </div>
                  </div>
                </section>
                <input type="submit" value="filter"/>
              </form>
          </div>
      </div>
    );
  }

};

Sidebar.displayName = 'Sidebar';

export default Sidebar;
