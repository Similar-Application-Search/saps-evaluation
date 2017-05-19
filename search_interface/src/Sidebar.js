import React, { Component } from "react";

import "./bootstrap/css/bootstrap.min.css";
import "./css/sidebar.css";
import $ from "jquery";


class Sidebar extends Component {
  constructor(props) {
    super(props);
    this.onToggleLang = this.onToggleLang.bind(this);
    this.onCheckboxClicked = this.onCheckboxClicked.bind(this);
    this.onFilterSubmitClick = this.onFilterSubmitClick.bind(this);

    this.state ={
      langExpanded : false,
      langSelected: ["C++","Java","Python","Javascript","Objective-C"],
    };
  }
  onToggleLang(e) {
    e.preventDefault();
    this.setState({
      langExpanded:!this.state.langExpanded,
    });
  }

  onCheckboxClicked(e) {
    this.props.onCheckboxClicked(e);
    if (e.target.checked) {
      this.setState({
        langSelected: this.state.langSelected.concat([e.target.value]),
      });
    } else {
      const removedIndex = this.state.langSelected.indexOf(e.target.value);
      const left = this.state.langSelected.slice(0,removedIndex);
      const right = this.state.langSelected.slice(removedIndex+1);
      const newList = left.concat(right);
      this.setState({
        langSelected: newList,
      });
    }
  }

  onFilterSubmitClick(e) {
    this.props.onFilterSubmitClick(e);
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
                      <input type="checkbox" name="Python" value="Python" onClick={this.onCheckboxClicked} checked={this.state.langSelected.indexOf("Python")>=0}/> Python <br/>
                      <input type="checkbox" name="Java" value="Java" onClick={this.onCheckboxClicked} checked={this.state.langSelected.indexOf("Java")>=0}/> Java
                      <input type="checkbox" name="C++" value="C++" onClick={this.onCheckboxClicked} checked={this.state.langSelected.indexOf("C++")>=0}/> C++
                      <input type="checkbox" name="Objective-C" value="Objective-C" onClick={this.onCheckboxClicked} checked={this.state.langSelected.indexOf("Objective-C")>=0}/> Objective-C
                      <input type="checkbox" name="Javascript" value="Javascript" onClick={this.onCheckboxClicked} checked={this.state.langSelected.indexOf("Javascript")>=0}/> Javascript

                    </div>
                  </div>
                </section>
                <input type="submit" value="filter" onClick={this.onFilterSubmitClick}/>
              </form>
          </div>
      </div>
    );
  }

};

Sidebar.displayName = "Sidebar";

export default Sidebar;
