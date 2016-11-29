import React from 'react';
import ReactStars from 'react-stars';
import './bootstrap/css/bootstrap.min.css';
import './css/SearchItem.css';

const onRatingChange = (newRating) => {
  console.log(newRating);
}

const SearchItem = (props) => {
  return (
    <div className="row searchItem">

        <div className="col-md-12">
            <h3>{props.name}</h3>
            <ReactStars half = {props.allowHalfStar} onChange= {onRatingChange}/>
            <h4><a href= {props.url}>{props.url}</a></h4>
            <p>{props.description}</p>
            <a className="btn btn-primary" href={props.url}>View Project <span className="glyphicon glyphicon-chevron-right"/></a>
        </div>
    </div>
    );
};

SearchItem.displayName = 'SearchItem';

export default SearchItem;
