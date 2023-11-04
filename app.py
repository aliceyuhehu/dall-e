import json
import os
import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
promptdefault = "detailed image"

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/prompt', methods =["POST", "GET"])
def prompting():
    if request.method == "POST":
       story_prompt = request.form.get("sprompt")
       # getting input with name = name in HTML form 
       character_name = request.form.get("cname") 
       global promptdefault
       promptdefault = story_prompt
       img_url = generate_image()
       return render_template("testing.html", image_url=img_url)
    return render_template("prompting.html")

@app.route('/testing', methods=['POST', 'GET'])
def loading():
    return render_template('testing.html')

@app.route('/generate-image', methods=['POST', 'GET'])
def generate_image():
    openai.api_key = os.getenv("DALLE_API_KEY")
    global promptdefault

    if not openai.api_key:
        return jsonify({'error': 'API key not found'}), 403

    try:
        # Call the OpenAI API to generate an image
        response = openai.Image.create(
            prompt=promptdefault,
            n=1,  
            size="1024x1024"
        )

        # Extract the image URL(s) from the response
        # Adjust the following line according to the actual response structure
        image_urls = [data['url'] for data in response['data']]
        # Send back the image URLs in the response
        #jsonify({'images': image_urls})
        return image_urls[0]
        #return render_template("testing.html", image_url=website_url)

    except openai.error.OpenAIError as e:
        # Handle OpenAI specific errors
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        # Handle other possible errors
        #return jsonify({'error': 'An error occurred while generating the image'}), 500
        return render_template('prompting.html', image_url=website_url)

if __name__ == '__main__':
    app.run(debug=True)