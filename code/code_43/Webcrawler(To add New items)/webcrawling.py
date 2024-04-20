import requests
from bs4 import BeautifulSoup
import pymongo
import time
from urllib.parse import urljoin
import cohere
from datetime import datetime
    
    
current_date = datetime.now()
    
year = current_date.year
month = current_date.month
day = current_date.day
    
hash=year*10000+month*100+day
    
product_names=[]
product_links=[]
product_descriptions=[]
product_dim_w=[]
product_dim_h=[]
product_image=[]
    
def scraper_products():        
    wordpress_url ='https://clubartizen.com/catalog/'
    wordpress_url1 = 'https://clubartizen.com/product/'
    gh=0
    dfg='https://clubartizen.com/product/handmade-newspaper-bowl-small/'
    response = requests.get(wordpress_url)
    text_content_list = []
    
    
    if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Replace 'your_class_name' with the actual class name containing the text
            text_class = 'woocommerce-loop-product__title'
            # Find all div tags within the specified class
            text_divs = soup.find_all('h2', class_=text_class)
            my_link = 'woocommerce-LoopProduct-link woocommerce-loop-product__link'
            links = soup.find_all('a', class_=my_link)
            # Create a directory to save the text data
            # Iterate over each text_div in text_divs
            for text_div in text_divs:
                text_content = text_div.get_text(strip=True)
                
                # Check if text_content is not empty
                if text_content:
                    # Write the text_content to the file
                    product_names.append(text_content)
            for link in links:
                href = link.get('href')
                text_content_list.append(href)
                product_links.append(href)
            print('Text data scraped successfully.')
    else:
            print(f'Error: {response.status_code}')
            
    for list in text_content_list:
        response1 = requests.get(list)
        if response1.status_code == 200:
                soup = BeautifulSoup(response1.text, 'html.parser')
                text_class = 'et_pb_module_inner'
                text_divs = soup.find_all('div', class_=text_class)
                count=0
                for text_div in text_divs:
                    paragraph = text_div.find('p')
                    if paragraph :
                            paragraph_text = paragraph.get_text()
                            if "₹" in paragraph_text:
                                gh=gh+1
                                count=1
                            elif count==1 and "stock" not in paragraph_text :
                                product_descriptions.append(paragraph_text)
                                count=0
                            elif count==1 and "stock" in paragraph_text :
                                product_descriptions.append("None")
                                count=2
        else:
                print(f'Error: {response1.status_code}')
                    
    
    c=0
    for list in text_content_list:
        # print(list)
        response1 = requests.get(list)
        if response1.status_code == 200:
                soup = BeautifulSoup(response1.text, 'html.parser')
                text_class = 'et_pb_module_inner'
                text_divs = soup.find_all('div', class_=text_class)
                count=0
                # print(len(text_divs))
                for text_div in text_divs:
                    img_div="woocommerce-product-gallery__wrapper"
                    new1=text_div.find_all('div',class_=img_div)
                    if(new1):
                        for new2 in new1:
                                if(new2):
                                        img = new2.find('a')
                                        if(img):
                                                link = img.get('href')
                                                product_image.append(str(link))
                                        img_tag = new2.find('img')
                                        if img_tag:
                                                # Extract and print the dimensions of the img tag
                                                width = img_tag.get('width')
                                                height = img_tag.get('height')
                                                product_dim_w.append(str(width))
                                                product_dim_h.append(str(height))
        else:
                print(f'Error: {response1.status_code}')
            # c+=1
            # break
    height=400
    width=400
    product_dim_w.append(str(400))
    product_dim_h.append(str(400))
    print(gh)
    
craft_names=[]
craft_links=[]
craft_descriptions=[]
craft_dim_w=[]
craft_dim_h=[]
craft_image=[]
    
