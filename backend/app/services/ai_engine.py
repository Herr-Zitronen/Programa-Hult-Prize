import re
import io
from PyPDF2 import PdfReader
from docx import Document

class AIEngine:
    def __init__(self):
        print("Logic NLP Engine initialized (Deterministic Mode - Aggressive).")

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
        # Limpieza agresiva: minúsculas y solo alfanuméricos
        text = text.lower()
        # Reemplazar puntuación por espacios para no pegar palabras
        text = re.sub(r'[^a-z0-9áéíóúñ]', ' ', text) 
        tokens = set(text.split())
        
        # LISTA NEGRA EXTENDIDA (Español e Inglés)
        STOPWORDS = {
            # Gramática básica
            "de", "la", "que", "el", "en", "y", "a", "los", "del", "las", "un", "una", "por", "para", "con", "no", "sus", "su", "es", "lo", "al", "como", "mas", "pero",
            "is", "the", "and", "to", "of", "in", "for", "on", "with", "as", "by", "an", "are", "be", "or", "at",
            # Palabras "Relleno" de RRHH (¡Aquí está el truco!)
            "experiencia", "experience", "trabajo", "work", "job", "equipo", "team", "teams", "grupo", 
            "buscamos", "looking", "candidato", "candidate", "perfil", "profile", "habilidades", "skills",
            "conocimientos", "knowledge", "nivel", "level", "años", "years", "capacidad", "ability",
            "excelente", "excellent", "manejo", "uso", "using", "profesional", "professional",
            "responsabilidades", "funciones", "cargo", "puesto", "empresa", "company", "sector"
        }
        
        return {w for w in tokens if w not in STOPWORDS and len(w) > 2}

    def get_embedding(self, text: str):
        # Mock para compatibilidad con llamadas legacy
        return []

    def calculate_similarity_and_skills(self, cv_text: str, role_text: str):
        cv_tokens = self.clean_tokenize(cv_text)
        role_tokens = self.clean_tokenize(role_text)

        intersection = cv_tokens.intersection(role_tokens)
        match_count = len(intersection)
        
        # FÓRMULA DE CONTRASTE:
        # Si match_count es bajo (1 o 2), el score se queda bajo.
        # Necesitas al menos 3 o 4 palabras CLAVE reales para subir.
        if match_count == 0: score = 5
        elif match_count == 1: score = 25 # Una coincidencia aislada no es suficiente
        elif match_count == 2: score = 45 # Mejorando...
        elif match_count == 3: score = 65 # Aceptable
        elif match_count == 4: score = 80 # Muy bueno
        else: score = 90 + (match_count * 2) # Excelente

        # Cap at 99
        final_score = int(min(99, score))

        return final_score, list(intersection)

    def analyze_cv(self, cv_text, role_text):
        """
        Function that orchestrates the analysis and returns the expected dictionary format.
        """
        score, skills = self.calculate_similarity_and_skills(cv_text, role_text)
        return {
            "score": score,
            "matched_skills": skills[:10],  # Top 10 coincidencias
            "explanation": f"Se encontraron {len(skills)} coincidencias clave."
        }
