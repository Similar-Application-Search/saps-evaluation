import React, { Component } from 'react';
import './App.css';
import SearchItem from './SearchItem.js';
import Sidebar from './Sidebar.js';
import { Button, ControlLabel, Form, FormGroup, FormControl, HelpBlock, Modal, Nav, NavItem, Pagination } from 'react-bootstrap';
import http from 'http';
import $ from 'jquery';

class App extends Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
    this.onSearchClick = this.onSearchClick.bind(this);
    this.onPageSelect = this.onPageSelect.bind(this);
    this.onLoginButtonClick = this.onLoginButtonClick.bind(this);
    this.onLogoutButtonClick = this.onLogoutButtonClick.bind(this);
    this.onLoginClose = this.onLoginClose.bind(this);
    this.onNavSelect = this.onNavSelect.bind(this);
    this.onLoginSubmitClick = this.onLoginSubmitClick.bind(this);
    this.onLoginEmailChange = this.onLoginEmailChange.bind(this);

    this.state = {
      candidates:[],
      activePage: 1,
      searchTarget: 0,
      showLoginWindow: false,
      activeNavItem: 'login',
      loginEmail: '',
      user: null, //would be [email, username] if logged in
      loginFailed: false, //email input cannot be found

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
        console.log(data);
        this.setState({candidates: data['candidates']});
      }.bind(this),
    });
  }

  onLoginSubmitClick(e) {
    e.preventDefault();
    $.ajax({
      url: "/login?email=" + this.state.loginEmail,
      dataType: 'json',
      cache: false,
      success: function(data) {
        console.log(data);

        if (data['username'] !== null) {
          // log the user in; close the login model window
          this.setState({
            user: [this.state.loginEmail, data],
            showLoginWindow: false,
            loginFailed: false,});
        } else {
          this.setState({
            loginFailed: true,
          })
        }
      }.bind(this),
    });
  }

  onPageSelect(eventKey) {
    this.setState({
      activePage: eventKey
    });
  }

  onLoginButtonClick() {
    this.setState({
      showLoginWindow: !this.state.showLoginWindow,
    });

  }

  onLogoutButtonClick() {
    //TODO: clear the user cookie; log user out
  }

  onLoginClose() {
    this.setState({ showLoginWindow: false});
  }

  onNavSelect(e) {
    if (e == 'login') {
      this.setState({activeNavItem:'login'});
    } else if (e == 'register') {
      this.setState({activeNavItem:'register'});
    }
  }



  onLoginEmailChange(e) {
    e.preventDefault();
    this.setState({loginEmail:e.target.value});
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
        <SearchItem name={item.name} description={item.description} url={item.url}
          allowHalfStar={ false }/>
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

      // const colse = () => this.setState({ showLoginWindow: false});
      const loginModal = (
        <Modal
          show={this.state.showLoginWindow}
          onHide={this.onLoginClose}
          container={this}>
            <Modal.Header closeButton>
              <Modal.Title id="contained-modal-title">Login/Register</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Nav bsStyle="tabs" activeNavItem="login" onSelect={this.onNavSelect} justified>
                <NavItem eventKey="login" >Log In</NavItem>
                <NavItem eventKey="register" >Register</NavItem>
              </Nav>
              <div hidden={this.state.activeNavItem!=='login'}>
                <form>
                  <FormGroup validationState={this.state.loginFailed && 'error'}>
                    <ControlLabel>Email</ControlLabel>
                    <FormControl type={'email'} placeholder={'Enter email'} onChange={this.onLoginEmailChange} value={this.state.loginEmail}/>
                    <FormControl.Feedback />
                    {this.state.loginFailed && <HelpBlock>'Email address not found. Please go ahead to register.'</HelpBlock>}
                  </FormGroup>
                  <Button type='button' onClick={this.onLoginSubmitClick} >
                    Submit
                  </Button>
                </form>
              </div>
              <div hidden={this.state.activeNavItem!='register'}>
                register
              </div>
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={this.onLoginClose}>Close</Button>
            </Modal.Footer>
        </Modal>
      );

    return (
      <div>
        <div className="col-md-2">
          <Sidebar/>
        </div>
        <Button className="col-md-2" type="button" onClick={this.onLoginButtonClick} hidden={this.state.user!==null}>
          Login
        </Button>
        <Button className="col-md-2" type="button" onClick={this.onLogoutButtonClick} hidden={this.state.user===null}>
          Log out
        </Button>
        { loginModal }
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
