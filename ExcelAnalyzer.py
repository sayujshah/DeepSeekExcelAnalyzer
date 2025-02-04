import pandas as pd
from huggingface_hub import InferenceClient
from openai import OpenAI
import chromadb
from typing import Optional

DEFAULT_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

class ExcelAnalyzer:
    def __init__(self, model_name: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        # Initialize HuggingFace client
        self.model_name = model_name
        self.api_key = api_key
        self.client = InferenceClient(model=model_name) if api_key == None else OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.df = None

        # Initialize ChromaDB for RAG storage
        self.chromadb = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.chromadb.get_collection("excel_data")

    def load_excel(self, file):
        """Load and validate Excel file"""
        try:
            self.df = pd.read_excel(file.name)
            return "Excel file loaded and indexed successfully."
        
        except Exception as e:
            return f"Error loading file: {str(e)}"
    
    def store_in_chroma_db(self, file):
        try:
            self.df = pd.read_excel(file.name)
            # Convert DataFrame to structured text
            texts = self.df.apply(lambda row: ', '.join(f"{col}: {row[col]}" for col in self.df.columns), axis=1).tolist()
            
            uuid = self.collection.count()
            # Embed and store in ChromaDB
            for text in texts:
                self.collection.add(
                    ids=[str(uuid)],
                    documents=[text]
                )
                uuid += 1
            self.store = False
            return f"File '{file.name}' successfully stored in ChromaDB."
        
        except Exception as e:
            return f"Error loading file: {str(e)}"
    
    def retrieve_relevant_data(self, question):
        """Retrieve relevant rows from vector DB based on the question"""
        results = self.collection.query(query_texts=[question], n_results=5)  # Retrieve top 5 similar results
        retrieved_data = "\n".join(results["documents"][0]) if results["documents"] else "No relevant data found."
        
        return retrieved_data

    def generate_response(self, question):
        """Main text generation function"""
        if self.df is None:
            return "Please upload an Excel file first."
        
        try:
            # Retrieve relevant rows from the vector database
            relevant_data = self.retrieve_relevant_data(question)
            
            # Construct the context-enhanced prompt
            context = f"""
            You are an expert data analyst. Analyze the relevant data below to answer the user's question. 
            Generate only the response to the user's question based on your analysis of the data.

            ###RELEVANT DATA FROM EXCEL###
            {relevant_data}
            
            ###QUESTION###
            {question}
            """
            
            # Query the LLM
            if self.api_key is None:
                response = self.client.text_generation(
                    context,
                    temperature=0.2,
                    return_full_text=False
                )
                return response.strip()
            else:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are an expert data analyst."},
                        {"role": "user", "content": context},
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"Error during analysis: {str(e)}"