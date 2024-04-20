import pymongo
 
# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://tanaygad:192837465@dass.tqizd9y.mongodb.net/")
db = client["Initial_database"]
items_collection = db["items"]
 
# db.dropDatabase()
 
 
 
# Define a function to create items for each product
def create_items_for_product(product_name, url, image_url,description, image_width, image_height, caption, date_to_post, type, time, date_hash):
    # Example: you can define your item structure here
    # This is just a placeholder
    item = {
        "name": f"{product_name}",
        "image-url": f"{image_url}",
        "url-link": f"{url}",
        "recommended": 0,
        "approved": 0,
        "description": f"{description}",
        "caption": f"{caption}",
        "img-width": image_width,
        "img-height": image_height,
        "platform": 0,                           # 1-> insta, 2->facebook, 3->both, 0->none
        "date_to_post": date_to_post,
        "type": f"{type}",
        "time": f"{time}",
        "scrape_date_hash": date_hash
    }
    return item
 
def update_item_to_approved(url_link, approved_val):
    # Update the item to approved = 1
    query = {"url-link": url_link}
    new_values = {"$set": {"approved": approved_val}}
 
    # Update one document that matches the query
    result = items_collection.update_one(query, new_values)
 
def update_item_to_recommended(url_link, recommended_val):
    # Update the item to approved = 1
    query = {"url-link": url_link}
    new_values = {"$set": {"recommended": recommended_val}}
 
    # Update one document that matches the query
    result = items_collection.update_one(query, new_values)
 
# Iterate over each product name
    # Read the file containing product names
def load_database():
    with open("product_names.txt", "r") as file:
        product_names = file.readlines()
    with open("product_links.txt","r") as file:
        product_links = file.readlines()
    with open("product_image.txt","r") as file:
        product_images = file.readlines()
    with open('product_descriptions.txt', 'r') as file:
        segments = file.read()
        segment_list = segments.split('---\n')
    with open('product_captions.txt', 'r', errors = 'ignore') as file:
        caption = file.read()
        caption_list = caption.split('---\n')
    with open("product_dim_w.txt","r") as file:
        image_width = file.readlines()
    with open("product_dim_h.txt","r") as file:
        image_height = file.readlines()
    
 
    for i in range(0,len(product_names)):
        name = product_names[i].strip()  # Remove leading/traili    ng whitespaces
        link = product_links[i].strip()
        image = product_images[i].strip()
        desc = segment_list[i]
        cap = caption_list[i]
        if (cap[0]=='"'):
            cap = cap[1:-1]
        img_w = image_width[i]
        img_w = img_w[:-1]
        img_w = int(img_w)
        img_h = image_height[i]
        img_h = img_h[:-1]
        img_h = int(img_h)
        # Create items for the product
        items = create_items_for_product(name,link,image,desc,img_w,img_h,cap,"","product","18:00",0)  
 
        # Insert items into MongoDB
        items_collection.insert_one(items)
    with open("craft_names.txt", "r") as file:
        craft_names = file.readlines()
    with open("craft_links.txt","r") as file:
        craft_links = file.readlines()
    with open("craft_image.txt","r") as file:
        craft_images = file.readlines()
    with open('craft_descriptions.txt', 'r') as file:
        segments = file.read()
        segment_list = segments.split('---\n')
    with open('craft_captions.txt', 'r', errors = 'ignore') as file:
        caption = file.read()
        caption_list = caption.split('---\n')
    with open("craft_dim_w.txt","r") as file:
        image_width = file.readlines()
    with open("craft_dim_h.txt","r") as file:
        image_height = file.readlines()
    
    for i in range(0,len(craft_names)):
        name = craft_names[i].strip()  # Remove leading/traili    ng whitespaces
        link = craft_links[i].strip()
        image = craft_images[i].strip()
        desc = segment_list[i]
        cap = caption_list[i]
        cap = cap + "Read more on our website www.clubartizen.com and like our craft stories as it helps our content team get feedback from readers."
        if (cap[0]=='"'):
            cap = cap[1:-1]
        img_w = image_width[i]
        img_w = img_w[:-1]
        img_w = int(img_w)
        img_h = image_height[i]
        img_h = img_h[:-1]
        img_h = int(img_h)
        # Create items for the product
        items = create_items_for_product(name,link,image,desc,img_w,img_h,cap,"","craft","18:00",0)  
 
        # Insert items into MongoDB
        items_collection.insert_one(items)
    with open("blog_names.txt", "r") as file:
        blog_names = file.readlines()
    with open("blog_links.txt","r") as file:
        blog_links = file.readlines()
    with open("blog_image.txt","r") as file:
        blog_images = file.readlines()
    with open('blog_descriptions.txt', 'r') as file:
        segments = file.read()
        segment_list = segments.split('---\n')
    with open('blog_captions.txt', 'r', errors = 'ignore') as file:
        caption = file.read()
        caption_list = caption.split('---\n')
    with open("blog_dim_w.txt","r") as file:
        image_width = file.readlines()
    with open("blog_dim_h.txt","r") as file:
        image_height = file.readlines()
    
    for i in range(0,len(blog_names)):
        name = blog_names[i].strip()  # Remove leading/traili    ng whitespaces
        link = blog_links[i].strip()
        image = blog_images[i].strip()
        desc = segment_list[i]
        cap = caption_list[i]
        cap = cap + "Read more on our website www.clubartizen.com and like our craft stories as it helps our content team get feedback from readers."
        if (cap and cap[0]=='"'):
            cap = cap[1:-1]
        img_w = image_width[i]
        img_w = img_w[:-1]
        img_w = int(img_w)
        img_h = image_height[i]
        img_h = img_h[:-1]
        img_h = int(img_h)
        # Create items for the product
        items = create_items_for_product(name,link,image,desc,img_w,img_h,cap,"","blog","18:00",0)  
 
        # Insert items into MongoDB
        items_collection.insert_one(items)
    
 
 
load_database()
# update_item_to_approved("https://clubartizen.com/product/upcycled-toran-set-of-four/",1)
 
 
 
 