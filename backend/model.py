import pandas as pd
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

model_id = "google/gemma-2b-it"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

#Collect dataset
dataset = load_dataset("json", data_files = "products.json")
product_data=dataset["train"].to_list()

#Encode for RAG
encode_model = SentenceTransformer("all-MiniLM-L6-v2", trust_remote_code=True)
products = [f"{item['name']}: {item['description']}" for item in product_data]
productnames = [f"{item['name']}" for item in product_data]
products_embed = encode_model.encode(productnames, normalize_embeddings=True)
