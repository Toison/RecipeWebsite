import React, { Component } from 'react'

class PostComments extends Component {
    constructor(props) {
      super(props)
    
      this.state = {
        commentList: [],
        newComment: "",
        currStar: 0,
        in_session: false,
        parent: null
      }
    }

    componentDidMount() {
      const {url, parent} = this.props;
      this.state.parent = parent;
      fetch(url, { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
            commentList: data.commentList,
            in_session: data.in_session
          });
        })
        .catch((error) => console.log(error));
  }

  handleCommentChange = (event) => {
    this.setState({
        newComment: event.target.value
    })
  }

  handleStar = (event, idx) => {
    this.setState({
      currStar: idx + 1
    })
    event.preventDefault()
  }

  handleSubmit = (event) => {
    event.preventDefault()
    if (!this.state.in_session) {
      window.location = '/accounts/login/'
      return
    } else {
      const { url, parent } = this.props;

      const postData = {
        text: this.state.newComment,
        rating: this.state.currStar
      };
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify(postData),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          let stars = this.state.currStar;
          let len = this.state.commentList.length;
          this.setState((prevState) => ({
            commentList: prevState.commentList.concat(data.comment_update),
            newComment: '',
            currStar: 0,
            })
          );
          parent.setState((prevState) => ({rating: (prevState.rating * len + stars) / (len + 1)}));
        })
        .catch((error) => console.log(error));
    }
  }

  render() {

    var z = 0;
    const comments = this.state.commentList.map(comment => {
    var n = 5;
    var arr = [...Array(n).keys()];
    const cmtstars = arr.map(idx => 
      (idx < comment.ratevalue) ? <span key={++z} className="fa fa-star checked" onClick={(e) => this.handleStar(e, idx)}></span> : <span key={++z} className="fa fa-star" onClick={(e) => this.handleStar(e, idx)}></span>
    )
    return (<div key={comment.commentid} className='comment'> 
      <div>
        <a href={`/u/${comment.username}`}>
          <div className='image-cropper left'>
              <img className='post_profile_img left' src={comment.filename}></img>
          </div>
          <span className='boldtext'>{comment.fullname}</span>
        </a>
      </div>
      {cmtstars}
      <br />
      <span className='graytext'>Reviewed {comment.created}</span>
      <p>{comment.text}</p>
    </div>)
    })

    var n = 5;
    var arr = [...Array(n).keys()];
    const stars = arr.map(idx => 
      (idx < this.state.currStar) ? <span key={++z} className="fa fa-star checked" onClick={(e) => this.handleStar(e, idx)}></span> : <span key={++z} className="fa fa-star" onClick={(e) => this.handleStar(e, idx)}></span>
    )

    return (
      <div>
        <h2>Comments ({this.state.commentList.length})</h2>
        {comments}
        <form onSubmit={this.handleSubmit}>
        <textarea rows="4" cols="50" value={this.state.newComment} onChange={this.handleCommentChange} placeholder="Share your thoughts here!"/>
        <br></br>
        {stars}
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <button type="submit">comment</button>
        </form>
      </div>
    )
  }
}

export default PostComments