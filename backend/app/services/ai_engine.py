import re
import io
from PyPDF2 import PdfReader
from docx import Document

# Lista básica de palabras vacías en español e inglés para limpiar ruido
STOPWORDS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "se", "del", "las", "un", "por", "con", "no", "una", "su", "para", "es", "al", "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "fue", "este", "ha", "si", "porque", "esta", "son", "entre", "cuando", "muy", "sin", "sobre", "ser", "tiene", "tambien", "me", "hasta", "hay", "donde", "quien", "desde", "nos", "durante",
    "the", "and", "of", "to", "in", "a", "is", "for", "on", "with", "as", "by"
}

class AIEngine:
    def __init__(self):
        print("Logic NLP Engine initialized (Deterministic Mode).")

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

    def clean_tokenize(self, text: str):
        # 1. Minusculas y quitar caracteres especiales
        text = text.lower()
        text = re.sub(r'[^a-z0-9áéíóúñ\s]', '', text)
        # 2. Tokenizar por espacios
        tokens = set(text.split())
        # 3. Filtrar stopwords
        return {word for word in tokens if word not in STOPWORDS and len(word) > 2}

    def calculate_similarity_and_skills(self, cv_text: str, role_text: str):
        """
        Calcula score basado en coincidencia de palabras clave (Jaccard Index adaptado)
        """
        cv_tokens = self.clean_tokenize(cv_text)
        role_tokens = self.clean_tokenize(role_text)

        if not role_tokens:
            return 0, []

        # Intersección: Palabras que están en AMBOS (CV y Rol)
        intersection = cv_tokens.intersection(role_tokens)
        
        # Matched Skills (para mostrar en el frontend)
        matched_skills = list(intersection)

        match_count = len(intersection)
        
        # Curva "Demo Friendly":
        if match_count == 0: score = 10
        elif match_count <= 2: score = 45  # ¡Animo al usuario!
        elif match_count <= 4: score = 65
        elif match_count <= 6: score = 80  # Bastante bien
        elif match_count <= 9: score = 92  # Excelente
        else: score = 98  # Perfecto (>9 palabras)
        
        final_score = int(score)

        return final_score, matched_skills

    def analyze_cv(self, cv_text, role_text):
        """
        Function that orchestrates the analysis and returns the expected dictionary format.
        """
        score, skills = self.calculate_similarity_and_skills(cv_text, role_text)
        return {
            "score": score,
            "matched_skills": skills[:10],  # Top 10 coincidencias
            "explanation": f"Se encontraron {len(skills)} coincidencias clave entre el CV y el perfil del cargo."
        }
