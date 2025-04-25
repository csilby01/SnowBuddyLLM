from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import json
import requests
import transformers
from transformers import pipeline, AutoTokenizer, Gemma3ForCausalLM, GenerationConfig, AutoModelForCausalLM
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

import torch
import evaluate
import time

from tqdm import tqdm
tqdm.pandas()

model_id = "google/gemma-2b-it"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Inference pipeline
chat = pipeline("text-generation", model=model, tokenizer=tokenizer)

dataset = load_dataset("json", data_files = "products.json")
product_data=dataset["train"].to_list()
encode_model = SentenceTransformer("all-MiniLM-L6-v2", trust_remote_code=True)
products = [f"{item['name']}: {item['description']}" for item in product_data]
productnames = [f"{item['name']}" for item in product_data]
products_embed = encode_model.encode(productnames, normalize_embeddings=True)

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

def getModelResponse(chat, query, topI = 2):
    prompt = get_RAG_prompt(products, query, products_embed, encode_model, topI)
    response = chat(prompt, max_new_tokens=1000, do_sample=True, temperature=1.0)[0]['generated_text']
    return response.replace(prompt, "").strip()

app = Flask(__name__)
CORS(app)

#query API route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # You can replace this with your LLM logic
    reply = getModelResponse(chat, user_message)

    return jsonify({'reply': reply})

if __name__ == "__main__":
    app.run(debug="true")