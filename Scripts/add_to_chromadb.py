"""
Use this file to add new files to the ChromaDB used as model memory for RAG
"""

import chromadb
import pandas as pd
import os

# Initialize Chroma client and model
client = chromadb.PersistentClient(path="chroma_db") 
collection = client.get_or_create_collection("excel_data")

# Insert folder path here
folder_path = "INSERT FOLDER PATH HERE"
uuid = 0

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        print(f"Loading {file_path}...")
        df = pd.read_excel(file_path)
        # Convert DataFrame to structured text
        texts = df.apply(lambda row: ', '.join(f"{col}: {row[col]}" for col in df.columns), axis=1).tolist()

        # Embed and store in ChromaDB
        for text in texts:
            collection.add(
                ids=[str(uuid)],
                documents=[text]
            )
            print(f"Insert of embedding ID: {uuid}")
            uuid += 1