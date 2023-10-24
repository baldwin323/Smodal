/**  
 * @file This file manages all user interaction events on the new frontend elements.
 * Each function has error handling and each API call endpoint has a detailed description in the form of comments.
 */

// The index of the current page
let currentPageIndex = 0;

// The ids of the frontend pages
const pageIds = ['new-front-end-element1', 'new-front-end-element2', 'new-front-end-element3', 'new_feature', 'another_new_feature'];

/**
 * Function that sets a click event listener and calls a corresponding API endpoint
 * @param id - HTML element id
 * @param callback - Callback function to be executed on click event
 */
function setClickEventListener(id, callback) {
    document.getElementById(id).addEventListener('click', callback);
}

/**
 * Function to handle HTTP response errors
 * @param response - HTTP response object
 * @throws Will throw an error if the response status is not OK
 */
function errorHandler(response) {
    if (!response.ok) throw Error(response.statusText);
    return response;
}

// Callback functions calling the relevant backend API and handling loading states and HTTP errors
// Each callback hits a different API endpoint depending on the pageId, handles any response error, processes the json response and handles loading states.
const backendApiCallbacks = pageIds.map(id => () => {
    document.body.classList.add('loading');
    fetch(`/api/${id}`)
        .then(errorHandler)
        .then(response => response.json())
        .then(data => {
            // updated to handle new data structure
            document.getElementById(id).innerText = `The returned data is: ${JSON.stringify(data)}`;
        })  
        .finally(() => document.body.classList.remove('loading'))
});

// Event listener for the 'previous' navigation button
// Handles page navigation in backward direction
document.getElementById('nav-prev').addEventListener('click', function() {
    if (currentPageIndex > 0) {
        let oldPageId = pageIds[currentPageIndex];
        currentPageIndex -= 1;
        let newPageId = pageIds[currentPageIndex];
        
        document.getElementById(oldPageId).style.display = 'none';
        document.getElementById(newPageId).style.display = '';
    }
});

// Event listener for the 'next' navigation button
// Handles page navigation in forward direction
document.getElementById('nav-next').addEventListener('click', function() {
    if (currentPageIndex < pageIds.length - 1) {
        let oldPageId = pageIds[currentPageIndex];
        currentPageIndex += 1;
        let newPageId = pageIds[currentPageIndex];

        document.getElementById(oldPageId).style.display = 'none';
        document.getElementById(newPageId).style.display = '';
    }
});

// Set click event listeners for all frontend page ids, using corresponding backend API callbacks
pageIds.forEach((id, index) => setClickEventListener(id, backendApiCallbacks[index]));