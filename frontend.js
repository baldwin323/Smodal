/**  
 * @file This file manages all user interaction events on the new frontend elements.
 */

// The index of the current page
let currentPageIndex = 0;

// The ids of the frontend pages
const pageIds = ['new-front-end-element1', 'new-front-end-element2', 'new-front-end-element3', 'new_feature', 'another_new_feature'];

// Helper function that sets a click event listener and calls a corresponding API endpoint
function setClickEventListener(id, callback) {
    document.getElementById(id).addEventListener('click', callback);
}

// Function that handles HTTP response errors
function errorHandler(response) {
    if (!response.ok) throw Error(response.statusText);
    return response;
}

// Callback functions calling the relevant backend API and handling loading states and HTTP errors
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
document.getElementById('nav-next').addEventListener('click', function() {
    if (currentPageIndex < pageIds.length - 1) {
        let oldPageId = pageIds[currentPageIndex];
        currentPageIndex += 1;
        let newPageId = pageIds[currentPageIndex];

        document.getElementById(oldPageId).style.display = 'none';
        document.getElementById(newPageId).style.display = '';
    }
});

// Set click event listeners for all frontend page ids
pageIds.forEach((id, index) => setClickEventListener(id, backendApiCallbacks[index]));