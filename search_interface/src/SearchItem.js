import React from 'react';
// import baseStyles from './DemoApp.less';
import './bootstrap/css/bootstrap.min.css';

const SearchItem = (props) => {
  return (
    <div className="row">
        <div className="col-md-5">
            <a href="#">
                <img className="img-responsive" src="http://placehold.it/700x300" alt=""/>
            </a>
        </div>
        <div className="col-md-7">
            <h3>{props.name}</h3>
            <h4>{props.url}</h4>
            <p>{props.description}</p>
            <a className="btn btn-primary" href="#">View Project <span className="glyphicon glyphicon-chevron-right"/></a>
        </div>
    </div>
    );
};

SearchItem.displayName = 'SearchItem';

export default SearchItem;
