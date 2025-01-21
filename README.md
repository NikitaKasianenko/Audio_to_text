##Audio-to-Text Conversion Website



#Install using pip:

pip install -r req.txt

#Navigate to the directory containing the app.py file.

Run the Flask server:

python app.py

The server will start at http://127.0.0.1:5000.

Start the Frontend:

Open the index.html file in a browser, or use a local web server to host it (e.g., with VSCode Live Server).

Usage

Open the website in your browser.

Upload an audio file using the interface.

Wait for the file to be processed and the transcription to appear in the text box.

Troubleshooting

Common Errors

Error: [WinError 2] The system cannot find the file specified

Ensure ffmpeg is installed and added to your PATH.

Verify installation with:

ffmpeg -version

Error: 500 Internal Server Error

Check the Flask server logs for more details.

Ensure the transcription API key and configuration are correct.

CORS Issues:

Make sure Flask-CORS is properly configured in the backend:

from flask_cors import CORS
CORS(app)

