import React, { Component } from 'react'
class PostSteps extends Component {
    constructor(props) {
        super(props)
        
        this.state = {
            stepList: [],
        }
    }

    componentDidMount() {
        const {url} = this.props
        fetch(url, { credentials: 'same-origin' })
          .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
          })
          .then((data) => {
            this.setState({
                stepList: data.stepList
            });
          })
          .catch((error) => console.log(error));
    }

    render() {
        const steps = this.state.stepList.map(step => <div key={step.stepnum} className='step-item'>
            <div>
                <div><img className="recipeimage" src={step.imgpath}></img></div>
                <div>
                    <h2>{`STEP ${step.stepnum}`}</h2>
                    <p>{step.text}</p>
                </div>
            </div>
         </div>)

        return (
            <div className='steps-container'>{steps}</div>
        )
    }
}

export default PostSteps