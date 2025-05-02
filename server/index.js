const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path');

const app = express();
app.use(cors());

const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    const filePath = req.file.path;
    const form = new FormData();
    form.append('image', fs.createReadStream(filePath));

    const response = await axios.post('http://localhost:5001/analyze', form, {
      headers: {
        ...form.getHeaders()
      }
    });

    fs.unlinkSync(filePath); // clean up temp file

    res.json(response.data);
  } catch (error) {
    console.error('Error uploading to Flask:', error.message);
    res.status(500).json({ error: 'Failed to analyze image' });
  }
});

app.listen(5000, () => {
  console.log('Server is running on port 5000');
});
