from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # Extract the prompt from the request
    prompt = request.json.get('prompt')

    # Your DALL-E generation code will go here
    # For now, we'll just return the prompt as a JSON
    return jsonify({'prompt': prompt})

if __name__ == '__main__':
    app.run(debug=True)
