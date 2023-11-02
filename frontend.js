// Import necessary dependencies
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';
import './styles.css';

// Import the loading spinner and feedback prompt components
import LoadingSpinner from './components/LoadingSpinner';
import FeedbackPrompt from './components/FeedbackPrompt';
import HelpSupport from './components/HelpSupport';

// Define the Ids of all pages we have
const pageIds = ['user-authentication', 'dashboard', 'file-upload', 'button-actions', 'form-validation', 'ui-ux-design', 'state-management', 'routing', 'api-integration', 'watch-page', 'cloning-page', 'menu-page', 'banking-page'];

// Error handler to provide better error messages
const errorHandler = (error) => {
  if (!error.response) {
    // Give friendly message and suggest action
    return {
      errorMsg: `Error: Network Error`,
      actionSuggestion: 'Please check your internet connection.'
    };
  } else {
    return {
      errorMsg: error.response.data,
      actionSuggestion: "Please try again. If the problem persists, contact our support team."  // Suggest possible action
    };
  }
};

// Main page component that handles all our logic
const MainPage = () => {
  const [currentPageIndex, setCurrentPageIndex] = useState(0); // Keep track of current page
  const [aiResponse, setAiResponse] = useState(''); // State variable for storing AI response.
  const [isLoading, setIsLoading] = useState(false); // State variable for loading spinner

  // On page load call the api for the current page
  useEffect(() => {
    handleAPIFetch(pageIds[currentPageIndex]);
  }, [currentPageIndex]);

  // Function to call APIs and handle error properly
  const handleAPIFetch = (id) => {
    setIsLoading(true); // Start loading spinner
    axios.get(`/api/${id}`)
      .then(response => {
        const data = response.data;
        console.log(`The returned data is: ${JSON.stringify(data)}`);
        setIsLoading(false); // Stop loading spinner
      }) 
      .catch(error => {
        const { errorMsg, actionSuggestion } = errorHandler(error); // Use the error handler when an error occurs
        console.log(`${errorMsg}. ${actionSuggestion}`);
        setIsLoading(false); // Stop loading spinner
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
    setIsLoading(true); // Start loading spinner
    axios.get('/ai_predict', { input: inputData })
      .then(response => {
        setAiResponse(response.data.response); // Save the AI response to state
        setIsLoading(false); // Stop loading spinner
      })
      .catch(error => {
        const { errorMsg, actionSuggestion } = errorHandler(error); // Use the error handler when an error occurs
        console.log(`${errorMsg}. ${actionSuggestion}`);
        setIsLoading(false); // Stop loading spinner
      });
  }

  // Using currentPageIndex to conditionally render content
  const renderContent = () => {
    switch(currentPageIndex) {
      case 0: return <div>This is page 0</div>;
      case 1: return <div>This is page 1</div>;
      // Add more cases as needed for each page
      default: return <div>;
    }
  }

  return (
    <div className="app-container">
      <div className="nav-bar">
        <button onClick={handlePrevClick} className="nav-button">Prev</button> {/* Prev Button */}
        <button onClick={handleNextClick} className="nav-button">Next</button> {/* Next Button */}
        {/* Button to call AI model. */}
        <button onClick={() => handleAiCall('input data here')} className="nav-button">Call AI</button> 
      </div>
      {/* Conditionally render page content based on currentPageIndex */}
      {renderContent()}
      <div id={pageIds[currentPageIndex]} className='page-container'>
        {/* Display AI response. */}
        <p>{aiResponse}</p>
        {/* Display a loading spinner if isLoading is true */}
        {isLoading && <LoadingSpinner />}
        {/* Display the feedback prompt */}
        <FeedbackPrompt />
        {/* Display the help and support section */}
        <HelpSupport />
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
