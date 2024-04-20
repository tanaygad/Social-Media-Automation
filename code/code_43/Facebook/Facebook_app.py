#!pip install facebook-sdk
import facebook as fb
from flask import Flask, jsonify
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()
access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
fb_auto = fb.GraphAPI(access_token)


@app.route('/')
def start():
    return "This is our webserver to post on  facebook"


@app.route('/post_to_facebook', methods=['POST', 'GET'])
def post_to_facebook():
    server_url = "https://flask-heroku-server-3.onrender.com/post"
    response = requests.get(server_url)
    print(response)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)
        # message = facebook(data)
        image_url = data['image_url']
        description = data['description']
        height = data['height']
        width = data['width']
        platform = data['platform']
        if (platform == 2 or platform == 4 or platform == 6):
            # Fetch the image data from the URL
            image_data = requests.get(image_url).content
    
            # Open the image using PIL
            img = Image.open(BytesIO(image_data))
    
            #Resize the image
            img = img.resize((width, height))
            
            # Load logo image
            logo_url = "https://github.com/Samarth23-sudo/ClubArtizen/blob/main/Club%20Artizen%20Logo%20Circle.png?raw=true"
            logo_data = requests.get(logo_url).content
            logo_img = Image.open(BytesIO(logo_data))
            # Resize logo image if needed
            logo_img = logo_img.convert("RGBA")
            logo_img_with_transparency = Image.new("RGBA", logo_img.size, (255, 255, 255, 0))
            logo_img_with_transparency.paste(logo_img, (10, 10), logo_img)
    
            # Resize logo image if needed
            logo_img_with_transparency = logo_img_with_transparency.resize((int(width/6), int(width/6)))  # Adjust size as necessary
    
            # Paste logo image onto original image at top left corner
            img.paste(logo_img_with_transparency,(0, 0), logo_img_with_transparency)
    
            # Convert the image back to bytes
            img.save('final_image.jpg')
            resized_image_data = BytesIO()
            img.save(resized_image_data, format='JPEG')
    
            # Use the resized image data in your Facebook API code
            fb_auto.put_photo(image=resized_image_data.getvalue(),message=description)
            print("Posted Successfuly")
            return jsonify({"message": "Posted Successfuly"})
        return jsonify({"message": "Accessed Successfuly"})
    else:
        print("Failed to fetch data from the server:", response.status_code)
        return jsonify({"message": "doc not found"})


# def facebook(data):
#     print(data)
    
#     return "get_info function executed successfully"

if __name__ == '__main__':
    app.run()
