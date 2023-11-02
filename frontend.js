// Import necessary dependencies
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';
import './styles.css';

// Define the Ids of all pages we have
const pageIds = ['user-authentication', 'dashboard', 'file-upload', 'button-actions', 'form-validation', 'ui-ux-design', 'state-management', 'routing', 'api-integration', 'watch-page', 'cloning-page', 'menu-page', 'banking-page'];

// Error handler to provide better error messages
const errorHandler = (error) => {
  if (!error.response) {
    return `Error: Network Error`;
  } else {
    return error.response.data;
  }
};

// Main page component that handles all our logic
const MainPage = () => {
  const [currentPageIndex, setCurrentPageIndex] = useState(0); // Keep track of current page
  const [aiResponse, setAiResponse] = useState(''); // State variable for storing AI response.

  // On page load call the api for the current page
  useEffect(() => {
    handleAPIFetch(pageIds[currentPageIndex]);
  }, [currentPageIndex]);

  // Function to call APIs and handle error properly
  const handleAPIFetch = (id) => {
    axios.get(`/api/${id}`)
      .then(response => {
        const data = response.data;
        console.log(`The returned data is: ${JSON.stringify(data)}`);
      }) 
      .catch(error => {
        console.log(errorHandler(error)); // Use the error handler when an error occurs
      });
  }

  // Handle Clicking on previous button
  const handlePrevClick = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(prevState => prevState - 1);
    }
  }

  // Handle Clicking on Next button
  const handleNextClick = () => {
    if (currentPageIndex < pageIds.length - 1) {
      setCurrentPageIndex(prevState => prevState + 1);
    }
  }
  
  // New function to handle requesting AI model predictions/responses.
  const handleAiCall = (inputData) => {
    axios.get('/ai_predict', { input: inputData })
      .then(response => {
        setAiResponse(response.data.response); // Save the AI response to state
      })
      .catch(error => {
        console.log(errorHandler(error)); // Use the error handler when an error occurs
      });
  }

  return (
    <div className="app-container">
      <div className="nav-bar">
        <button onClick={handlePrevClick} className="nav-button">Prev</button> {/* Prev Button */}
        <button onClick={handleNextClick} className="nav-button">Next</button> {/* Next Button */}
        {/* Button to call AI model. */}
        <button onClick={() => handleAiCall('input data here')} className="nav-button">Call AI</button> 
      </div>
      <div id={pageIds[currentPageIndex]} className='page-container'>
        {/* Display AI response. */}
        <p>{aiResponse}</p>
      </div>
    </div>
  );
}

// Render our main page into the root element
ReactDOM.render(
  <Router>
    <Switch>
      <Route exact path="/"><MainPage /></Route> {/* Render MainPage at root */}
      {/* Render MainPage at all other paths based on pageIds */}
      {pageIds.map((pageId, i) => (
        <Route exact path={`/${pageId}`}><MainPage /></Route>
      ))}
    </Switch>
  </Router>,
  document.getElementById('root')
);