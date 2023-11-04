import os
import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/generate-image', methods=['POST', 'GET'])
def generate_image():

    prompt = "dog with sunglasses"
    openai.api_key = os.getenv("DALLE_API_KEY")

    if not openai.api_key:
        return jsonify({'error': 'API key not found'}), 403

    try:
        # Call the OpenAI API to generate an image
        response = openai.Image.create(
            prompt=prompt,
            n=1,  
            size="1024x1024"
        )

        # Extract the image URL(s) from the response
        # Adjust the following line according to the actual response structure
        image_urls = [data['url'] for data in response['data']]

        # Send back the image URLs in the response
        return jsonify({'images': image_urls})

    except openai.error.OpenAIError as e:
        # Handle OpenAI specific errors
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        # Handle other possible errors
        #return jsonify({'error': 'An error occurred while generating the image'}), 500
        return render_template('show_image.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
