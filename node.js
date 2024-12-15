const express = require('express');
const multer = require('multer');
const axios = require('axios');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

const API_KEY = 'your-api-key';
const API_SECRET = 'your-secret-key';

app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        const file = req.file;

        // Authenticate with Copyleaks API
        const authResponse = await axios.post('https://id.copyleaks.com/v3/account/login/api', {
            key: API_KEY,
            secret: API_SECRET,
        });

        const authToken = authResponse.data.access_token;

        // Upload file for scanning
        const scanResponse = await axios.post(
            'https://api.copyleaks.com/v3/education/submit/file',
            fs.createReadStream(file.path),
            {
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'multipart/form-data',
                },
            }
        );

        // Clean up uploaded file
        fs.unlinkSync(file.path);

        res.json(scanResponse.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