def scraper_crafts():
    wordpress_url ='https://clubartizen.com/journal/'
    wordpress_url1 = 'https://clubartizen.com/product/'
    gh=0
    dfg='https://clubartizen.com/product/handmade-newspaper-bowl-small/'
    text_content_list=[]
    response = requests.get(wordpress_url)
    if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Replace 'your_class_name' with the actual class name containing the text
            text_class = 'entry-title'
            # Find all div tags within the specified class
            text_divs = soup.find_all('h4', class_=text_class)
            my_link = 'entry-title'
            links = soup.find_all('h4', class_=my_link)
            # Create a directory to save the text data
            # Iterate over each text_div in text_divs
            for text_div in text_divs:
                text_content = text_div.get_text(strip=True)
                
                # Check if text_content is not empty
                if text_content:
                    # Craft stories heading 
                    craft_names.append(text_content)
            for link in links:
                a_element = link.find('a')
                if a_element:
                    link = a_element.get('href')
                
                craft_links.append(link)
                text_content_list.append(link)
            # print('Text data scraped successfully.')
    else:
            print(f'Error: {response.status_code}')
    #craft stories description
    # print(text_content_list)
    for jk in text_content_list:
        response1 = requests.get(jk)
        # print(jk)
        if response1.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            text_class = 'entry-content'
            text_divs = soup.find_all('div', class_=text_class)
            count=0
            flag=0
            for text_div in text_divs:
                paragraph1 = text_div.find_all('p')
            paragraph2=''
            for paragraph in paragraph1:
                if paragraph :
                        paragraph_text = paragraph.get_text()
                        if '₹' not in paragraph_text:
                            if paragraph_text.endswith('\n'):
                                paragraph_text = paragraph_text[:-1]
                            paragraph2+=paragraph_text
                        if '<br>' in paragraph_text:
                            flag=1
                            break
            if(not(paragraph2)):
                paragraph2=" "
            craft_descriptions.append(paragraph2)
            # print("YAY")
            # count+=1
            # if(count==1):
            #     break
        else:
            print(f'Error: {response1.status_code}')
            
    for jk in text_content_list:
        response1 = requests.get(jk)
        if response1.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            text_class = 'entry-content'
            text_divs = soup.find_all('div', class_=text_class)
            count=0
            flag=0
            for text_div in text_divs:
                img_tag = text_div.find('img')
                if img_tag:
                    img_link = img_tag['src']
                    craft_image.append(img_link)
                    width = img_tag.get('width')
                    height = img_tag.get('height')
                    craft_dim_h.append(str(height))
                    craft_dim_w.append(str(width))
                else:
                    craft_image.append("None")
                    craft_dim_h.append("0")
                    craft_dim_w.append("0")
                # print('Text data scraped successfully.')
        else:
            print(f'Error: {response1.status_code}')
    
blog_names=[]
blog_links=[]
blog_descriptions=[]
blog_dim_w=[]
blog_dim_h=[]
blog_image=[]
    
