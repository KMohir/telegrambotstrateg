import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_content_ideas(answers: dict):
    prompt = f"""
    Instagram uchun kontent g'oyalar va senariy yaratib ber.
    
    Ma'lumotlar:
    1. Mavzu: {answers.get('topic')}
    2. Auditoriya: {answers.get('audience')}
    3. Maqsad: {answers.get('goal')}
    4. Ohang: {answers.get('tone')}
    5. Format: {answers.get('format')}
    6. Qo'shimcha: {answers.get('additional')}
    
    Vazifa:
    3 ta variantda kontent g'oya va senariy yozib ber. Har bir variant quyidagi tuzilishga ega bo'lsin:
    - G'oya nomi
    - Hook (3 sekundlik ilmoq)
    - Asosiy qism (Body)
    - CTA (Harakatga chaqiruv)
    - Qo'shimcha tavsiya
    
    Javobni faqat O'zbek tilida qaytar.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or gpt-4 if available/preferred
            messages=[
                {"role": "system", "content": "Sen Instagram marketing bo'yicha ekspert va ssenariystsan."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"
