import io
import re
import os
import requests
import json
from PyPDF2 import PdfReader
from docx import Document

class AIEngine:
    def __init__(self):
        self.api_url = "https://router.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.api_token = os.environ.get("HF_TOKEN")
        print("AI Engine initialized via Hugging Face API.")

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
        
        payload = {"inputs": text}
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                # The API returns a list of floats directly for a single string input
                # Example: [0.1, 0.2, ...]
                data = response.json()
                # Safety check: ensure it's a list even if API format changes
                if isinstance(data, list):
                    # Sometimes API returns [[...]] if inputs is a list
                    if len(data) > 0 and isinstance(data[0], list):
                        return data[0] 
                    return data
            else:
                print(f"HF API Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"HF API Exception: {e}")
        
        # Fallback: Zero vector (384 dimensions for MiniLM)
        return [0.0] * 384

    def calculate_similarity(self, embedding1, embedding2):
        # Manual Cosine Similarity (No numpy/scikit-learn)
        # Cosine Similarity = (A . B) / (||A|| * ||B||)
        
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
        
        # Clamp between 0 and 1 just in case floating point errors
        similarity = max(0.0, min(1.0, similarity))
        
        return int(similarity * 100)

    def extract_keywords(self, text: str, role_text: str = ""):
        # Simple Explainability Logic (Regex based, no heavy NLP)
        
        def tokenize(s):
            # Lowercase and split by non-alphanumeric
            words = re.findall(r'\b[a-z]{3,}\b', s.lower())
            return set(words)

        cv_tokens = tokenize(text)
        role_tokens = tokenize(role_text)
        
        # Intersection
        common = cv_tokens.intersection(role_tokens)
        
        return list(common)
