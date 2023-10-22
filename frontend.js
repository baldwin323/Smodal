/**  
 * @file This file handles all user interaction events on the new frontend elements.
 */
 
// The index of the current page
let currentPageIndex = 0;

// The ids of the pages
const pageIds = ['new-front-end-element1', 'new-front-end-element2', 'new-front-end-element3', 'new_feature', 'another_new_feature'];

// Helper function abstracting the repetitive logic for adding event listeners and calling backend API
function setupEventListener(id, callback) {
    document.getElementById(id).addEventListener('click', callback);
}

// Error handling function 
function handleErrors(response) {
    if (!response.ok) throw Error(response.statusText);
    return response;
}

// Callback functions calling the corresponding backend API and handling loading and errors
const actionElements = pageIds.map(id => () => {
    document.body.classList.add('loading');
    fetch(`/api/${id}`).catch(handleErrors).then(() => document.body.classList.remove('loading')); 
});

document.getElementById('nav-prev').addEventListener('click', function() {
    if (currentPageIndex > 0) {
        let oldPageId = pageIds[currentPageIndex];
        currentPageIndex -= 1;
        let newPageId = pageIds[currentPageIndex];
        
        document.getElementById(oldPageId).style.display = 'none';
        document.getElementById(newPageId).style.display = 'block';
    }
});

document.getElementById('nav-next').addEventListener('click', function() {
    if (currentPageIndex < pageIds.length - 1) {
        let oldPageId = pageIds[currentPageIndex];
        currentPageIndex += 1;
        let newPageId = pageIds[currentPageIndex];

        document.getElementById(oldPageId).style.display = 'none';
        document.getElementById(newPageId).style.display = 'block';
    }
});

// Add event listeners to new elements on the watch page
pageIds.forEach((id, index) => setupEventListener(id, actionElements[index]));
