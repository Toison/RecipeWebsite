import React from 'react';
import ReactDOM from 'react-dom';
import Post from './post';
// This method is only called once

var root = document.getElementById('container');

ReactDOM.render(
  <Post {...(root.dataset)}/>, root
);