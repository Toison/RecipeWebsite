import React from 'react';
import PropTypes from 'prop-types';
import PostHeader from './postheader';
import PostSteps from './poststeps';
import PostComments from './postcomments';
class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { rating: 0.0 }
  }
  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    return; // URL is not defined
    const { url } = this.props;
    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          owner: data.owner
        });
      })
      .catch((error) => console.log(error));
  }
  render() {
    console.log(this.state.rating)
    return (
      <div className="post_block">
        <PostHeader url={`/api/v1/p/${this.props.id}/hdr`} parent={this} postid={this.props.id}/>
        <PostSteps url={`/api/v1/p/${this.props.id}/stp`}/>
        <PostComments url={`/api/v1/p/${this.props.id}/cmt`} parent={this}/>
      </div>
    );
  }
}

export default Post;