const express = require("express");
const path = require("path");
const app = express();

const PORT = process.env.PORT || 3000;

// Serve all static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// (Optional) Handle 404s
app.use((req, res) => {
  res.status(404).send("404 Not Found");
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
