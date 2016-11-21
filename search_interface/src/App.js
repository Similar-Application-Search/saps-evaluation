import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchItem from './SearchItem.js';
import Sidebar from './Sidebar.js';
import { Button, Form, FormGroup, FormControl, Pagination } from 'react-bootstrap';
import http from 'http';
import $ from 'jquery';

class App extends Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
    this.onSearchClick = this.onSearchClick.bind(this);
    this.onPageSelect = this.onPageSelect.bind(this);
    this.state = {
      candidates:[],
      activePage: 1,
      searchTarget: 0,
    }
  }

  onChange(e) {
    e.preventDefault();
    this.setState({ searchTarget: e.target.value })
  }

  onSearchClick(e) {
    e.preventDefault();
    $.ajax({
      url: "/search?key=" + this.state.searchTarget,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({candidates: data['candidates']});
      }.bind(this),
    });
  }

  onPageSelect(eventKey) {
    this.setState({
      activePage: eventKey
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
    const candnum = this.state.candidates.length;
    const pageSize = 5;
    const candStart = (this.state.activePage-1)*pageSize;
    const candEnd = Math.min(this.state.candidates.length, this.state.activePage*pageSize);
    const candidates = this.state.candidates.slice(candStart,candEnd).map((item, index) => {
      return (
        <SearchItem name={item.name} description={item.description} url={item.url}/>
      );
    });

    let maxPage = candnum / pageSize;
    if (candnum%pageSize > 0) {
      maxPage += 1;
    }
    const pagination = (<Pagination
        prev
        next
        first
        last
        ellipsis
        boundaryLinks
        items={maxPage}
        maxButtons={3}
        activePage={this.state.activePage}
        onSelect={this.onPageSelect} />);


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
                  <Button className="col-md-2" type="submit" onClick={this.onSearchClick}>
                    Search
                  </Button>
                </Form>
              </div>
          </div>
          {candidates}
          {pagination}
        </div>

      </div>
    );
  }
}

export default App;
