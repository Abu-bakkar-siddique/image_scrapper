import os
from fastapi import FastAPI
from random import randint
from fastapi.responses import FileResponse
from requests import Request
from bs4 import BeautifulSoup
from functions import get_image, generate_random_string, check_url_type, download_many_imgs, get_img_urls

app = FastAPI()

@app.get("/download_image")
async def download_image(url: str) : # downloading the image
    url_type = check_url_type(url)

    # if single image
    if url_type == "image":
        Dir = "images"
        #random_dir_name = generate_random_string() # creating a directory with random name
                                              # this will be deleted later, no worries
        os.makedirs(Dir)
        file_name = get_image(url, Dir)

        if not file_name.endswith(".png"):
            return {"status": file_name}
            
        else:
            return FileResponse(file_name)
            
    # if the inputed url is of an html page
    elif url_type == "html":
        dir = "images"
        #random_dir = generate_random_string() # creating a directory with random name this will be deleted later,so no worries
        
        os.makedirs(dir)
        all_urls =  get_img_urls(url)

        # fails has all urls that were not downloaded (just in case)
        file_names = download_many_imgs(all_urls, dir)
        return {"File names" : file_names}
        # return FileResponse()
    else:
        return {"Error message" : "Document type has to be image or html only"}

    