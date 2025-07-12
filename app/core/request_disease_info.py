import os
from typing import Dict
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def get_more_info(disease_name: str) -> Dict:
    prompt = f"""
        You are an agricultural assistant trained to support Ghanaian farmers. Your task is to provide detailed, localized information about crop diseases in a structured format.

        Given the crop disease name below, generate the following in **clean and short bullet points**:

        1. The disease name (keep as-is)
        2. Common symptoms (3–5 bullet points)
        3. Causes or how the disease spreads (2–4 points)
        4. Treatment options available to farmers (3–5 points)
        5. Prevention tips to reduce the chance of infection (3–5 points)

        Return your result in this exact structured JSON format:

        {{
        "name": "<exact disease name>",
        "symptoms": ["<point 1>", "<point 2>", "..."],
        "causes": ["<cause 1>", "<cause 2>", "..."],
        "treatments": ["<treatment 1>", "..."],
        "preventions": ["<prevention 1>", "..."]
        }}

        Make sure the tips are suitable for smallholder farmers in Ghana, especially in rural settings with limited access to chemicals or tools.

        Crop disease to analyze: "{disease_name}"
    """.strip()

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt).text
    print(response)

    # to avoid wasting out tokens lets use a pre-propmted response;
    # from app.utils.utils import text
    # response = text

    try:
        if (response):
            clean_text = response.strip().lstrip("```json").rstrip("```").strip()
            data_dict = json.loads(clean_text)
            return data_dict
        else:
            return "error"
        
    except Exception as e:
        print("[Gemini Parsing Error]", e)
        raise Exception("Gemini did not return valid structured JSON.")



if __name__ == "__main__":
    disease = "Maize - leaf beetle"
    reply = get_more_info(disease)

    print(" AI Reply:\n")
    print(reply, type(reply))
