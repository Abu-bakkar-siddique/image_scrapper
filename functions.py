import os
import string
import random
import requests 
from urllib.parse import urlparse, urljoin
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO

#returns the path to the downloaded image

def get_image(url: str, directory : str):
    num = random.randint(1,10000000000)
    response = requests.get(url)

    if response.status_code != 200:
        return response.status_code
        
    image = response.content
    image_path = f"{directory}/image{num}.png" 
    
    with open(image_path, "wb") as file:
        file.write(image)

    return image_path

def generate_random_string():
    length = 20
    letters = string.ascii_letters  # Uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))


#func1: A function that takes a url, and checks it the url leads to a webpage or an image
def check_url_type(url: str) -> str: 
   
    response = requests.get(url)
    type = response.headers["Content-Type"].lower()

    if type[0:5] =='image':
        return "image"
    
    elif type[5:9] == 'html':
        return 'html'
     
    else:
        return 'invalid'


# func2: A function that would return all the image URLs in a url of a webpage
# or a website that it took as an input.
def get_img_urls(url: str) -> list:

    #extracting base url
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    img_links = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        imgs = soup.find_all('img')
        
        for img in imgs:
            src_value = img.get('src')
            src_value = str(src_value)
            if src_value:

                #checking if the url is a relative url
                if not src_value.startswith(("http", "https")):

                    src_value = urljoin(base_url, src_value)
                    img_links.append(src_value)
                img_links.append(src_value)
                
    except requests.RequestException as e:
        print(f"Error: {str(e)}")

    return img_links

# A function to download all the images to the urls returned by func2
def download_many_imgs(links: list, dir: str): # returns a list of filenames downloaded

    fails = [] # this list will have all the failed links
    filenames = [] # all the downloaded filenames
    for link in links:
        path = get_image(link, dir)

        if path.endswith(".png"):
            filenames.append(path)
    return filenames


#function to exrtract base url
def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url
