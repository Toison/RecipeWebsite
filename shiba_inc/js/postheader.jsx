import React, { Component } from 'react'
class PostHeader extends Component {
    
    
    constructor(props) {
    super(props)
    
        this.state = {
            recipeName: '',
            authorId: '',
            authorName: '',
            following: false,
            postTime: '',
            posterIcon: '',
            rating: 0.0.toFixed(1),
            parent: null,
            in_session: false,
            is_self: true,
            is_liking: false,
            num_likes: 0,
            tag_list: [],
        }
    }

    componentDidMount() {
        const {url, parent} = this.props
        fetch(url, { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          parent.state.rating = data.rating;
          this.setState({
              recipeName: data.recipeName,
              authorId: data.ownerusername,
              authorName: data.ownerfullname,
              following: data.following,
              postTime: data.time,
              postIcon: data.icon,
              parent: parent,
              in_session: data.in_session,
              is_self: data.is_self,
              is_liking: data.is_liking,
              num_likes: data.num_likes,
              tag_list: data.tag_list
          });
        })
    }

    followHandler = (event) => {
      event.preventDefault()
      if (!this.state.in_session) {
        window.location = '/accounts/login/'
      } else {
        this.setState({
          following: true,
        });
        const url = `/api/v1/u/${this.state.authorId}/follow`;

        const postData = {
          op: "follow",
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
        })
        .catch((error) => console.log(error));
      }
    }

    unfollowHandler = (event) => {
      event.preventDefault()
      if (!this.state.in_session) {
        window.location = '/accounts/login/'
      } else {
        this.setState({
          following: false,
        })
        const url = `/api/v1/u/${this.state.authorId}/follow`;

        const postData = {
          op: "unfollow",
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
        })
        .catch((error) => console.log(error));
      }
    }

    deleteHandler = (event) => {
      event.preventDefault()
      var modal = document.getElementById("exitModal")
      modal.style.display = "block"
    }

    closeModalHandler = (event) => {
      event.preventDefault()
      var modal = document.getElementById("exitModal")
      var cancel = document.getElementById("cancel")
      var x = document.getElementById("x")
      if (event.target == modal || event.target == cancel || event.target == x) {
        modal.style.display = "none";
      }
    }

    deleteConfirmHandler = (event) => {
      event.preventDefault()
      const postid = this.props.postid
      const url = `/api/v1/p/${postid}/delete-post/`
      const postData = {};
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
        window.location = '/'
      })
      .catch((error) => console.log(error));
    }

    handleHeart = (event, toLike) => {
      event.preventDefault();
      if (!this.state.in_session) {
          window.location = '/accounts/login/'
      }
      const postid = this.props.postid
      const url = `/api/v1/p/${postid}/like`;
      let likeop = "unlike"
      if(toLike) {
          likeop = "like"
      }
      const postData = {
          op: likeop,
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
          return response.json()
      })
      .then((data) => {
          const countChange = likeop == 'like' ? 1 : -1
          this.setState((prevState) => ({
              is_liking: data.is_liking,
              num_likes: prevState.num_likes + countChange,
          }))
      })
      .catch((error) => console.log(error));
    }

    render() {
        const {recipeName, authorName, authorId, following, postTime, postIcon, parent, in_session, is_self, is_liking, num_likes} = this.state;
        const rating = parent ? parent.state.rating.toFixed(1) : 0
        // TODO: fix this link issue (fullname vs username)
        const authorLink = `/u/${authorId}`

        const heart = is_liking ? <i className="fa fa-heart pink margin-on-left right" onClick={(e) => this.handleHeart(e, false)} style={{fontSize: "24px"}}></i> : <i className="fa fa-heart-o pink margin-on-left right" onClick={(e) => this.handleHeart(e, true)} style={{fontSize: "24px"}}></i>

        const followButton = () => {
          console.log(is_self)
          if(!is_self) {
            return (following ? <button  className='left inline margin-on-left smallfollowbutton' onClick={this.unfollowHandler}> following </button> : <button className='left inline margin-on-left smallfollowbutton' onClick={this.followHandler}>+ follow </button>)
          }
        }

        const deleteButton = is_self && <button className="deletebutton" onClick={this.deleteHandler}> Delete Recipe</button>

        var n = 5;
        var z = 0;
        var arr = [...Array(n).keys()];
        const hdrstars = arr.map(idx => {
          if (rating >= idx + 1) {
            return <span key={++z} className="fa fa-star checked"></span>
          } else if (rating >= idx + 0.5) {
            return <span key={++z} className="fa fa-star-half-full checked"></span>
          } else {
            return <span key={++z} className="fa fa-star-o checked"></span>
          }
        }
        )

        return (
            <div className='posthdr'>
                <h1 className='centertext'>{recipeName}</h1>
                <div className='posthdr-second-line'>
                  <div className='star-count'>
                    <span>Overall Rating: </span>
                    {hdrstars}
                    <span className='margin-on-left'>{(rating * 2.0).toFixed(1)}</span>
                  </div>
                  <div className='heart-count right'>
                    <span className='right margin-on-left'>{num_likes}</span>
                    {heart}
                  </div>
                </div>
                <div className='tag-span-container centertext'>
                    {this.state.tag_list.map( (tag, idx) => <span key={idx} className='tag-span'>{tag}</span> )}
                </div>
                <div className='posthdr-third-line'>
                    <div className='image-cropper left'>
                        <img className='post_profile_img' src={postIcon}></img>
                    </div>
                    <div className='left'>
                        <a href={authorLink} className="boldtext left"> <span>{authorName}</span> </a>
                        {followButton()}
                        <br />
                        <span className='no-margin'> updated {postTime}</span>
                    </div>
                    <div className='right delete-button-container'>
                      {deleteButton}
                    </div>
                </div>
                <div id="exitModal" className="modal" onClick={this.closeModalHandler}>
                  <div className="modal-content">
                    <span id="x" className="close" onClick={this.closeModalHandler}>&times;</span>
                    <br />
                    <br />
                    <span className='boldtext'>Are you sure you want to delete this recipe permanently?</span>
                    <br />
                    <br />
                    <div>
                      <button id="cancel" className='left cancelbutton' onClick={this.closeModalHandler}>Cancel</button>
                      <button className='right  deletebutton' onClick={this.deleteConfirmHandler}>Delete</button>
                    </div>
                    <br />
                  </div>
                </div>
            </div>
        )
    }
}
export default PostHeader