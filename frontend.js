import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';
import './styles.css'; // Assuming that CSS file exists in the same directory

// Array of page ids for navigation purpose
const pageIds = ['user-authentication', 'dashboard', 'file-upload', 'button-actions', 'form-validation', 'ui-ux-design', 'state-management', 'routing', 'api-integration', 'watch-page', 'cloning-page', 'menu-page', 'banking-page'];

// Function to handle errors from the server
const errorHandler = (error) => {
  if (!error.response) {
    return `Error: Network Error`;
  } else {
    return error.response.data;
  }
};

// Main Component for the application
const MainPage = () => {
  const [currentPageIndex, setCurrentPageIndex] = useState(0);

  // Fetching required data when the page is loaded
  useEffect(() => {
    handleAPIFetch(pageIds[currentPageIndex]);
  }, [currentPageIndex]);

  // Function to fetch data from the server
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

  const handlePrevClick = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(prevState => prevState - 1);
    }
  }

  const handleNextClick = () => {
    if (currentPageIndex < pageIds.length - 1) {
      setCurrentPageIndex(prevState => prevState + 1);
    }
  }

  return (
    <div className="app-container">
      <div className="nav-bar">
        <button onClick={handlePrevClick} className="nav-button">Prev</button>
        <button onClick={handleNextClick} className="nav-button">Next</button>
      </div>
      <div id={pageIds[currentPageIndex]} className='page-container'>
        {/* Content goes here */}
      </div>
    </div>
  );
}

// Render the main component into the div with id 'root'
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