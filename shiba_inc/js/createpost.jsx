import React, { Component } from 'react'

class Createpost extends Component {

    constructor(props) {
        super(props)
        
        this.state = {
            currPage: 0,
            recipeTitle: "",
            stepText: [],
            stepImg: [],
            stepImgName: [],
            pid: -1,
            pickedCount: 0,
            geotags: [],
            ingtags: [],
            tastags: [],
            reqtags:[],
        }
    }

    componentDidMount() {
        let url = "/api/v1/get-tags/"
        fetch(url, { credentials: 'same-origin'})
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
              geotags: data.geotags,
              ingtags: data.ingtags,
              tastags: data.tastags,
              reqtags: data.reqtags,
          });
        })
    }

    handleLabelChange = (event) => {
        this.setState({
            recipeTitle: event.target.value
        })
    }

    handleStepTextChange = (event, idx) => {
        this.setState((prevState) => ({
            stepText: [
                ...prevState.stepText.slice(0, idx),
                event.target.value,
                ...prevState.stepText.slice(idx + 1)
            ]
        }))
    }

    handleFileChange = (event, idx) => {
        event.preventDefault()
        const currPage = this.state.currPage
        let url = '/api/v1/upload-file/';
        const imageData= new FormData();
        imageData.append('file', event.target.files[0]);
        imageData.append('filename', `postid${this.state.pid}step${currPage}`);
        fetch(url, {
            method: 'POST',
            body: imageData,
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            this.setState((prevState) => ({
                stepImgName: [
                    ...prevState.stepImgName.slice(0, idx),
                    data.filename,
                    ...prevState.stepImgName.slice(idx + 1)
                ],
                stepImg: [
                    ...prevState.stepImg.slice(0, idx),
                    data.img_path,
                    ...prevState.stepImg.slice(idx + 1)
                ]
            }))
        })
    }

    handleAddStep = (event) => {
        event.preventDefault()

        const currPage = this.state.currPage
        if(currPage === 0) {
            let url = '/api/v1/add-post';
            
            let tags = []
            for (const tag of this.state.geotags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            for (const tag of this.state.ingtags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            for (const tag of this.state.tastags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            for (const tag of this.state.reqtags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            
            const postData = {
                text: this.state.recipeTitle,
                pid: this.state.pid,
                tagList: tags
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
                if (this.state.currPage + 1 > this.state.stepText.length) {
                    this.setState((prevState) => ({
                        currPage: prevState.currPage + 1,
                        stepText: [...prevState.stepText, ""],
                        stepImg: [...prevState.stepImg, ""],
                        stepImgName: [...prevState.stepImgName, ""],
                        pid: data.pid
                    }))
                } else {
                    this.setState((prevState) => ({
                        currPage: prevState.currPage + 1,
                        pid: data.pid
                    }))
                }
            })
            .catch((error) => console.log(error));
        } else {
            const url = `/api/v1/p/${this.state.pid}/add-step/`;
            console.log(this.state.stepText)
            const stepData = {
                stepnum: currPage,
                text: this.state.stepText[currPage - 1],
                filename: this.state.stepImgName[currPage - 1]
            }
            console.log(stepData)
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
                body: JSON.stringify(stepData),
            })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                console.log(`currpage: ${this.state.currPage}`)
                console.log(`stepText Length: ${this.state.stepText.length}`)
                if (this.state.currPage == this.state.stepText.length) {
                    this.setState((prevState) => ({
                        currPage: prevState.currPage + 1,
                        stepText: [...prevState.stepText, ""],
                        stepImg: [...prevState.stepImg, ""],
                        stepImgName: [...prevState.stepImgName, ""]
                    }))
                    this.fileInput.value = "";
                } else {
                    this.setState((prevState) => ({
                        currPage: prevState.currPage + 1,
                    }))
                }

                return response.json();
            })
            .catch((error) => console.log(error));
        }
    }

    handlePreviousStep = (event) => {
        event.preventDefault();
        const currPage = this.state.currPage
        let url = `/api/v1/p/${this.state.pid}/add-step/`;
        const stepData = {
            stepnum: currPage,
            text: this.state.stepText[currPage - 1],
            filename: this.state.stepImgName[currPage - 1]
        }
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
            body: JSON.stringify(stepData),
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            this.setState((prevState) => ({
                currPage: prevState.currPage - 1,
            }))
            this.fileInput.value = "";
        })
        .catch((error) => console.log(error));
    }

    handleSubmit = (event) => {
        event.preventDefault();
        const currPage = this.state.currPage
        if(currPage === 0) {
            let url = '/api/v1/add-post';
            
            let tags = []
            for (const tag of this.state.geotags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            for (const tag of this.state.ingtags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            for (const tag of this.state.tastags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }
            for (const tag of this.state.reqtags) {
                if (tag.picked) {
                    tags.push(tag.tagid)
                }
            }

            const postData = {
                text: this.state.recipeTitle,
                pid: this.state.pid,
                tagList: tags
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
                  window.location = `/p/${this.state.pid}`
            })
            .catch((error) => console.log(error));
        } else {
            let url = `/api/v1/p/${this.state.pid}/add-step/`;
            const stepData = {
                stepnum: currPage,
                text: this.state.stepText[currPage - 1],
                filename: this.state.stepImgName[currPage - 1]
            }
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
                body: JSON.stringify(stepData),
            })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                window.location = `/p/${this.state.pid}`
            })
            .catch((error) => console.log(error));
        }
    }

    handleCancel = (event) => {
        event.preventDefault();
        if(this.state.pid == -1) {
            window.location = '/'
        } else {
            const url = `/api/v1/p/${this.state.pid}/delete-post/`;
            fetch(url, {
                method: 'POST',
            })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                window.location = '/'
            })
            .catch((error) => console.log(error));
        }
    }

    tagHandler = (event, idx, cat, isPick) => {
        event.preventDefault();
        if (this.state.pickedCount >= 4 && isPick) {
            return
        }
        const countChange = isPick ? 1 : -1
        if (cat === "geo") {
            this.setState((prevState) => ({
                geotags: [
                    ...prevState.geotags.slice(0, idx),
                    {
                        ...prevState.geotags[idx],
                        picked: isPick,
                    },
                    ...prevState.geotags.slice(idx + 1)
                ],
                pickedCount: prevState.pickedCount + countChange
            }))
        } else if (cat === "ing") {
            this.setState((prevState) => ({
                ingtags: [
                    ...prevState.ingtags.slice(0, idx),
                    {
                        ...prevState.ingtags[idx],
                        picked: isPick,
                    },
                    ...prevState.ingtags.slice(idx + 1)
                ],
                pickedCount: prevState.pickedCount + countChange
            }))
        } else if (cat === "tas") {
            this.setState((prevState) => ({
                tastags: [
                    ...prevState.tastags.slice(0, idx),
                    {
                        ...prevState.tastags[idx],
                        picked: isPick,
                    },
                    ...prevState.tastags.slice(idx + 1)
                ],
                pickedCount: prevState.pickedCount + countChange
            }))
        } else if (cat === "req") {
            this.setState((prevState) => ({
                reqtags: [
                    ...prevState.reqtags.slice(0, idx),
                    {
                        ...prevState.reqtags[idx],
                        picked: isPick,
                    },
                    ...prevState.reqtags.slice(idx + 1)
                ],
                pickedCount: prevState.pickedCount + countChange
            }))
        }
    }

    render() {
        const {currPage, recipeTitle, stepText, stepImg} = this.state;
        
        const imageUploaded = this.state.stepImg[currPage - 1] != "" && <img className="uploaded-img" src={this.state.stepImg[currPage - 1]} alt={this.state.stepImgName[currPage - 1]} />

        const tagButtons = (category) => {
            if (this.state.geotags.length === 0) {
                return
            }

            const tagbutton = (tag, idx) => {
                return (                    
                <div key={tag.tagid.toString()}>
                    {tag.picked ? <button className="tag-picked" onClick={(e) => {this.tagHandler(e, idx, tag.category, false)}}>{tag.name}</button> : <button className="tag-not-picked" onClick={(e) => {this.tagHandler(e, idx, tag.category, true)}}>{tag.name}</button>}
                    <br />
                </div>)
            }

            if (category === "geo") {
                return this.state.geotags.map((tag, idx) => tagbutton(tag, idx))
            } else if (category === "ing") {
                return this.state.ingtags.map((tag, idx) => tagbutton(tag, idx))
            } else if (category === "tas") {
                return this.state.tastags.map((tag, idx) => tagbutton(tag, idx))
            } else if (category === "req") {
                return this.state.reqtags.map((tag, idx) => tagbutton(tag, idx))
            }
        }

        const step = currPage === 0 ? (
            <div>
                <div>
                    <label>Recipe Title:</label>
                    <input  className="margin-on-left newpost-textline" type="text" placeholder="Enter recipe name here ..." value={recipeTitle} onChange={this.handleLabelChange}/>
                </div>

                <br />

                <div>
                    <label>Pick Recipe Category (at most four): </label>
                    <br />
                    <br />
                    <div className='tag-container'>
                        <div className='quartercolumn'>
                            <span> Geography </span>
                            <br />
                            {tagButtons('geo')}
                        </div>
                        <div className='quartercolumn'>
                            <span>Ingredient</span>
                            <br />
                            {tagButtons('ing')}
                        </div>
                        <div className='quartercolumn'>
                            <span>Taste</span>
                            <br />
                            {tagButtons('tas')}
                        </div>
                        <div className='quartercolumn'>
                            <span>Requirement</span>
                            <br />
                            {tagButtons('req')}
                        </div>

                    </div>
                </div>

            </div>            

        ) : (
            <div>
                <h3>STEP {currPage}</h3>
                <label htmlFor="file">Upload New Image: </label>
                <input type="file" name="file" className="input_field margin-on-left" onChange={(e) => this.handleFileChange(e, currPage-1)} ref={ref=> this.fileInput = ref} required/>
                <br />
                {imageUploaded}
                <br />
                <label>Step Instruction:</label>
                <br />
                <textarea value={stepText[currPage - 1]} className="newpost-textbox" placeholder="Enter instruction here ..." onChange={(e) => this.handleStepTextChange(e, currPage-1)}></textarea>
            </div>
        )

        const prevButton = currPage != 0 && <button className='left margin-on-left' onClick={this.handlePreviousStep}>Previous Step</button>

        return (
            <div>
                <h2>Create A New Recipe</h2>
                <form>
                    {step}
                    <br />
                    <button className='left' onClick={this.handleCancel}> Cancel </button>
                    {prevButton}
                    <button className='right' onClick={this.handleSubmit}>Finish</button>
                    <button className='right margin-on-right' onClick={this.handleAddStep}> Next Step </button>
                </form>
            </div>
        )
    }
}

export default Createpost