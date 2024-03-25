```
// Dependecies
const express = require('express');
const app = express();

// Constants
const PORT = process.env.PORT || 8080;

// Routes
app.get('/', (req, res) => {
    res.send('Hello, world!');
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something went wrong!');
});

// Starting the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
```
This code sets up a basic Express server that listens on a specified port. It includes basic error handling and a simple root route. Depending on the requirements of the underlying application, additional routes and middleware may need to be added.