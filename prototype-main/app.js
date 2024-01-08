```
// Import required modules
const express = require('express');
const OpenAI = require('openai-api');

// Use environment variable for OpenAI API key
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const openai = new OpenAI(OPENAI_API_KEY);

const app = express();
app.use(express.json());

// Endpoint to start cloning
app.post('/startCloning', async (req, res) => {
  try {
    const prompt = req.body.prompt;
    const response = await openai.complete({
      engine: 'davinci-codex',
      maxTokens: 100,
      prompt
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: `Failed to start cloning: ${error.message}`
    });
  }
});

// Endpoint to check clone status
app.get('/checkClone', (req, res) => {
  res.json({
    cloneCreated: true,
    cloneMessage: 'Your clone is ready. You can activate it now.'
  });
});

// Endpoint to activate clone
app.get('/activateClone', (req, res) => {
  res.json({
    cloneActive: true,
    message: 'Congrats! Your clone is now active.'
  });
});

// Listen to the port provided by environment variable or default 3000
app.listen(process.env.PORT || 3000, () => {
  console.log(`App is running on port ${process.env.PORT || 3000}.`);
});

module.exports = app;

/*
Added Procfile for deployment 
web: node app.js
*/
```
