import React, { Component } from 'react';
import './css/App.css';
import './css/SearchResult.css';
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
    this.onRegisterEmailChange = this.onRegisterEmailChange.bind(this);
    this.onRegisterUsernameChange = this.onRegisterUsernameChange.bind(this);
    this.onRegisterSubmitClick = this.onRegisterSubmitClick.bind(this);
    this.onCheckboxClicked = this.onCheckboxClicked,bind(this);
    this.onFilterSubmitClick = this.onFilterSubmitClick.bind(this);

    this.state = {
      candidates:[],
      activePage: 1,
      searchTarget: 0,
      showLoginWindow: false,
      activeNavItem: 'login',
      loginEmail: '',
      user: null, //would be [email, username] if logged in
      loginFailed: false, //email input cannot be found
      registerEmail: '',
      registerUsername: '',
      registerFailed: false,
      langSelected: ['C++','Java','Python','Javascript','Objective-C'],
      filteredCandidates:[],

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
        this.setState({
          candidates: data['candidates'],
          filteredCandidates: data['candidates'],
          langSelected: ['C++','Java','Python','Javascript','Objective-C'],
        });
      }.bind(this),
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
    const newFilteredCand = candidates.filter(function(cand){
      return langSelected.indexOf(cand.language) >= 0;
    });
    this.setState({
      filteredCandidates : newFilteredCand,
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
            user: [this.state.loginEmail, data['username']],
            showLoginWindow: false,
            loginFailed: false,
            loginEmail: '',
          });
        } else {
          this.setState({
            loginFailed: true,
          })
        }
      }.bind(this),
    });
  }

  onRegisterSubmitClick(e) {
    e.preventDefault();
    const userData = {'email':this.state.registerEmail, 'username': this.state.registerUsername};
    $.ajax({
      type: 'POST',
      url: "/register",
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


  onLogoutButtonClick(e) {
    //TODO: clear the user cookie; log user out
    this.setState({
      user: null
    });
    $.ajax({
      url: "/logout",
      cache: false,
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


  onLoginClose() {
    this.setState({
      showLoginWindow: false,
      loginFailed: false,
      registerFailed: false,});
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

  onRegisterEmailChange(e) {
    e.preventDefault();
    this.setState({registerEmail:e.target.value});
  }

  onRegisterUsernameChange(e) {
    e.preventDefault();
    this.setState({registerUsername:e.target.value});
  }

  render() {
    const queryOptions = this.props.queryoptions.map((option, index) => {
      return (
        <option key={ index } value={index} >
          {option}
        </option>
      );
    });

    const candnum = this.state.filteredCandidates.length;
    const pageSize = 5;
    const candStart = (this.state.activePage-1)*pageSize;
    const candEnd = Math.min(this.state.filteredCandidates.length, this.state.activePage*pageSize);
    const filteredCandidates = this.state.candfilteredCandidatesidates.slice(candStart,candEnd).map((item, index) => {
      return (
        <SearchItem name={item.name} description={item.description} url={item.url} language={item.language} category={item.category}
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
              <form>
                <FormGroup validationState={this.state.registerFailed && 'error'}>
                  <ControlLabel>Email</ControlLabel>
                  <FormControl type={'email'} placeholder={'Enter email'} onChange={this.onRegisterEmailChange} value={this.state.registerEmail}/>
                  <FormControl.Feedback />
                  {this.state.loginFailed && <HelpBlock>'Email address has been registered. Please login or try another email address.'</HelpBlock>}
                  <ControlLabel>Username</ControlLabel>
                  <FormControl type={'text'} placeholder={'Enter username'} onChange={this.onRegisterUsernameChange} value={this.state.registerUsername}/>

                </FormGroup>
                <Button type='button' onClick={this.onRegisterSubmitClick} >
                  Submit
                </Button>
              </form>
              </div>
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={this.onLoginClose}>Close</Button>
            </Modal.Footer>
        </Modal>
      );

    return (
      <div>
        <div id="searchResult">
          <div className="col-md-2">
            <Sidebar langSelected={this.langSelected} onCheckboxClicked={this.onCheckboxClicked} onFilterSubmitClick={this.onFilterSubmitClick}/>
          </div>

          <div className="container col-md-10">
            <div hidden={this.state.user!==null}>
              <Button className="col-md-2" type="button" onClick={this.onLoginButtonClick} >
                Login
              </Button>
            </div>

            <div hidden={this.state.user===null}>
              <div> Hi {this.state.user===null ? '': this.state.user[1]}!</div>
              <Button className="col-md-2" type="button" onClick={this.onLogoutButtonClick} >
                Log out
              </Button>
            </div>
            { loginModal }
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
            {filteredCandidates}
            {pagination}
          </div>

        </div>
      </div>
    );
  }
}

export default App;
