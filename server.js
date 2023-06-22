const express = require('express');
const app = express();
const port = 3000;

// Middleware to parse JSON data
app.use(express.json());

// Read user data from JSON file
const users = require('./users.json');

// Read bank activities data from JSON file
const bankActivities = require('./bankActivities.json');

// Define routes
app.get('/api/v2/users', (req, res) => {
  res.json(users);
});

app.get('/api/v2/users/:userId/activities', (req, res) => {
  const userId = req.params.userId;
  const userActivities = bankActivities.filter((activity) => activity.user_id == userId);
  res.json(userActivities);
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
