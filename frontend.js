// Importing necessary modules ie. react, react-dom, react-router-dom and axios for making API calls
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';

// Defining constants for the ids of the frontend pages
const pageIds = ['user-authentication', 'dashboard', 'file-upload', 'button-actions', 'form-validation', 'ui-ux-design', 'state-management', 'routing', 'api-integration', 'watch-page', 'cloning-page', 'menu-page', 'banking-page'];

// Function to handle HTTP response errors
const errorHandler = (error) => {
  if (!error.response) {
    // network error
    return `Error: Network Error`;
  } else {
    return error.response.data;
  }
};

// Functional component to manage all pages
const MainPage = () => {
  // State management
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  
  // Using useEffect to update UI based on state changes
  useEffect(() => {
    let newPageId = pageIds[currentPageIndex];
    handleAPIFetch(newPageId);
  }, [currentPageIndex]);

  // Function to fetch data from backend API
  const handleAPIFetch = (id) => {
    axios.get(`/api/${id}`)
      .then(response => {
        const data = response.data;
        console.log(`The returned data is: ${JSON.stringify(data)}`);
      }) 
      .catch(error => {
        console.log(errorHandler(error));
      });
  }

  // Defining function to handle previous navigation
  const handlePrevClick = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(prevState => prevState - 1);
    }
  }

  // Defining function to handle next navigation
  const handleNextClick = () => {
    if (currentPageIndex < pageIds.length - 1) {
      setCurrentPageIndex(prevState => prevState + 1);
    }
  }

  // Render logic for the component
  return (
    <div>
      <button onClick={handlePrevClick}>Prev</button>
      <button onClick={handleNextClick}>Next</button>
    </div>
  );
}

// Creating routing within the application using react-router-dom
ReactDOM.render(
  <Router>
    <Switch>
      <Route exact path="/"><MainPage /></Route>
      {pageIds.map((pageId, i) => (
        <Route exact path={`/${pageId}`}><MainPage /></Route>
      ))}
    </Switch>
  </Router>,
  document.getElementById('root')
);