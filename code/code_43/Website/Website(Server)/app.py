from flask import Flask, jsonify
from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

password="password"

# MongoDB connection URI
uri = "mongodb+srv://tanaygad:192837465@dass.tqizd9y.mongodb.net/"
client = MongoClient(uri)


@app.route('/')
def start():
    return "This is our webserver"
# Define a route to handle the AJAX request

@app.route('/jtop', methods=['POST', 'GET'])
def jtop():
    try:
        data = request.json
        password1 = data['password']
        print("Yay")
        print(password1)
        passflag=0
        if(password1==password):
            passflag=1
        print(passflag)
        return jsonify(passflag=passflag),200
    
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500

@app.route('/rej', methods=['POST', 'GET'])
def rej():
    try:
        data = request.json
        url = data['url']
        approval = data['approved']
        date = data['date']
        print("Yay")
        print(url)
        # Process the received data as needed

        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        document = collection.find_one({'url-link': url})
        if document:
            print("Received URL:", url)
            print("approved:", approval)
            print("date:", date)
        else:
            print("huh")
        # Update the description
        collection.update_many(
        {'url-link': url},
        {'$set': {'approved': -1}}
        )
        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500


@app.route('/edit', methods=['POST', 'GET'])
def editmodify():
    try:
        print("yeahhhhhh")
        data = request.json
        url = data['url']
        caption = data['caption']
        date = data['date']
        time = data['time']
        print("Yay")
        print(url)
        # Process the received data as needed

        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        document = collection.find_one({'url-link': url})
        if document:
            print("Received URL:", url)
            # print("Caption:", caption)
            print("date:", date)
        else:
            print("huh")
        # Update the description
        collection.update_one(
        {'url-link': url},
        {'$set': {'caption': caption}}
        )
        # date="2024-01-01"
        collection.update_one(
        {'url-link': url},
        {'$set': {'date_to_post': date}}
        )
        collection.update_one(
        {'url-link': url},
        {'$set': {'time': time}}
        )
        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500


@app.route('/view-doc')
def get_view_doc():
    try:
        # print("ubwebvhwefbhjwevjk")
        database = client['Initial_database']
        collection = database['items']
        documents = collection.find(
            {'approved': {'$in': [1, 2, 3, 4, 5, 6]}, 'recommended': 0})
        print(documents)
        lst = []
        print("!!!")
        if (1):
            print("YAY")
            for document in documents:
                if document:
                    print(document)
                    d = {}
                    # Assuming the image URL is stored in a field called 'image-url'
                    d['image_url'] = document['image-url']
                    d['description'] = document['caption']
                    d['url'] = document['url-link']
                    d['date'] = document['date_to_post']
                    d['time'] = document['time']
                    d['name']=document['name']
                    print(document['date_to_post'])
                    lst.append(d)
                    # return jsonify(image_url=image_url,description=description,url=url)  # Send the image URL as JSON
                # else:
                    # return jsonify(error='Document not found'), 404
        return jsonify(lst), 200
    except Exception as e:
        print(":(")
        return jsonify(error=str(e)), 500


@app.route('/get-image-url')
def get_image_url():
    try:
        database = client['Initial_database']
        collection = database['items']
        document1 = collection.find_one(
            {'approved': 0, 'recommended': 0, 'type': "product"})
        document2 = collection.find_one(
            {'approved': 0, 'recommended': 0, 'type': "craft"})
        document3 = collection.find_one(
            {'approved': 0, 'recommended': 0, 'type': "blog"})
        print(document1)
        if document1:
            # Assuming the image URL is stored in a field called 'image-url'
            image_url1 = document1['image-url']
            description1 = document1['caption']
            url1 = document1['url-link']
            image_url2 = ""
            image_url3 = ""
            url2 = ""
            url3 = ""
            description2 = ""
            description3 = ""
            name1=document1['name']
            name2=''
            name3=''
            if (document2):
                # Assuming the image URL is stored in a field called 'image-url'
                image_url2 = document2['image-url']
                description2 = document2['caption']
                url2 = document2['url-link']
                name2=document2['name']
            if (document3):
                # Assuming the image URL is stored in a field called 'image-url'
                image_url3 = document3['image-url']
                description3 = document3['caption']
                url3 = document3['url-link']
                name3=document3['name']
            # Send the image URL as JSON
            return jsonify(image_url1=image_url1, description1=description1, url1=url1, image_url2=image_url2, description2=description2, url2=url2, image_url3=image_url3, description3=description3, url3=url3,name1=name1,name2=name2,name3=name3)
            # 1-product 2-craft 3-blog
        else:
            return jsonify(error='Document not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/send-edited-response', methods=['POST', 'GET'])
