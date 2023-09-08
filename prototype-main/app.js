```
const express = require('express');
const OpenAI = require('openai-api');

const OPENAI_API_KEY = 'PLACE_YOUR_OPENAI_API_KEY_HERE';
const openai = new OpenAI(OPENAI_API_KEY);

const app = express();
app.use(express.json());

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

app.get('/checkClone', (req, res) => {
  res.json({
    cloneCreated: true,
    cloneMessage: 'Your clone is ready. You can activate it now.'
  });
});

app.get('/activateClone', (req, res) => {
  res.json({
    cloneActive: true,
    message: 'Congrats! Your clone is now active.'
  });
});

app.listen(3000, () => {
  console.log('App is running on port 3000.');
});

module.exports = app;
```