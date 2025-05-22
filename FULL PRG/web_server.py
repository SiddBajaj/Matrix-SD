from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Function to generate voice prompts
def generate_prompts():
    # Generate prompts and send them to the webpage
    while True:
        # Example: Send voice prompt "Hello, I am Matrix" to the webpage
        prompt = "Hello, I am Matrix"
        # Code to send prompt to the webpage
        time.sleep(5)  # Wait for 5 seconds before sending the next prompt

# Endpoint to receive commands from the webpage
@app.route('/receive_command', methods=['POST'])
def receive_command():
    data = request.json
    command = data['command']
    # Process the command received from the webpage
    # Example: If command is "activate", start the main loop
    if command == "activate":
        # Code to handle the "activate" command
        return jsonify({"status": "success"})

# Function to start the Flask web server
def start_server():
    app.run(debug=True, port=8080, threaded=True)

if __name__ == '__main__':
    threading.Thread(target=generate_prompts).start()
    start_server()