def receive_edited_content():
    try:
        data = request.json
        url = data['url']
        updated_data = data['updateData']

        # Process the received data as needed
        print("Received URL:", url)
        print("Updated Data:", updated_data)

        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        document = collection.find({'url-link': url})
        if document:
            # Update the description
            collection.update_many(  # change this to update many
                {'url-link': url},
                {'$set': {'caption': updated_data}}
            )

        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500


@app.route('/post')
def get_post_ready():
    try:
        database = client['Initial_database']
        collection = database['items']
        today_date = datetime.today().strftime('%Y-%m-%d')
        current_time = datetime.now()
        current_hour = current_time.hour
        current_hour_int = int(current_hour)
        current_hour_int+=6                         #UTC is 5 and half hours behind
        print(current_hour_int)
        document_1 = collection.find_one(
            {'approved': {'$in': [1, 2, 3, 4, 5, 6]}, 'recommended': 2, 'date_to_post': today_date, 'time':current_hour_int})
        if (document_1 != None):
            # Assuming the image URL is stored in a field called 'image-url'
            print(document_1)
            image_url = document_1['image-url']
            description = document_1['caption']
            height = document_1['img-height']
            width = document_1['img-width']
            url = document_1['url-link']
            platform = document_1['approved']
            time = document_1['time']
            collection.update_many(
                    {'url-link': url},
                    {'$set': {'recommended': 1}}
                )

            # Send the image URL as JSON
            return jsonify(image_url=image_url, description=description, width=width, height=height, platform=platform)
        else:
            document = collection.find_one(
                {'approved': {'$in': [1, 2, 3, 4, 5, 6]}, 'recommended': 0, 'date_to_post': today_date,'time':current_hour_int})
            if document:
                print(document)
                image_url = document['image-url']
                description = document['caption']
                height = document['img-height']
                width = document['img-width']
                url = document['url-link']
                platform = document['approved']
                time = document['time']
                if (platform == 4 or platform == 6):
                        collection.update_many(
                        {'url-link': url},
                        {'$set': {'recommended': 2}}
                    )
                else:
                    collection.update_many(
                        {'url-link': url},
                        {'$set': {'recommended': 1}}
                    )
                # Send the image URL as JSON
                return jsonify(image_url=image_url, description=description, width=width, height=height, platform=platform)

            else:
                return jsonify(error='Document not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/send-approval', methods=['POST', 'GET'])
def receive_approval():
    try:
        data = request.json
        url = data['url']
        approval = data['approved']
        date = data['date']
        # Process the received data as needed

        # Here you can perform further processing or return a response
        # For example, return a success message
        database = client['Initial_database']
        collection = database['items']
        time=data['time']
        document = collection.find_one({'url-link': url})
        if document:
            print("Received URL:", url)
            print("approved:", approval)
            print("date:", date)
        # Update the description
        collection.update_many(
        {'url-link': url},
        {'$set': {'approved': approval, 'date_to_post': date,'time':time}}
        )
        return {'message': 'Data received successfully'}, 200
    except Exception as e:
        # Handle any exceptions that occur during processing
        print("Error:", e)
        return {'error': 'An error occurred'}, 500

 
# if __name__ == '__main__':
#     app.run(debug=True)  # Run the Flask app in debug mode