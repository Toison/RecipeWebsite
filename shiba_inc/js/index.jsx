import React, { Component } from 'react'

class Index extends Component {
    constructor(props) {
        super(props)

        this.state = {
            recipeCards: [],
            in_session: false,
            placeholder_interval: undefined,
            placeholdertext: "",
            phts: ["Looking for something?", "Chicken?", "Breakfast?", "Dinner?"],
            pidx: [0, 0],
            delay: 50,
            sleep: 8,
            query: "",
        }
    }

    componentDidMount() {
        let url = "/api/v1/index/"
        fetch(url, { credentials: 'same-origin'})
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          
          this.setState({
              recipeCards: data.recipes,
              in_session: data.in_session,
              placeholder_interval: setInterval(this.placeholderLoop, this.state.delay)
          });
        })
    }

    handleHeart = (event, info, idx, toLike) => {
        event.preventDefault();
        if (!this.state.in_session) {
            window.location = '/accounts/login/'
        }
        const postid = info.postid
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
                recipeCards: [
                    ...prevState.recipeCards.slice(0, idx),
                    {
                        ...prevState.recipeCards[idx],
                        is_liking: data.is_liking,
                        likenum: prevState.recipeCards[idx].likenum + countChange,
                    },
                    ...prevState.recipeCards.slice(idx + 1)
                ]    
            }))
        })
        .catch((error) => console.log(error));
    }

    placeholderLoop = () => {
        this.setState((prevState) => { 
            if (prevState.pidx[1] == prevState.phts[prevState.pidx[0]].length + 1 && prevState.sleep) return {
                sleep: prevState.sleep - 1
            };
            return {
                sleep: 5,
                pidx: (prevState.pidx[1] + 1 > prevState.phts[prevState.pidx[0]].length * 2) 
                        ? [(prevState.pidx[0] + 1) % prevState.phts.length, 0] : [prevState.pidx[0], prevState.pidx[1] + 1],
                placeholdertext: prevState.phts[(prevState.pidx[0])].slice(0, 
                    prevState.pidx[1] > prevState.phts[(prevState.pidx[0])].length ? 
                    prevState.phts[(prevState.pidx[0])].length - prevState.pidx[1] :
                    prevState.pidx[1])
            }
        })
    }

    handleSearch = (event) => {
        event.preventDefault()
        // placeholder stuff
        // if (event.target.value == '') {
        //     this.setState({
        //         pidx: [0, 0], 
        //         placeholdertext: "", 
        //         placeholder_interval: setInterval(this.placeholderLoop, this.state.delay)
        //     })
        // } else {
        //     clearInterval(this.state.placeholder_interval);
        // }

        // search
        const req = {
            credentials: 'same-origin',
            method: 'POST',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: this.state.query }),
          };
      
        const url = "/api/v1/index/"
        fetch(url, req)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
              recipeCards: data.recipes,
              in_session: data.in_session,
          });
        })
    }

    queryChange = (event) => {
        event.preventDefault(0)
        this.setState({
            query: event.target.value
        })
    }

    render() {
        const stars = (rating) => {
            var n = 5;
            var z = 0;
            var arr = [...Array(n).keys()];
            return (
                arr.map(idx => {
                    if (rating >= idx + 1) {
                        return <span key={++z} className="fa fa-star checked"></span>
                    } else if (rating >= idx + 0.5) {
                        return <span key={++z} className="fa fa-star-half-full checked"></span>
                    } else {
                        return <span key={++z} className="fa fa-star-o checked"></span>
                    }
                })
            )
        }

        const heart = (info, idx) => info.is_liking ? <i className="fa fa-heart pink" onClick={(e) => this.handleHeart(e, info, idx, false)} style={{fontSize: "24px"}}></i> : <i className="fa fa-heart-o pink" onClick={(e) => this.handleHeart(e, info, idx, true)} style={{fontSize: "24px"}}></i>
    
        const tags = (info) => info.tag_list.map( (tag, idx) => <span key={idx} className='tag-span'>{tag}</span> )

        const card = (info, idx) => (
            <div className="recipe-card" key={info.postid}>
                <a href={`/p/${info.postid}`}>
                <img src={info.recipeImg} alt="recipe_img" style={{width: "100%"}}/>
                </a>
                <div className="card-container">
                    <h4 className="no-margin"><b>{info.recipename}</b></h4>
                    <div>
                        <span className="graytext"> {(info.rating * 2).toFixed(1)} </span>

                        {stars(info.rating)}

                        <span className="right margin-on-left graytext"> {info.likenum} </span> 
                        <span className="right">
                            {heart(info, idx)}
                        </span>
                    </div>
                    <div className='tag-span-container'>
                        {tags(info)}
                    </div>
                    <div style={{display: "flex"}}>
                        <div className='image-cropper'>
                        <img className='post_profile_img' src={info.filename}/>
                        </div>
                        <div className="username-center">
                            <a href={`/u/${info.username}`} className="boldtext"> <span>{info.fullname}</span> </a>
                            <span className="margin-on-left graytext">updated {info.created}</span>
                        </div>
                    </div>
                </div>
            </div>
        ) 

        const oddColumn = this.state.recipeCards.map((info, idx) => (
                idx % 2 === 1 && card(info, idx)
        ));

        const evenColumn = this.state.recipeCards.map((info, idx) => (
            idx % 2 === 0 && card(info, idx)
        ));

        return (
            <div className="index-metacontainer">            
                {/* <div className="searchbox" style={{width: '100%', 'textAlign': 'center'}}>
                    <textarea onChange={this.handleSearch} placeholder={this.state.placeholdertext}/>
                </div> */}

                <form onSubmit={this.handleSearch}>
                    <div className='searchbar'>
                        <input type="text" placeholder="Search.." name="search" value={this.state.query} onChange={this.queryChange}/>
                        <button type="submit" className='centertext'><i className="fa fa-search"></i></button>
                    </div>
                </form>

                <br></br>
                <div className="index-container">
                    <div className="column" style={{float: 'left'}}>
                        {evenColumn}
                    </div>                
                    <div className="column" style={{float: 'right'}}>
                        {oddColumn}
                    </div>
                </div>
            </div>
        )
    }
}

export default Index