def scraper_blogs():    
    co = cohere.Client('B398jwxi9t14giGRL4DK01eZJgBD5FaImRON6fOR')
    wordpress_url ='https://clubartizen.com/blogs/'
    wordpress_url1 = 'https://clubartizen.com/product/'
    gh=0
    dfg='https://clubartizen.com/product/handmade-newspaper-bowl-small/'
    text_content_list=[]
    response = requests.get(wordpress_url)
    if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Replace 'your_class_name' with the actual class name containing the text
            text_class = 'entry-title'
            # Find all div tags within the specified class
            text_divs = soup.find_all('h4', class_=text_class)
            my_link = 'entry-title'
            links = soup.find_all('h4', class_=my_link)
            # Create a directory to save the text data
            # Iterate over each text_div in text_divs
            for text_div in text_divs:
                text_content = text_div.get_text(strip=True)
                
                if text_content:
                    blog_names.append(text_content)
            for link in links:
                a_element = link.find('a')
                if a_element:
                    link = a_element.get('href')
            
                blog_links.append(link)
                text_content_list.append(link)
    else:
            print(f'Error: {response.status_code}')
    
    # craft stories description
    for jk in text_content_list:
        response1 = requests.get(jk)
        if response1.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            text_class = 'entry-content'
            text_divs = soup.find_all('div', class_=text_class)
            count=0
            flag=0
            for text_div in text_divs:
                paragraph1 = text_div.find_all('p')
                paragraph2=''
            for paragraph in paragraph1:
                if paragraph :
                        paragraph_text = paragraph.get_text()
                        if '₹' not in paragraph_text:
                            if paragraph_text.endswith('\n'):
                                paragraph_text = paragraph_text[:-1]
                            paragraph2+=paragraph_text
                        if '<br>' in paragraph_text:
                            flag=1
                            break
                        
            blog_descriptions.append(paragraph2)
            count+=1
    
    for jk in text_content_list:
        response1 = requests.get(jk)
        if response1.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            text_class = 'entry-content'
            text_divs = soup.find_all('div', class_=text_class)
            count=0
            flag=0
            for text_div in text_divs:
                img_tag = text_div.find('img')
                if img_tag:
                    img_link = img_tag['src']
                    blog_image.append(img_link)
                    width = img_tag.get('width')
                    height = img_tag.get('height')
                    blog_dim_h.append(str(height))
                    blog_dim_w.append(str(width))
                else:
                    blog_image.append("None\n")
                    blog_dim_h.append("0")
                    blog_dim_w.append("0")
        
    
def create_items_for_database(product_name, url, image_url,description, image_width, image_height, caption, date_to_post, type):
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
        "scrape_date_hash":hash,
    }
    return item
    
def upload_new_products_database():
    co = cohere.Client('B398jwxi9t14giGRL4DK01eZJgBD5FaImRON6fOR')
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://tanaygad:192837465@dass.tqizd9y.mongodb.net/")
    db = client["Initial_database"]
    items_collection = db["items"]
    
    
    
    
    
    # with open("product_links.txt","r") as link:
    i=0
    for line in product_links:
        # line=line[:-1]
        # print(i)
        # i+=1
        query = {"url-link": line}
        results = list(items_collection.find(query))
        h=int(product_dim_h[i])
        w=int(product_dim_w[i])
        img=product_image[i]
        des=product_descriptions[i]
        name=product_names[i]
        if(len(results)>0 or line=='https://clubartizen.com/product/gift-card/'):
            continue
        # print("..")
        # name=name[0:-1]
        # img=img[0:-1]
        # des=des[0:-1]
        # h=h[0:-1]
        # w=w[0:-1]
        # h=int(h)
        # w=int(w)
        i+=1
        time.sleep(15)
        str=''
        caption=''
        response = co.generate(model='command-nightly',prompt = f"make an instagram caption on description: {des} around 50 words and add 10 hashtags ,hashtags and caption both should be in one paragraph",)
        
        result=response.generations[0].text
        # result = response.generations[0].text
        
        paragraphs = result.split('\n')
    
        desired_paragraph = None
        for paragraph in paragraphs:
            if '#' in paragraph:
                desired_paragraph = paragraph
                break
    
        if desired_paragraph:
            print(1)
            print(desired_paragraph)
            # bold_sentence = 'Please read and like our craft stories on the website as it helps our team improve content for our readers' 
            desired_paragraph += '\n'
            caption=desired_paragraph
        else:
            print(2)
        
        count=0
        items = create_items_for_database(name,line,img,des,w,h,caption,"","product")  
        print(items)
        items_collection.insert_one(items)
    
    
