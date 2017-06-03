import React, { Component } from 'react';
import ReactStars from 'react-stars';
import './bootstrap/css/bootstrap.min.css';
import './css/SearchItem.css';
import $ from "jquery";

class SearchItem extends Component {
  constructor(props) {
    super(props);
    this.onRatingChange = this.onRatingChange.bind(this);
    this.state = {
      rating:0,
    }
  }

  onRatingChange (newRating) {
    const user_email = this.props.user_email;
    const testproject_id = this.props.testproject_id;
    const candidate_id = this.props.candidate_id;
    const rating = newRating;
    const ratingData = {"user_email":user_email, "testproject_id":testproject_id, "candidate_id":candidate_id, "rating":rating};
    if (user_email===null) {
      this.props.promptLogin();
    } else {
      $.ajax({
        type: "POST",
        url: "/rating",
        dataType: "json",
        cache: false,
        data: ratingData,
        success: function(data) {
          console.log(data);
          this.setState({
            rating:rating,
          })
        }.bind(this),
      });
    }
  }

  componentWillMount() {
    $.ajax({
      url: "/check_rating?key=" + this.props.testproject_id + "&cand=" + this.props.candidate_id + "&user_email=" + this.props.user_email,
      dataType: "json",
      cache: false,
    }).done(function(data) {
      if (data.length > 0) {
        this.setState({rating:data[0].rating})
      }
    }.bind(this));
  }

  componentWillReceiveProps(nextprops) {
    console.log("received props: " + nextprops.testproject_id)
    $.ajax({
      url: "/check_rating?key=" + nextprops.testproject_id + "&cand=" + nextprops.candidate_id + "&user_email=" + nextprops.user_email,
      dataType: "json",
      cache: false

    }).done(function(data) {
      if (data.length > 0) {
        this.setState({rating:data[0].rating})

      }
      console.log(data.length);

    }.bind(this));

  }
  render() {
    const language_color_dict = {
      "Java": "red",
      "C++" : "blue",
      "Javascript" : "green",
      "Objective-C" : "purple",
      "Python" : "grey"
    };
    const language_color = language_color_dict[this.props.language.trim()];

    return (
      <div className="row searchItem">

          <div className="col-md-12">
              <h3>{this.props.name}</h3>
              <ReactStars value = {this.state.rating} half = {this.props.allowHalfStar} onChange= {this.onRatingChange}/>
              <h4><a href= {this.props.url}>{this.props.url}</a></h4>
              <p>{this.props.description}</p>
              <p><span style= {{color:language_color}}>•{this.props.language}</span>  <span>{this.props.category}</span></p>
              <a className="btn btn-primary" href={this.props.url}>View Project <span className="glyphicon glyphicon-chevron-right"/></a>
          </div>
      </div>
      );

  }
}


export default SearchItem;
