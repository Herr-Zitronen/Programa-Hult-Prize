import io
import re
import os
import requests
import time
import json
from PyPDF2 import PdfReader
from docx import Document

class AIEngine:
    def __init__(self):
        # Updated to Router URL with /hf-inference path
        self.api_url = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2"
        self.api_token = os.environ.get("HF_TOKEN")
        print("AI Engine initialized via Hugging Face Router API.")

    def extract_text_from_pdf(self, file_bytes):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""

    def extract_text_from_docx(self, file_bytes):
        try:
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_embedding(self, text: str):
        # Call Hugging Face API
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        else:
            print("Warning: HF_TOKEN not set. API calls might fail.")
        
        # Payload must be a list for Feature Extraction pipeline to work correctly
        payload = {"inputs": [text]}
        
        # Retry logic for model loading (503)
        max_retries = 1
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    # Data should be a list of embeddings (list of lists)
                    if isinstance(data, list) and len(data) > 0:
                        # We sent one input, so we take the first result
                         if isinstance(data[0], list):
                            # data[0] is the embedding vector [0.1, 0.2, ...]
                            # Sometimes API returns [[[0.1...]]] (3D) if batching is weird, but usually 2D.
                            # Standard Feature Extraction: [ [embedding_vector] ]
                            return data[0]
                         # If it's just [0.1, 0.2] (unexpected for list input but possible)
                         return data
                    
                    return [0.0] * 384 # Unexpected format fallback

                elif response.status_code == 503:
                    # Model loading... wait and retry
                    if attempt < max_retries:
                        print(f"HF API 503 (Model Loading). Retrying in 2s... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(2)
                        continue
                    else:
                         print("HF API 503: Model still loading after retry.")

                else:
                    print(f"HF API Failed. Status: {response.status_code}")
                    print(f"Response: {response.text}")
                    break # Don't retry other errors blindly

            except Exception as e:
                print(f"HF API Exception: {e}")
                break
        
        # Fallback: Zero vector
        print("Using Fallback Zero Vector due to API failure.")
        return [0.0] * 384

    def calculate_similarity(self, embedding1, embedding2):
        # Manual Cosine Similarity (No numpy/scikit-learn)
        
        if not embedding1 or not embedding2:
            return 0

        # Dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Magnitudes
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
            
        similarity = dot_product / (magnitude1 * magnitude2)
        
        # Clamp between 0 and 1
        similarity = max(0.0, min(1.0, similarity))
        
        return int(similarity * 100)

    def extract_keywords(self, text: str, role_text: str = ""):
        # Simple Explainability Logic (Regex based)
        
        def tokenize(s):
            # Lowercase and split by non-alphanumeric
            words = re.findall(r'\b[a-z]{3,}\b', s.lower())
            return set(words)

        cv_tokens = tokenize(text)
        role_tokens = tokenize(role_text)
        
        # Intersection
        common = cv_tokens.intersection(role_tokens)
        
        return list(common)
