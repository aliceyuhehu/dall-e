const express = require('express');
const app = express();
const port = 3000;
const DALLE_API_KEY = KlwxQwOjyWGK4JnvqA0QT3BlbkFJz4T7NrWnlXOCZyjJSWOg;

// Body parser middleware to parse form data
// This needs to come before your routes
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Define routes
app.get('/', (req, res) => res.send('Hello World! ye'));

// Serve an HTML page with a form at the '/enter-prompt' route
app.get('/enter-prompt', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Enter Prompt for DALL-E</title>
    </head>
    <body>
      <h1>Enter Prompt for DALL-E</h1>
      <form action="/generate-image" method="post">
        <input type="text" name="prompt" placeholder="Enter an image prompt" required>
        <button type="submit">Generate Image</button>
      </form>
    </body>
    </html>
  `);
});

// Endpoint to handle the form submission and talk to DALL-E
app.post('/generate-image', async (req, res) => {
  const prompt = req.body.prompt;
  
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/images/generations',
      {
        prompt: prompt,
        n: 1,
        size: "1024x1024"
      },
      {
        headers: {
          'Authorization': `Bearer ${DALLE_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    const imageSrc = response.data.data[0].url; // Adjust according to the actual response structure

    // Redirect to a new page to display the image
    res.redirect(`/display-image?src=${encodeURIComponent(imageSrc)}`);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error generating image');
  }
});


// New GET endpoint to display the image
app.get('/display-image', (req, res) => {
  const imageSrc = req.query.src;

  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Generated Image</title>
    </head>
    <body>
      <h3>Your generated image:</h3>
      <img src="${imageSrc}" alt="Generated Image" style="max-width:100%;"/>
      <p><a href="/enter-prompt">Generate another image</a></p>
    </body>
    </html>
  `);
});

// Start server
app.listen(port, () => console.log(`Server running on port ${port}`));
