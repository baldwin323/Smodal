import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import axios from 'axios';
import './styles.css'; 

const pageIds = ['user-authentication', 'dashboard', 'file-upload', 'button-actions', 'form-validation', 'ui-ux-design', 'state-management', 'routing', 'api-integration', 'watch-page', 'cloning-page', 'menu-page', 'banking-page'];

const errorHandler = (error) => {
  if (!error.response) {
    return `Error: Network Error`;
  } else {
    return error.response.data;
  }
};

const MainPage = () => {
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [aiResponse, setAiResponse] = useState(''); // State variable for storing AI response.

  useEffect(() => {
    handleAPIFetch(pageIds[currentPageIndex]);
  }, [currentPageIndex]);

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
  
  // New function to handle requesting AI model predictions/responses.
  const handleAiCall = (inputData) => {
    axios.get('/ai_predict', { input: inputData })
      .then(response => {
        setAiResponse(response.data.response);
      })
      .catch(error => {
        console.log(errorHandler(error));
      });
  }

  return (
    <div className="app-container">
      <div className="nav-bar">
        <button onClick={handlePrevClick} className="nav-button">Prev</button>
        <button onClick={handleNextClick} className="nav-button">Next</button>
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