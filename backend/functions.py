import numpy as np
from model import products, products_embed, encode_model, model, tokenizer
# - - - - - - - - - - - - -
#      Model Functions
# - - - - - - - - - - - - -

#Creates prompt to send to model
def get_RAG_prompt(products, query, products_embed, e_model, topI = 2):
    query_embed = e_model.encode(query, normalize_embeddings=True)
    similarities = np.dot(products_embed, query_embed.T)
    top_I_index = np.argsort(similarities, axis = 0)[-topI:][::-1].tolist()
    most_similar_docs = [products[i] for i in top_I_index]

    prompt = f"""
    You are a product expert working at a snowboard shop.
    Given the user request: "{query}",
    And the following product descriptions:

    {chr(10).join(f"- {name}" for name in most_similar_docs)}

    Answer the user request as **objectively** as possible, DO NOT rephrase the question asked, and DO NOT repeat the user request back to the user.
    """
    return(prompt)


#Retrieves response of model
def getModelResponse(chat, query, topI = 2):
    prompt = get_RAG_prompt(products, query, products_embed, encode_model, topI)
    #response = chat(prompt, max_new_tokens=1000, do_sample=True, temperature=1.0)[0]['generated_text']
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    output = model.generate(
        input_ids,
        max_new_tokens=1000,
        do_sample=True,
        temperature=1.0
    )
    
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return output_text.replace(prompt, "").strip()

# - - - - - - - - - - - - -
#      Scrape Functions
# - - - - - - - - - - - - -
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import json
from yt_dlp import YoutubeDL
from IPython.display import clear_output
import time

from tqdm import tqdm
tqdm.pandas()

def getPage(url):
    http = httplib2.Http()
    status, response = http.request(url)
    return response

def filterProductLinks(response, category):
    #filter out all links from HTML response
    soup = BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a'))

    links=[]
    #filtering by all links that are product pages we want
    for link in soup:
        if link.has_attr('href') and category in link['href'] and "shop" not in link['href']:
            links.append(link['href'])
    return links

def collectURLs(main_url, category):
    i = 1
    links = []
    while True:
        #Moves through the pages in the store as needed
        temp_url = main_url + "/p_{}".format(i) if i != 1 else main_url

        #Collects all present URLs on page with BeautifulSoup library    
        response = getPage(temp_url)
        new_links = filterProductLinks(response, category)

        #If there are no product links, we are complete
        if not new_links:
            break

        links.extend(new_links)
        #Go to next page
        i+=1
    return links

def getNameDescription(soup):
    text, product_name, old_string, to_append = "", "", "", 0
    for i, string in enumerate(soup.stripped_strings):
        #the previous line before sku# is AlWAYS the product's name
        if "sku#" in string:
            product_name = old_string
        #Once we see "Specs", we are no longer interested in the info on the page
        if string == "Specs" or string == "Effective Edge (mm)":
            to_append = 0
        #if info is in the product details, we append to our main text
        if to_append == 1:
            text = text + " " + string
        #We want to search for everything in the product details section
        if string == "Product Details":
            to_append = 1
        #overwrite before going to the next line
        old_string = string
    return product_name, text

def collectProductInfo(links, main_url):
    products = []
    for i, link in enumerate(links):
        if i % 100 == 0:
            clear_output(wait=True)
            print(f"Current progress: {i}/{len(links)} products processed.")
        combined_url = main_url + link
        #get html
        response = getPage(combined_url)

        #parse plaintext
        soup = BeautifulSoup(response, 'html.parser')

        #collect name and description of product and append to product list
        product_name, text = getNameDescription(soup)
        products.append({'name': product_name, 'description': text.strip()})
    return products

def jsonDump(filename, contents):
    with open(f"{filename}.json", "w") as f:
        json.dump(contents, f, indent=2)
    return True

def createProductJSON():
    #Collect the links to each product page
    links = collectURLs("https://www.evo.com/shop/snowboard/snowboards/condition_new", "snowboards/") + collectURLs("https://www.evo.com/shop/snowboard/bindings/condition_new", "bindings/")
    
    #Next, we will collect the text from every single product page that we are interested in
    products = collectProductInfo(links, "https://www.evo.com")

    #Create json file
    jsonDump("products", products)
    clear_output(wait=True)
    print("JSON file successfully created")
    return True