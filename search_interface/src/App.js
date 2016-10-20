import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchItem from './SearchItem.js';
import Sidebar from './Sidebar.js';
import { Button, Form, FormGroup, FormControl } from 'react-bootstrap';
import http from 'http';
import $ from 'jquery';

class App extends Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
    this.state = {candidates:[]}
  }

  onChange(e) {
    e.preventDefault();
    $.ajax({
      url: "/search?key=" + e.target.value,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({candidates: data['candidates']});
        console.log(data);

      }.bind(this),
    });

  }

  render() {
    const queryOptions = this.props.queryoptions.map((option, index) => {
      return (
        <option key={ index } value={index} >
          {option}
        </option>
      );
    });

    // const searchResult = require("../saps-evaluation/search_sample.json");

    const candidates = this.state.candidates.map((item, index) => {
      return (
        <SearchItem name={item.name} description={item.description} url={item.url}/>
      );
    });
    return (
      <div>
        <div className="col-md-2">
          <Sidebar/>
        </div>
        <div className="container col-md-10">
          <div className="row">
              <div className="col-md-12">
                <Form>
                  <FormGroup className="col-md-10" controlId="searchEntry">
                    <FormControl componentClass="select" placeholder="select" onChange={this.onChange}>
                      <option value="select">Select a project name...</option>
                      { queryOptions }
                    </FormControl>
                  </FormGroup>
                  <Button className="col-md-2" type="submit">
                    Search
                  </Button>
                </Form>
              </div>
          </div>
          {candidates}
        </div>
      </div>
    );
  }
}

export default App;