def upload_new_crafts_databse():
    co = cohere.Client('B398jwxi9t14giGRL4DK01eZJgBD5FaImRON6fOR')
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://tanaygad:192837465@dass.tqizd9y.mongodb.net/")
    db = client["Initial_database"]
    items_collection = db["items"]
    # print(craft_descriptions)
    # print(craft_names)
    
    # with open("craft_links.txt","r") as link:
    i=1
    for line in craft_links:
        query = {"url-link": line}
        results = list(items_collection.find(query))
        h=int(craft_dim_h[i])
        w=int(craft_dim_w[i])
        img=craft_image[i]
        des=craft_descriptions[i]
        # print(i)
        
        name=craft_names[i]
        if(len(results)>0):
            continue
        # print("..")
        # name=name[0:-1]
        # img=img[0:-1]
        # des=des[0:-1]
        # print(name,line,des)
        # print(h)
        # print(w)
        # h=h[0:-1]
        # w=w[0:-1]
        # h=int(h)
        # w=int(w)
        time.sleep(15)
        i+=1
        str=''
        caption=''
        response = co.generate(model='command-nightly',
                                prompt = f"make an instagram caption without emoji on description: {des} in less than 50 words and add 10 hashtags,hashtags and caption both should be in one paragraph",
                                )
                                
                                
        result=response.generations[0].text
        paragraphs = result.split('\n')
# Iterate through the paragraphs to find the one containing a hashtag
    
    
# Iterate through the paragraphs to find the one containing a hashtag
        desired_paragraph = ''
        for paragraph in paragraphs:
            if '#' in paragraph:
                desired_paragraph = paragraph
                break
    
        if desired_paragraph:
            print(1)
            bold_sentence = 'Read more on our website www.clubartizen.com and like our craft stories as it helps our content team get feedback from readers.' 
            desired_paragraph += '\n' + bold_sentence
            print(desired_paragraph)
            caption=desired_paragraph
        else:
            print(2)
        
        count=0
        items = create_items_for_database(name,line,img,des,w,h,caption,"","craft")  
        print(items)
        items_collection.insert_one(items)
    
    
def upload_new_blogs_database():
    co = cohere.Client('B398jwxi9t14giGRL4DK01eZJgBD5FaImRON6fOR')
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://tanaygad:192837465@dass.tqizd9y.mongodb.net/")
    db = client["Initial_database"]
    items_collection = db["items"]
    # print(blog_descriptions)
    # print(blog_links)
    
    # with open("blog_links.txt","r") as link:
    i=0
    for line in blog_links:
        query = {"url-link": line}
        results = list(items_collection.find(query))
        h=int(blog_dim_h[i])
        # print(i)
        
        w=int(blog_dim_w[i])
        img=blog_image[i]
        des=blog_descriptions[i]
        name=blog_names[i]
        if(len(results)>0):
            continue
        i+=1
        # print("..")
        # print(name,line,des)
        # print(h)
        # print(w)
        time.sleep(15)
        str=''
        caption=''
        response = co.generate(model='command-nightly',prompt = f"make an instagram caption without emoji on description: {des} in less than 50 words and add 10 hashtags,hashtags and caption both should be in one paragraph",)
                                
                                
        result=response.generations[0].text
        paragraphs = result.split('\n')
# Iterate through the paragraphs to find the one containing a hashtag
    
    
# Iterate through the paragraphs to find the one containing a hashtag
        desired_paragraph = ''
        for paragraph in paragraphs:
            if '#' in paragraph:
                desired_paragraph = paragraph
                break
    
        if desired_paragraph:
            print(1)
            bold_sentence = 'Read more on our website www.clubartizen.com and like our blogs as it helps our content team get feedback from readers.' 
            desired_paragraph += '\n' + bold_sentence
            print(desired_paragraph)
            caption=desired_paragraph
        else:
            print(2)
        
        count=0
        items = create_items_for_database(name,line,img,des,w,h,caption,"","blog")  
        print(items)
        items_collection.insert_one(items)
    
        
    
scraper_products()
print("1")
upload_new_products_database()
print("2")
scraper_crafts()
print("3")
upload_new_crafts_databse()
print("4")
scraper_blogs()
print("5")
upload_new_blogs_database()
print("6")